"""Public Boutiques baseline. No ALLOW / REJECT / ABSTAIN. No model API."""

from __future__ import annotations

import json
from pathlib import Path

from scicap_core.boutiques_baseline import (
    DEFAULT_DESCRIPTOR,
    FILE_TYPE_RULE,
    SCICAP_DECISIONS,
    check_invocable,
    load_descriptor,
    scicap_fields_in_descriptor,
)

ROOT = Path(__file__).resolve().parents[1]
SHARED = next(p for p in (ROOT.parent / "shared", ROOT / "shared") if p.is_dir())
INSTANCES = {
    "complete_t1w": SHARED / "fixtures" / "valid" / "complete_t1w" / "instance.json",
    "missing_space": SHARED / "fixtures" / "invalid" / "missing_space" / "instance.json",
    "dk_as_dkt": SHARED / "fixtures" / "invalid" / "dk_as_dkt" / "instance.json",
    "wrong_modality": SHARED / "fixtures" / "invalid" / "wrong_modality" / "instance.json",
}


def _no_scicap_decision(result: dict) -> None:
    assert "decision" not in result
    assert SCICAP_DECISIONS.isdisjoint(result.keys())
    assert SCICAP_DECISIONS.isdisjoint(
        {value for value in result.values() if isinstance(value, str)}
    )
    assert result["baseline_mode"] in {"live", "recorded"}
    assert result["download_in_pytest"] is False


def test_descriptor_has_no_scicap_fields() -> None:
    descriptor = load_descriptor(DEFAULT_DESCRIPTOR)
    assert scicap_fields_in_descriptor(descriptor) == []
    text = json.dumps(descriptor)
    for token in ('"space"', '"atlas"', '"qc_status"', '"ABSTAIN"'):
        assert token not in text


def test_complete_t1w_boutiques_invocable() -> None:
    result = check_invocable(INSTANCES["complete_t1w"])
    _no_scicap_decision(result)
    assert result["boutiques_invocable"] is True
    assert result["reasons"] == []
    assert result["invocation"]["t1w"]


def test_missing_space_still_boutiques_invocable() -> None:
    """Boutiques does not require space."""
    instance = json.loads(INSTANCES["missing_space"].read_text(encoding="utf-8"))
    assert "space" not in instance and "Space" not in instance
    result = check_invocable(instance)
    _no_scicap_decision(result)
    assert result["boutiques_invocable"] is True


def test_dk_as_dkt_still_boutiques_invocable() -> None:
    """Atlas is not a Boutiques type. Files/types still match."""
    result = check_invocable(INSTANCES["dk_as_dkt"])
    _no_scicap_decision(result)
    assert result["boutiques_invocable"] is True


def test_wrong_modality_follows_descriptor_file_type() -> None:
    """Wrong modality fails Boutiques only if File is further constrained.

    This descriptor's t1w input is type File with no value-choices. A DWI
    path is still a string File, so the invocation schema accepts it.
    That is not a SciCap REJECT.
    """
    descriptor = load_descriptor()
    t1w = next(item for item in descriptor["inputs"] if item["id"] == "t1w")
    assert t1w["type"] == "File"
    assert not t1w.get("value-choices")
    result = check_invocable(INSTANCES["wrong_modality"])
    _no_scicap_decision(result)
    assert result["boutiques_invocable"] is True
    assert "modality" not in FILE_TYPE_RULE.lower() or "not constrain" in FILE_TYPE_RULE
    assert result["file_type_rule"] == FILE_TYPE_RULE
