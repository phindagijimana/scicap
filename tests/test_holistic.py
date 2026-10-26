"""Same four S0 instances through Boutiques and scicap invoke.

Behavioral residual only. Not a measured evaluation result.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scicap_core.boutiques_baseline import SCICAP_DECISIONS, check_invocable
from scicap_core.invoke import invoke

ROOT = Path(__file__).resolve().parents[1]
SHARED = next(p for p in (ROOT.parent / "shared", ROOT / "shared") if p.is_dir())
CAPABILITY = (
    ROOT
    / "packages"
    / "scicap-neuro"
    / "capabilities"
    / "neuro.t1.hippocampal_volumes.yaml"
)

# Same four instances. Boutiques invocability is per the File-only descriptor.
CASES = (
    (
        "complete_t1w",
        SHARED / "fixtures" / "valid" / "complete_t1w" / "instance.json",
        True,
        "ALLOW",
    ),
    (
        "missing_space",
        SHARED / "fixtures" / "invalid" / "missing_space" / "instance.json",
        True,
        "ABSTAIN",
    ),
    (
        "dk_as_dkt",
        SHARED / "fixtures" / "invalid" / "dk_as_dkt" / "instance.json",
        True,
        "REJECT",
    ),
    (
        "wrong_modality",
        SHARED / "fixtures" / "invalid" / "wrong_modality" / "instance.json",
        True,
        "REJECT",
    ),
)


@pytest.mark.parametrize(
    "name,path,boutiques_ok,scicap",
    CASES,
    ids=[row[0] for row in CASES],
)
def test_same_instance_boutiques_and_scicap(
    name: str,
    path: Path,
    boutiques_ok: bool,
    scicap: str,
) -> None:
    public = check_invocable(path)
    profile = invoke(CAPABILITY, path)
    assert public["boutiques_invocable"] is boutiques_ok
    assert "decision" not in public
    assert SCICAP_DECISIONS.isdisjoint(public.keys())
    assert profile["decision"] == scicap
    if name == "missing_space":
        assert profile["bound"]["space"] is None
        assert "space" in profile["missing"]


def test_boutiques_does_not_already_decide_the_four_cases() -> None:
    """Methods §5 go-gate residual: not a measured result."""
    scicap_decisions: list[str] = []
    for _name, path, boutiques_ok, scicap in CASES:
        public = check_invocable(path)
        profile = invoke(CAPABILITY, path)
        assert public["boutiques_invocable"] is boutiques_ok
        assert public.get("decision") not in SCICAP_DECISIONS
        assert profile["decision"] == scicap
        scicap_decisions.append(profile["decision"])
    assert set(scicap_decisions) == {"ALLOW", "REJECT", "ABSTAIN"}
    boutiques_flags = {
        check_invocable(path)["boutiques_invocable"] for _n, path, _b, _s in CASES
    }
    assert boutiques_flags == {True}


def test_model_api_key_unset() -> None:
    assert os.environ.get("OPENAI_API_KEY") is None


def test_no_nifti_in_scicap_or_shared() -> None:
    """NIfTI may exist under gitignored shared/data/external/ after an opt-in fetch."""
    external = (SHARED / "data" / "external").resolve()
    hits = []
    for root in (ROOT, SHARED):
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            resolved = path.resolve()
            if resolved == external or external in resolved.parents:
                continue
            name = path.name.lower()
            if name.endswith(".nii") or name.endswith(".nii.gz"):
                hits.append(path)
    assert hits == [], f"NIfTI must not be in git: {hits}"
