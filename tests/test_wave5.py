"""Wave 5: live Boutiques when importable; no OpenNeuro download; no SciCap tokens."""

from __future__ import annotations

import urllib.request
from pathlib import Path

from scicap_core.boutiques_baseline import (
    SCICAP_DECISIONS,
    boutiques_pypi_installed,
    check_invocable,
)

_ROOT = Path(__file__).resolve().parents[1]
SHARED = next(p for p in (_ROOT.parent / "shared", _ROOT / "shared") if p.is_dir())
COMPLETE = SHARED / "fixtures" / "valid" / "complete_t1w" / "instance.json"
BASELINE = _ROOT / "packages" / "scicap-core" / "boutiques_baseline.py"
TRACE = _ROOT / "docs" / "METHODS_TRACE.md"

_NETWORK_TOKENS = ("urlopen", "urlretrieve", "requests.get", "httpx", "wget")


def test_baseline_mode_is_live_when_importable() -> None:
    result = check_invocable(COMPLETE)
    assert result["baseline_mode"] in {"live", "recorded"}
    if boutiques_pypi_installed():
        assert result["baseline_mode"] == "live"
        assert result["used_boutiques_pypi"] is True
        assert result["descriptor_valid"] is True
        assert result["invocation_valid"] is True
    else:
        assert result["baseline_mode"] == "recorded"
        assert result["used_boutiques_pypi"] is False
    assert result["boutiques_invocable"] is True
    assert "decision" not in result
    assert SCICAP_DECISIONS.isdisjoint(result.keys())
    assert SCICAP_DECISIONS.isdisjoint(
        {value for value in result.values() if isinstance(value, str)}
    )


def test_pytest_does_not_download_openneuro(monkeypatch) -> None:
    def _boom(*_args, **_kwargs):
        raise AssertionError("pytest must not download OpenNeuro")

    monkeypatch.setattr(urllib.request, "urlopen", _boom)
    monkeypatch.setattr(urllib.request, "urlretrieve", _boom)
    result = check_invocable(COMPLETE)
    assert result["download_in_pytest"] is False
    assert result["boutiques_invocable"] is True


def test_scicap_python_has_no_openneuro_fetch() -> None:
    roots = (_ROOT / "packages", _ROOT / "scicap")
    hits: list[str] = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            if "openneuro.org" in lowered:
                hits.append(str(path))
            if any(token in text for token in _NETWORK_TOKENS):
                hits.append(str(path))
    assert hits == [], f"SciCap pytest must not fetch OpenNeuro: {hits}"
    baseline = BASELINE.read_text(encoding="utf-8")
    assert "openneuro.org" not in baseline.lower()
    assert "urlopen" not in baseline
    assert "urlretrieve" not in baseline
    assert "no OpenNeuro" in baseline or "download OpenNeuro" in baseline


def test_methods_trace_records_wave5_live_or_recorded() -> None:
    text = TRACE.read_text(encoding="utf-8")
    assert "Wave 5" in text
    assert "baseline_mode" in text
    assert "does not download" in text.lower() or "not downloaded" in text.lower()
    if boutiques_pypi_installed():
        assert "live" in text
    else:
        assert "recorded" in text
    assert "ALLOW" in text and "REJECT" in text and "ABSTAIN" in text
