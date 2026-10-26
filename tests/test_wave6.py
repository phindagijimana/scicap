"""Wave 6: point pilot-v0 at fetched S0 T1w. No download. No SciCap tokens from Boutiques."""

from __future__ import annotations

import urllib.request
from pathlib import Path

import yaml

from scicap_core.boutiques_baseline import SCICAP_DECISIONS, check_invocable
from scicap_core.invoke import invoke
from scicap_core.s0 import (
    GZIP_MAGIC,
    S0_REL_FROM_SCICAP,
    S0_REL_FROM_WORKSPACE,
    find_ds000003_t1w,
    is_public_gzip_t1w,
    s0_status,
)

ROOT = Path(__file__).resolve().parents[1]
SHARED = next(p for p in (ROOT.parent / "shared", ROOT / "shared") if p.is_dir())
TASKS = ROOT / "benchmarks" / "pilot-v0" / "tasks.yaml"
HOLDOUT = ROOT / "benchmarks" / "pilot-v0" / "holdout"
CAPS = ROOT / "packages" / "scicap-neuro" / "capabilities"
S0_INSTANCE = ROOT / "examples" / "instances" / "s0_public_t1w.json"
S0_MISSING = ROOT / "examples" / "instances" / "s0_public_missing_space.json"
TRACE = ROOT / "docs" / "METHODS_TRACE.md"
BASELINE = ROOT / "packages" / "scicap-core" / "boutiques_baseline.py"
S0_MOD = ROOT / "packages" / "scicap-core" / "s0.py"
CAPABILITY = CAPS / "neuro.t1.hippocampal_volumes.yaml"

_NETWORK_TOKENS = ("urlopen", "urlretrieve", "requests.get", "httpx", "wget")
_S0_T1W_TOKEN = "ds000003/sub-01/anat/sub-01_T1w.nii.gz"


def _s0_tasks() -> list[dict]:
    data = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    return [task for task in data["tasks"] if task.get("s0")]


def test_s0_locator_does_not_download(monkeypatch) -> None:
    def _boom(*_args, **_kwargs):
        raise AssertionError("pytest must not download OpenNeuro")

    monkeypatch.setattr(urllib.request, "urlopen", _boom)
    monkeypatch.setattr(urllib.request, "urlretrieve", _boom)
    status = s0_status()
    assert status["download_in_pytest"] is False
    assert status["bytes_in_git"] is False
    assert status["accession"] == "ds000003"
    assert status["relpath"] == S0_REL_FROM_WORKSPACE


def test_s0_python_has_no_network_fetch() -> None:
    text = S0_MOD.read_text(encoding="utf-8")
    lowered = text.lower()
    assert "openneuro.org" not in lowered
    assert all(token not in text for token in _NETWORK_TOKENS)


def test_pilot_tasks_point_at_s0_path() -> None:
    text = TASKS.read_text(encoding="utf-8")
    assert _S0_T1W_TOKEN in text
    assert S0_REL_FROM_SCICAP in text
    tasks = _s0_tasks()
    assert len(tasks) >= 2
    for task in tasks:
        pointed = " ".join(
            str(task.get(key, "")) for key in ("t1w", "path", "bids_root", "instance")
        )
        assert _S0_T1W_TOKEN in pointed or "ds000003" in pointed
        assert task["gold"] in {"ALLOW", "REJECT", "ABSTAIN"}


def test_s0_instances_point_at_external_path() -> None:
    for path in (S0_INSTANCE, S0_MISSING):
        payload = path.read_text(encoding="utf-8")
        assert _S0_T1W_TOKEN in payload
        assert "bytes_in_git" in payload


def test_holdout_still_empty() -> None:
    assert HOLDOUT.is_dir()
    leftover = [
        path
        for path in HOLDOUT.iterdir()
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml", ".json"}
    ]
    assert leftover == []


def test_s0_t1w_gzip_magic_when_present() -> None:
    status = s0_status()
    found = find_ds000003_t1w()
    if not status["present"]:
        assert found is None
        return
    assert found is not None
    assert is_public_gzip_t1w(found)
    head = found.read_bytes()[:2]
    assert head == GZIP_MAGIC
    assert found.stat().st_size > 1024
    assert found.name == "sub-01_T1w.nii.gz"
    assert "shared/data/external/ds000003" in str(found)


def test_s0_public_t1w_allow_and_missing_space_abstain() -> None:
    allow = invoke(CAPABILITY, S0_INSTANCE)
    abstain = invoke(CAPABILITY, S0_MISSING)
    assert allow["decision"] == "ALLOW"
    assert allow["executed"] is False
    assert allow["bound"]["space"] == "subject_native"
    assert abstain["decision"] == "ABSTAIN"
    assert "space" in abstain["missing"]
    assert abstain["bound"]["space"] is None
    assert abstain["decision"] not in {"ALLOW", "REJECT"}


def test_s0_pilot_gold_matches_invoke() -> None:
    for task in _s0_tasks():
        result = invoke(CAPS / f"{task['capability']}.yaml", ROOT / task["instance"])
        assert result["decision"] == task["gold"], task["id"]
        assert result["executed"] is False
        assert result["decision"] in SCICAP_DECISIONS


def test_boutiques_baseline_on_s0_does_not_emit_decisions() -> None:
    result = check_invocable(S0_INSTANCE)
    assert "decision" not in result
    assert SCICAP_DECISIONS.isdisjoint(result.keys())
    assert SCICAP_DECISIONS.isdisjoint(
        {value for value in result.values() if isinstance(value, str)}
    )
    assert result["boutiques_invocable"] is True
    assert result["download_in_pytest"] is False
    assert _S0_T1W_TOKEN in str(result["invocation"].get("t1w", ""))


def test_no_nifti_copied_into_scicap() -> None:
    hits = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and (
            path.name.lower().endswith(".nii") or path.name.lower().endswith(".nii.gz")
        )
    ]
    assert hits == [], f"do not copy S0 NIfTI into 01_SciCap: {hits}"


def test_methods_trace_records_wave6() -> None:
    text = TRACE.read_text(encoding="utf-8")
    assert "Wave 6" in text
    assert _S0_T1W_TOKEN in text or "shared/data/external" in text
    assert "gzip" in text.lower() or "\\x1f\\x8b" in text
    assert "ALLOW" in text and "REJECT" in text and "ABSTAIN" in text
    assert "does not download" in text.lower() or "not download" in text.lower()
    baseline = BASELINE.read_text(encoding="utf-8")
    assert "ALLOW" in baseline and "REJECT" in baseline and "ABSTAIN" in baseline
    assert "must not" in baseline.lower() or "does **not** return" in baseline
