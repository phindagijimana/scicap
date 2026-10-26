"""Three-valued invoke decision (M2). No model. No container execution by default."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .bind import bind, load_capability, load_instance
from .execute import dry_run

_SCHEMA_PATH = Path(__file__).with_name("result.schema.json")
_RESULT_VALIDATOR = Draft202012Validator(
    json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
)


def _reason(decision: str, binding: dict[str, Any]) -> tuple[str, str]:
    if decision == "REJECT":
        first = binding["contradictions"][0]
        predicate = first["predicate"]
        if first.get("detail") == "declared_atlas_contradicts_label_set":
            return (
                "atlas_contradiction",
                (
                    f"atlas contradiction: declared {first['instance']} "
                    f"but label_set {first['label_set']}"
                ),
            )
        return (
            f"{predicate}_contradiction",
            (
                f"{predicate} contradiction: instance {first.get('instance')} "
                f"vs capability {first.get('capability')}"
            ),
        )
    if decision == "ABSTAIN":
        missing = ",".join(binding["missing"])
        return (
            "required_predicates_missing",
            f"required predicates missing: {missing}",
        )
    return ("required_predicates_established", "required predicates established")


def decide(binding: dict[str, Any]) -> str:
    # M2 residual vs Boutiques: invocation schema is binary (typed inputs
    # present → invocable). Boutiques has no ABSTAIN and does not return
    # ALLOW/REJECT. Missing space is not an invocation-schema miss.
    if binding["contradictions"]:
        return "REJECT"
    if binding["missing"]:
        return "ABSTAIN"
    return "ALLOW"


def invoke(
    capability: dict[str, Any] | str | Path,
    instance: dict[str, Any] | str | Path,
    *,
    approve: bool = False,
) -> dict[str, Any]:
    """Return ALLOW / REJECT / ABSTAIN. Never infer missing space as true."""
    if not isinstance(capability, dict):
        capability = load_capability(capability)
    if not isinstance(instance, dict):
        instance = load_instance(instance)

    binding = bind(capability, instance)
    decision = decide(binding)
    reason_code, reason = _reason(decision, binding)

    result = {
        "capability_id": binding["capability_id"],
        "decision": decision,
        "bound": {
            "modality": binding["bound"].get("modality"),
            "space": binding["bound"].get("space"),
            "atlas": binding["bound"].get("atlas"),
        },
        "missing": list(binding["missing"]),
        "reason": reason,
        "reason_code": reason_code,
        "qc_status": binding["qc_status"],
        "approval_required": binding["approval_required"],
        "approval_granted": bool(approve),
        "executed": False,
        "unsupported_cases": binding["disclosures"]["unsupported_cases"],
        "qc_required": binding["disclosures"]["qc_required"],
        "output_completeness": binding["disclosures"]["output_completeness"],
        "interpretation_limits": binding["disclosures"]["interpretation_limits"],
        "dry_run": False,
        "container_pulled": False,
    }
    if approve:
        # Gated dry-run only: no container pull, QC did not run.
        exec_info = dry_run(capability, instance, decision=decision)
        result["executed"] = exec_info["executed"]
        result["dry_run"] = exec_info["dry_run"]
        result["container_pulled"] = exec_info["container_pulled"]
        result["qc_status"] = exec_info["qc_status"]
        result["execute_status"] = exec_info["execute_status"]
        result["execute_note"] = exec_info["execute_note"]
    _RESULT_VALIDATOR.validate(result)
    return result
