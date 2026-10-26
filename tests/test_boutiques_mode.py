"""Recorded-or-real Boutiques baseline. Never emits SciCap decisions."""

from __future__ import annotations

from pathlib import Path

from scicap_core.boutiques_baseline import (
    SCICAP_DECISIONS,
    boutiques_pypi_installed,
    check_invocable,
)

_ROOT = Path(__file__).resolve().parents[1]
SHARED = next(p for p in (_ROOT.parent / "shared", _ROOT / "shared") if p.is_dir())
COMPLETE = SHARED / "fixtures" / "valid" / "complete_t1w" / "instance.json"


def test_baseline_mode_recorded_or_real() -> None:
    result = check_invocable(COMPLETE)
    assert "decision" not in result
    assert SCICAP_DECISIONS.isdisjoint(result.keys())
    if boutiques_pypi_installed():
        assert result["baseline_mode"] == "live"
        assert result["used_boutiques_pypi"] is True
        assert "validate_descriptor" in result.get("boutiques_call", "")
    else:
        assert result["baseline_mode"] == "recorded"
        assert result["used_boutiques_pypi"] is False
    assert result["boutiques_invocable"] is True
    assert result["download_in_pytest"] is False
