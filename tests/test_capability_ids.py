"""`scicap invoke` accepts a bundled capability id, so pip users need no checkout."""

from __future__ import annotations

from pathlib import Path

from scicap_core.cli import main, resolve_capability

ROOT = Path(__file__).resolve().parents[1]
CAPS = ROOT / "packages" / "scicap-neuro" / "capabilities"
INSTANCE = ROOT / "examples" / "instances" / "s0_public_t1w.json"


def test_every_capability_id_resolves() -> None:
    for path in CAPS.glob("*.yaml"):
        resolved = Path(resolve_capability(path.stem))
        assert resolved.is_file(), path.stem
        assert resolved.name == path.name


def test_path_still_wins() -> None:
    path = CAPS / "neuro.t1.register.yaml"
    assert resolve_capability(str(path)) == str(path)


def test_unknown_id_is_left_for_invoke_to_report() -> None:
    assert resolve_capability("neuro.does.not.exist") == "neuro.does.not.exist"


def test_cli_invoke_by_id(capsys) -> None:
    code = main(["invoke", "neuro.t1.anatomical_segmentation", "--instance", str(INSTANCE)])
    assert code == 0
    assert '"decision": "ALLOW"' in capsys.readouterr().out


def test_pyproject_ships_capabilities() -> None:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"scicap_core.capabilities" = "packages/scicap-neuro/capabilities"' in text
