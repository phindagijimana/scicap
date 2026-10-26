"""Make packages/scicap-core importable as scicap_core without a model API."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

CORE = Path(__file__).resolve().parents[1] / "packages" / "scicap-core"

for key in (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
):
    os.environ.pop(key, None)


def _load_scicap_core() -> None:
    if "scicap_core" in sys.modules:
        return
    spec = importlib.util.spec_from_file_location(
        "scicap_core",
        CORE / "__init__.py",
        submodule_search_locations=[str(CORE)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load scicap_core from {CORE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["scicap_core"] = module
    spec.loader.exec_module(module)


_load_scicap_core()


@pytest.fixture(autouse=True)
def _no_model_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "AZURE_OPENAI_API_KEY",
        "GOOGLE_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)
