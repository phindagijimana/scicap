"""Gated dry-run execute. --approve does not pull a container."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from scicap_core.cli import main
from scicap_core.invoke import invoke

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY = (
    ROOT
    / "packages"
    / "scicap-neuro"
    / "capabilities"
    / "neuro.t1.hippocampal_volumes.yaml"
)
COMPLETE = ROOT / "examples" / "instances" / "complete_t1w.json"


def test_without_approve_does_not_execute() -> None:
    result = invoke(CAPABILITY, COMPLETE)
    assert result["approval_granted"] is False
    assert result["executed"] is False
    assert result["dry_run"] is False
    assert result["container_pulled"] is False
    assert result["qc_status"] == "unknown"


def test_approve_is_dry_run_only(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_args, **_kwargs):
        raise AssertionError("gated execute must not start a process")

    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "call", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    result = invoke(CAPABILITY, COMPLETE, approve=True)
    assert result["approval_granted"] is True
    assert result["executed"] is False
    assert result["dry_run"] is True
    assert result["container_pulled"] is False
    assert result["qc_status"] in {"unknown", "did_not_run"}


def test_cli_approve_dry_run(capsys) -> None:
    code = main(
        ["invoke", str(CAPABILITY), "--instance", str(COMPLETE), "--approve"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["executed"] is False
    assert payload["dry_run"] is True
    assert payload["container_pulled"] is False
    assert payload["qc_status"] in {"unknown", "did_not_run"}
    assert payload["decision"] == "ALLOW"
