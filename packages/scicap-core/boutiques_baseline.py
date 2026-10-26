"""Boutiques-only public baseline (M3 arm C).

Reuses the Boutiques 0.5 descriptor as identity / CLI / container substrate
(Glatard et al., 2018). This module does **not** return ALLOW / REJECT / ABSTAIN.

If ``import boutiques`` works, the installed package is called on the
Boutiques-only descriptor (descriptor and invocation-schema validation only;
no container launch; no OpenNeuro download) and ``baseline_mode`` is ``live``.
Otherwise this module keeps the recorded Boutiques 0.5 invocation-schema
contract and sets ``baseline_mode: recorded``. Do not claim a live Boutiques
call unless ``used_boutiques_pypi`` is true.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

# SciCap scientific fields. Boutiques 0.5 has none of these as input types.
# Coala / Nipoppy MCP / Paper2Agent occupy MCP adapters; this module is not one.
SCICAP_FIELDS = (
    "space",
    "atlas",
    "modality",
    "qc_status",
    "qc_required",
    "unsupported_cases",
    "interpretation_limits",
    "output_completeness",
    "invoke_decisions",
    "decision",
    "abstain",
    "ALLOW",
    "REJECT",
    "ABSTAIN",
    "units",
    "value_type",
)

SCICAP_DECISIONS = frozenset({"ALLOW", "REJECT", "ABSTAIN"})

# Boutiques File is a string path. Suffix / modality / space / atlas are not types.
FILE_TYPE_RULE = (
    "Boutiques File is a string path in the invocation schema. "
    "The descriptor type File does not constrain BIDS suffix, modality, "
    "space, or atlas. Wrong modality fails Boutiques only if the descriptor "
    "adds value-choices or an equivalent file constraint."
)

_PACKAGES = Path(__file__).resolve().parents[1]
DEFAULT_DESCRIPTOR = (
    _PACKAGES
    / "scicap-neuro"
    / "boutiques"
    / "neuro.t1.hippocampal_volumes.boutiques.json"
)

_FILE_KEYS = ("t1w", "path", "filename", "bids_name")


def boutiques_pypi_installed() -> bool:
    return importlib.util.find_spec("boutiques") is not None


def load_descriptor(path: str | Path | None = None) -> dict[str, Any]:
    target = Path(path) if path is not None else DEFAULT_DESCRIPTOR
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Boutiques descriptor must be an object: {target}")
    return data


def load_instance(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"instance JSON must be an object: {path}")
    return data


def scicap_fields_in_descriptor(descriptor: dict[str, Any]) -> list[str]:
    """Return SciCap keys baked into the Boutiques descriptor (must be empty)."""
    hits: list[str] = []
    top = set(descriptor.keys())
    for field in SCICAP_FIELDS:
        if field in top:
            hits.append(field)
    for item in descriptor.get("inputs") or []:
        if not isinstance(item, dict):
            continue
        ident = str(item.get("id", ""))
        if ident in SCICAP_FIELDS:
            hits.append(f"input:{ident}")
    return hits


def _present(value: Any) -> bool:
    return value is not None and value != ""


def _instance_file_path(instance: dict[str, Any]) -> Any:
    for key in _FILE_KEYS:
        if key in instance and _present(instance[key]):
            return instance[key]
    nested = instance.get("input")
    if isinstance(nested, dict):
        for key in _FILE_KEYS:
            if key in nested and _present(nested[key]):
                return nested[key]
    return None


def build_invocation(
    descriptor: dict[str, Any],
    instance: dict[str, Any],
    *,
    output_default: str = ".",
) -> dict[str, Any]:
    """Map instance files onto Boutiques inputs.

    Required non-File command parameters (e.g. output directory) are supplied
    as caller-side values. Boutiques callers always provide those; they are
    not scientific sidecar fields.
    """
    invocation: dict[str, Any] = {}
    file_path = _instance_file_path(instance)
    for item in descriptor.get("inputs") or []:
        if not isinstance(item, dict):
            continue
        ident = item.get("id")
        if not ident:
            continue
        itype = item.get("type")
        if ident in instance and _present(instance[ident]):
            invocation[ident] = instance[ident]
            continue
        if itype == "File" and _present(file_path):
            invocation[ident] = file_path
            continue
        if itype == "String" and not item.get("optional", False):
            invocation[ident] = output_default
    return invocation


def _type_ok(itype: str, value: Any, item: dict[str, Any]) -> str | None:
    listed = bool(item.get("list"))
    if listed:
        if not isinstance(value, list):
            return f"input {item.get('id')}: list {itype} must be an array"
        inner = [v for v in value]
        for entry in inner:
            err = _type_ok_scalar(itype, entry, item)
            if err:
                return err
        return None
    return _type_ok_scalar(itype, value, item)


def _type_ok_scalar(itype: str, value: Any, item: dict[str, Any]) -> str | None:
    ident = item.get("id")
    if itype == "File":
        if not isinstance(value, str):
            return f"input {ident}: File must be a string path"
        return None
    if itype == "String":
        if not isinstance(value, str):
            return f"input {ident}: String must be a string"
        return None
    if itype == "Number":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return f"input {ident}: Number must be a number"
        if item.get("integer") and not isinstance(value, int):
            return f"input {ident}: Number must be an integer"
        return None
    if itype == "Flag":
        if not isinstance(value, bool):
            return f"input {ident}: Flag must be a boolean"
        return None
    return f"input {ident}: unsupported Boutiques type {itype!r}"


def validate_invocation(
    descriptor: dict[str, Any],
    invocation: dict[str, Any],
) -> list[str]:
    """Recorded Boutiques 0.5 invocation-schema checks (not container launch)."""
    reasons: list[str] = []
    for item in descriptor.get("inputs") or []:
        if not isinstance(item, dict):
            continue
        ident = item.get("id")
        itype = item.get("type")
        optional = bool(item.get("optional", False))
        present = ident in invocation and _present(invocation[ident])
        if not optional and not present:
            reasons.append(f"required input missing: {ident} ({itype})")
            continue
        if not present:
            continue
        value = invocation[ident]
        type_err = _type_ok(str(itype), value, item)
        if type_err:
            reasons.append(type_err)
            continue
        choices = item.get("value-choices")
        if choices:
            candidates = value if isinstance(value, list) else [value]
            for entry in candidates:
                if entry not in choices:
                    reasons.append(
                        f"input {ident}: value {entry!r} not in value-choices"
                    )
    return reasons


def _call_boutiques_live(
    descriptor_path: Path,
    invocation: dict[str, Any],
) -> dict[str, Any] | None:
    """Call installed Boutiques on the descriptor. None if not installed.

    Descriptor and invocation-schema validation only. Do not launch a
    container, pull an image, or download OpenNeuro.
    """
    if not boutiques_pypi_installed():
        return None
    extra: dict[str, Any] = {
        "baseline_mode": "live",
        "used_boutiques_pypi": True,
        "boutiques_pypi_installed": True,
        "contract": "boutiques-0.5-pypi-descriptor-and-invocation",
        "download_in_pytest": False,
    }
    try:
        from boutiques.invocationSchemaHandler import (
            generateInvocationSchema,
            validateSchema,
        )
        from boutiques.validator import validate_descriptor

        descriptor = load_descriptor(descriptor_path)
        validate_descriptor(descriptor, descriptor_path=str(descriptor_path))
        extra["descriptor_valid"] = True
        schema = generateInvocationSchema(descriptor)
        validateSchema(schema, invocation)
        extra["invocation_valid"] = True
        extra["boutiques_call"] = "validate_descriptor+validateSchema"
        extra["boutiques_invocable"] = True
    except Exception as exc:
        extra["boutiques_pypi_error"] = str(exc)
        extra["boutiques_call"] = extra.get("boutiques_call", "failed")
        extra.setdefault("descriptor_valid", False)
        extra.setdefault("invocation_valid", False)
        try:
            from boutiques import InvocationValidationError
        except ImportError:  # pragma: no cover - package present if we got here
            InvocationValidationError = ()  # type: ignore[misc,assignment]
        if isinstance(exc, InvocationValidationError):
            extra["boutiques_invocable"] = False
            extra["live_invocation_error"] = str(exc)
    return extra


def check_invocable(
    instance: dict[str, Any] | str | Path,
    descriptor: dict[str, Any] | str | Path | None = None,
) -> dict[str, Any]:
    """Return Boutiques invocability. Never emit ALLOW / REJECT / ABSTAIN."""
    descriptor_path = DEFAULT_DESCRIPTOR
    if isinstance(descriptor, (str, Path)):
        descriptor_path = Path(descriptor)
        descriptor = load_descriptor(descriptor_path)
    elif not isinstance(descriptor, dict):
        descriptor = load_descriptor(descriptor_path)
    if not isinstance(instance, dict):
        instance = load_instance(instance)

    invocation = build_invocation(descriptor, instance)
    reasons = validate_invocation(descriptor, invocation)
    baked = scicap_fields_in_descriptor(descriptor)

    result = {
        "boutiques_invocable": reasons == [],
        "reasons": reasons,
        "descriptor_name": descriptor.get("name"),
        "tool_version": descriptor.get("tool-version"),
        "schema_version": descriptor.get("schema-version"),
        "invocation": invocation,
        "contract": "boutiques-0.5-invocation-schema-recorded",
        "used_boutiques_pypi": False,
        "boutiques_pypi_installed": boutiques_pypi_installed(),
        "baseline_mode": "recorded",
        "download_in_pytest": False,
        "file_type_rule": FILE_TYPE_RULE,
        "scicap_fields_in_descriptor": baked,
    }
    live = _call_boutiques_live(descriptor_path, invocation)
    if live:
        result.update(live)
    if any(key in result for key in SCICAP_DECISIONS):
        raise RuntimeError("Boutiques baseline must not use SciCap decision keys")
    if result.get("decision") in SCICAP_DECISIONS:
        raise RuntimeError("Boutiques baseline must not return a SciCap decision")
    for value in result.values():
        if isinstance(value, str) and value in SCICAP_DECISIONS:
            raise RuntimeError("Boutiques baseline must not emit a SciCap decision")
    return result
