"""Gold invoke cases. OPENAI_API_KEY is unset in conftest (no model API)."""

from __future__ import annotations

import json
import os
from pathlib import Path

from scicap_core.cli import main
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

GOLD = {
    "complete_t1w": (
        SHARED / "fixtures" / "valid" / "complete_t1w" / "instance.json",
        "ALLOW",
    ),
    "dk_as_dkt": (
        SHARED / "fixtures" / "invalid" / "dk_as_dkt" / "instance.json",
        "REJECT",
    ),
    "missing_space": (
        SHARED / "fixtures" / "invalid" / "missing_space" / "instance.json",
        "ABSTAIN",
    ),
    "wrong_modality": (
        SHARED / "fixtures" / "invalid" / "wrong_modality" / "instance.json",
        "REJECT",
    ),
}


def test_model_api_key_unset() -> None:
    assert os.environ.get("OPENAI_API_KEY") is None


def test_complete_t1w_allow() -> None:
    result = invoke(CAPABILITY, GOLD["complete_t1w"][0])
    assert result["decision"] == "ALLOW"
    assert result["capability_id"] == "neuro.t1.hippocampal_volumes"
    assert result["bound"]["modality"] == "T1w"
    assert result["bound"]["space"] == "subject_native"
    assert result["missing"] == []
    assert result["approval_required"] is True
    assert result["executed"] is False
    assert result["qc_required"] is True
    assert result["unsupported_cases"]
    assert result["interpretation_limits"]


def test_dk_as_dkt_reject() -> None:
    result = invoke(CAPABILITY, GOLD["dk_as_dkt"][0])
    assert result["decision"] == "REJECT"
    assert result["reason_code"] == "atlas_contradiction"
    assert "atlas" in result["reason"]


def test_missing_space_abstain() -> None:
    result = invoke(CAPABILITY, GOLD["missing_space"][0])
    assert result["decision"] == "ABSTAIN"
    assert "space" in result["missing"]
    assert result["bound"]["space"] is None
    assert result["decision"] not in {"ALLOW", "REJECT"}


def test_missing_space_not_filled_from_capability() -> None:
    """Never copy capability input.space and then ALLOW."""
    result = invoke(CAPABILITY, GOLD["missing_space"][0])
    assert result["decision"] == "ABSTAIN"
    assert result["bound"]["space"] != "subject_native"
    assert "space" in result["missing"]


def test_wrong_modality_reject() -> None:
    result = invoke(CAPABILITY, GOLD["wrong_modality"][0])
    assert result["decision"] == "REJECT"
    assert result["reason_code"] == "modality_contradiction"
    assert result["bound"]["modality"] == "DWI"


def test_abstain_not_coerced() -> None:
    result = invoke(CAPABILITY, GOLD["missing_space"][0])
    assert result["decision"] == "ABSTAIN"
    assert result["decision"] != "REJECT"
    assert result["decision"] != "ALLOW"


def test_cli_complete_t1w(capsys) -> None:
    example = ROOT / "examples" / "instances" / "complete_t1w.json"
    code = main(["invoke", str(CAPABILITY), "--instance", str(example)])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["decision"] == "ALLOW"
    assert payload["executed"] is False


def test_m4_fields_remain_on_capability() -> None:
    text = CAPABILITY.read_text(encoding="utf-8")
    for field in (
        "unsupported_cases",
        "qc_required",
        "qc_status",
        "output_completeness",
        "interpretation_limits",
    ):
        assert field in text
