"""Bind instance fields to capability predicates.

Missing values stay absent. Capability defaults are never copied onto the
instance (M1). BIDS / NIDM names are reused; no parallel ontology.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

REQUIRED_V0 = ("modality", "space")

FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "modality": ("modality", "Modality", "suffix"),
    "space": ("space", "Space", "SpatialReference", "spatial_reference"),
    "atlas": ("atlas", "Atlas"),
    "units": ("units", "Units"),
    "value_type": ("value_type", "ValueType", "valueType"),
    "kind": ("kind", "Kind"),
    "label_set": (
        "label_set",
        "LabelSet",
        "label_ontology",
        "atlas_source",
        "atlas_actual",
    ),
    "qc_status": ("qc_status", "QCStatus"),
}

# Filename entities are instance evidence (BIDS), not capability defaults.
_ENTITY_RE = re.compile(r"(?:^|_)([a-zA-Z0-9]+)-([a-zA-Z0-9+]+)")

# Compatibility families. Check DKT before DK (DK is a prefix of DKT).
_DKT_ATLAS = {
    "dkt",
    "desikan-killiany-tourville",
    "desikankillianytourville",
    "desikan_killiany_tourville",
}
_DK_ATLAS = {
    "dk",
    "desikan-killiany",
    "desikankilliany",
    "desikan_killiany",
    "aparc",
}
_T1W = {"t1w", "t1"}
_DWI = {"dwi", "dti", "diffusion"}
_SUBJECT_NATIVE = {
    "subject_native",
    "t1w",
    "individual",
    "orig",
    "native",
    "subject",
}


def load_capability(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"capability YAML must be a mapping: {path}")
    return data


def load_instance(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"instance JSON must be an object: {path}")
    return data


def _present(value: Any) -> bool:
    return value is not None and value != ""


def _lookup(record: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        if name in record and _present(record[name]):
            return record[name]
    nested = record.get("input")
    if isinstance(nested, dict):
        for name in names:
            if name in nested and _present(nested[name]):
                return nested[name]
    return None


def _entities_from_path(instance: dict[str, Any]) -> dict[str, str]:
    raw = instance.get("path") or instance.get("bids_name") or instance.get("filename")
    if not raw or not isinstance(raw, str):
        return {}
    stem = Path(raw).name
    found: dict[str, str] = {}
    for match in _ENTITY_RE.finditer(stem):
        found[match.group(1).lower()] = match.group(2)
    return found


def _normalize(value: Any) -> str:
    return str(value).strip().lower().replace(" ", "-")


def _atlas_family(value: Any) -> str | None:
    if not _present(value):
        return None
    token = _normalize(value)
    compact = token.replace("-", "").replace("_", "")
    if token in _DKT_ATLAS or "dkt" in token or "tourville" in token:
        return "DKT"
    if token in _DK_ATLAS or compact in {"dk", "desikankilliany"}:
        return "DK"
    return token


def _modality_family(value: Any) -> str | None:
    if not _present(value):
        return None
    token = _normalize(value)
    if token in _T1W:
        return "T1w"
    if token in _DWI:
        return "DWI"
    return token


def _space_family(value: Any) -> str | None:
    if not _present(value):
        return None
    token = _normalize(value)
    if token in _SUBJECT_NATIVE:
        return "subject_native"
    return token


def _capability_expected(capability: dict[str, Any], field: str) -> Any:
    block = capability.get("input")
    if isinstance(block, dict) and _present(block.get(field)):
        return block[field]
    if _present(capability.get(field)):
        return capability[field]
    return None


def _instance_field(instance: dict[str, Any], field: str) -> Any:
    aliases = FIELD_ALIASES.get(field, (field,))
    value = _lookup(instance, aliases)
    if _present(value):
        return value
    entities = _entities_from_path(instance)
    if field in entities:
        return entities[field]
    return None


def bind(capability: dict[str, Any], instance: dict[str, Any]) -> dict[str, Any]:
    """Bind predicates from the instance only. Missing stays missing."""
    bound: dict[str, Any] = {
        "modality": _instance_field(instance, "modality"),
        "space": _instance_field(instance, "space"),
        "atlas": _instance_field(instance, "atlas"),
        "units": _instance_field(instance, "units"),
        "value_type": _instance_field(instance, "value_type"),
        "kind": _instance_field(instance, "kind"),
    }
    label_set = _instance_field(instance, "label_set")
    qc_status = _instance_field(instance, "qc_status")
    if not _present(qc_status):
        qc_status = capability.get("qc_status", "unknown")

    missing: list[str] = []
    contradictions: list[dict[str, Any]] = []

    claims_label_set = _present(label_set) or _present(bound["atlas"])
    required = list(REQUIRED_V0)
    if claims_label_set and "atlas" not in required:
        required.append("atlas")

    for field in required:
        if not _present(bound.get(field)):
            missing.append(field)

    expected_modality = _capability_expected(capability, "modality")
    if _present(bound["modality"]) and _present(expected_modality):
        got = _modality_family(bound["modality"])
        want = _modality_family(expected_modality)
        if got != want:
            contradictions.append(
                {
                    "predicate": "modality",
                    "instance": bound["modality"],
                    "capability": expected_modality,
                }
            )

    expected_space = _capability_expected(capability, "space")
    if _present(bound["space"]) and _present(expected_space):
        got = _space_family(bound["space"])
        want = _space_family(expected_space)
        if got != want:
            contradictions.append(
                {
                    "predicate": "space",
                    "instance": bound["space"],
                    "capability": expected_space,
                }
            )

    expected_atlas = _capability_expected(capability, "atlas")
    if _present(bound["atlas"]) and _present(expected_atlas):
        if _atlas_family(bound["atlas"]) != _atlas_family(expected_atlas):
            contradictions.append(
                {
                    "predicate": "atlas",
                    "instance": bound["atlas"],
                    "capability": expected_atlas,
                }
            )

    if _present(bound["atlas"]) and _present(label_set):
        declared = _atlas_family(bound["atlas"])
        actual = _atlas_family(label_set)
        if declared != actual:
            contradictions.append(
                {
                    "predicate": "atlas",
                    "instance": bound["atlas"],
                    "label_set": label_set,
                    "detail": "declared_atlas_contradicts_label_set",
                }
            )

    return {
        "capability_id": capability.get("id", ""),
        "bound": bound,
        "missing": missing,
        "contradictions": contradictions,
        "label_set": label_set,
        "qc_status": qc_status if _present(qc_status) else "unknown",
        "approval_required": bool(
            (capability.get("execution") or {}).get("approval_required", True)
        ),
        "disclosures": {
            "unsupported_cases": capability.get("unsupported_cases") or [],
            "qc_required": capability.get("qc_required"),
            "output_completeness": (capability.get("output") or {}).get(
                "output_completeness", capability.get("output_completeness")
            ),
            "interpretation_limits": capability.get("interpretation_limits") or [],
        },
    }
