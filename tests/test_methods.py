"""Locked M1 / M4 wiring. Wave-1 invoke tests stay in test_invoke.py."""

from __future__ import annotations

from pathlib import Path

import yaml

from scicap_core.bind import bind, load_capability, load_instance
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
COMPLETE = SHARED / "fixtures" / "valid" / "complete_t1w" / "instance.json"
MISSING_SPACE = SHARED / "fixtures" / "invalid" / "missing_space" / "instance.json"
DK_AS_DKT = SHARED / "fixtures" / "invalid" / "dk_as_dkt" / "instance.json"


def test_m1_binds_space_atlas_modality_from_instance() -> None:
    capability = load_capability(CAPABILITY)
    instance = load_instance(DK_AS_DKT)
    binding = bind(capability, instance)
    assert binding["bound"]["modality"] == instance["modality"]
    assert binding["bound"]["space"] == instance["space"]
    assert binding["bound"]["atlas"] == instance["atlas"]
    assert capability.get("dataset") is None
    assert "hcp" not in str(capability.get("id", "")).lower()


def test_m1_capability_is_not_a_dataset() -> None:
    capability = yaml.safe_load(CAPABILITY.read_text(encoding="utf-8"))
    assert capability["id"] == "neuro.t1.hippocampal_volumes"
    assert "accession" not in capability
    assert capability.get("input", {}).get("space") == "subject_native"
    result = invoke(capability, MISSING_SPACE)
    assert result["decision"] == "ABSTAIN"
    assert result["bound"]["space"] is None
    assert "space" in result["missing"]


def test_m4_disclosures_and_exit_zero_is_not_science() -> None:
    result = invoke(CAPABILITY, COMPLETE)
    assert result["decision"] == "ALLOW"
    assert result["qc_required"] is True
    assert result["qc_status"] == "unknown"
    assert result["unsupported_cases"]
    assert result["interpretation_limits"]
    assert result["output_completeness"] in {"full", "partial", "unknown"}
    assert result["executed"] is False
    assert result["approval_required"] is True
    assert result["approval_granted"] is False


def test_m4_fields_live_on_capability_schema() -> None:
    capability = yaml.safe_load(CAPABILITY.read_text(encoding="utf-8"))
    for field in (
        "unsupported_cases",
        "qc_required",
        "qc_status",
        "interpretation_limits",
    ):
        assert field in capability
    assert capability["output"]["output_completeness"] == "unknown"
    assert capability["qc_status"] != "passed"
