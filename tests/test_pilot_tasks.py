"""Pilot-v0 has ≥10 tasks across five capabilities. Holdout stays empty."""

from __future__ import annotations

from pathlib import Path

import yaml

from scicap_core.invoke import invoke

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "benchmarks" / "pilot-v0" / "tasks.yaml"
HOLDOUT = ROOT / "benchmarks" / "pilot-v0" / "holdout"
CAPS = ROOT / "packages" / "scicap-neuro" / "capabilities"

REQUIRED_CAPABILITIES = {
    "neuro.t1.hippocampal_volumes",
    "neuro.bids.validate",
    "neuro.t1.anatomical_segmentation",
    "neuro.t1.register",
    "neuro.t1.regional_stats",
}


def test_pilot_has_ten_tasks_across_five_capabilities() -> None:
    data = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    tasks = data["tasks"]
    assert len(tasks) >= 10
    capability_ids = {task.get("capability") or data.get("capability") for task in tasks}
    assert REQUIRED_CAPABILITIES <= capability_ids
    assert data["holdout_tuning"] == "forbidden"


def test_pilot_gold_matches_invoke() -> None:
    data = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    default_cap = data.get("capability")
    for task in data["tasks"]:
        capability_id = task.get("capability") or default_cap
        instance = ROOT / task["instance"]
        result = invoke(CAPS / f"{capability_id}.yaml", instance)
        assert result["decision"] == task["gold"], task["id"]
        assert result["executed"] is False


def test_holdout_empty_of_tasks() -> None:
    assert HOLDOUT.is_dir()
    task_files = [
        path
        for path in HOLDOUT.iterdir()
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml", ".json"}
    ]
    assert task_files == [], f"holdout must stay empty of tasks: {task_files}"
    readme = HOLDOUT / "README.md"
    assert readme.is_file()
    text = readme.read_text(encoding="utf-8").lower()
    assert "empty" in text or "tuning" in text
