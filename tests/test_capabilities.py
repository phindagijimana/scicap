"""Four added capabilities: each has one ALLOW and one ABSTAIN or REJECT."""

from __future__ import annotations

from pathlib import Path

import yaml

from scicap_core.invoke import invoke

ROOT = Path(__file__).resolve().parents[1]
CAPS = ROOT / "packages" / "scicap-neuro" / "capabilities"
INST = ROOT / "examples" / "instances"

M4_FIELDS = (
    "unsupported_cases",
    "qc_required",
    "qc_status",
    "output_completeness",
    "interpretation_limits",
)

NEW_CAPABILITIES = (
    "neuro.bids.validate",
    "neuro.t1.anatomical_segmentation",
    "neuro.t1.register",
    "neuro.t1.regional_stats",
)

ALL_CAPABILITIES = ("neuro.t1.hippocampal_volumes",) + NEW_CAPABILITIES

# Each new capability: (allow_instance, other_instance, other_decision)
PAIRS = {
    "neuro.bids.validate": (
        "complete_bids.json",
        "missing_space.json",
        "ABSTAIN",
    ),
    "neuro.t1.anatomical_segmentation": (
        "complete_t1w.json",
        "wrong_modality.json",
        "REJECT",
    ),
    "neuro.t1.register": (
        "complete_t1w.json",
        "wrong_space_mni.json",
        "REJECT",
    ),
    "neuro.t1.regional_stats": (
        "complete_dkt.json",
        "dk_as_dkt.json",
        "REJECT",
    ),
}


def _cap(capability_id: str) -> Path:
    return CAPS / f"{capability_id}.yaml"


def test_five_capability_files_exist() -> None:
    found = {path.stem for path in CAPS.glob("*.yaml")}
    assert found == set(ALL_CAPABILITIES)


def test_m4_fields_on_every_capability() -> None:
    for capability_id in ALL_CAPABILITIES:
        text = _cap(capability_id).read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        for field in M4_FIELDS:
            assert field in text, f"{capability_id} missing {field}"
        assert data["qc_required"] is True
        assert data["qc_status"] == "unknown"
        assert data["unsupported_cases"]
        assert data["interpretation_limits"]
        completeness = (data.get("output") or {}).get(
            "output_completeness", data.get("output_completeness")
        )
        assert completeness in {"full", "partial", "unknown"}


def test_new_capabilities_allow_and_abstain_or_reject() -> None:
    for capability_id, (allow_name, other_name, other_gold) in PAIRS.items():
        allow = invoke(_cap(capability_id), INST / allow_name)
        other = invoke(_cap(capability_id), INST / other_name)
        assert allow["decision"] == "ALLOW", capability_id
        assert allow["capability_id"] == capability_id
        assert allow["executed"] is False
        assert other["decision"] == other_gold, capability_id
        assert other["decision"] in {"ABSTAIN", "REJECT"}
        assert other["executed"] is False
