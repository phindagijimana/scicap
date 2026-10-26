"""Gated dry-run execute.

``scicap invoke --approve`` may record a dry-run only. It does not pull a
container, start Apptainer/Docker, or treat exit 0 as scientific success.
Without ``--approve``, this module is not used to execute.
"""

from __future__ import annotations

from typing import Any

QC_DID_NOT_RUN = "did_not_run"


def dry_run(
    capability: dict[str, Any],
    instance: dict[str, Any],
    *,
    decision: str,
) -> dict[str, Any]:
    """Record approval without running the pinned container."""
    del capability, instance, decision
    return {
        "executed": False,
        "dry_run": True,
        "container_pulled": False,
        "qc_status": QC_DID_NOT_RUN,
        "execute_status": "dry_run",
        "execute_note": (
            "approval recorded; container not pulled; QC did not run"
        ),
    }
