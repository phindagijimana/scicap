# Agent instructions — SciCap (Paper 1)

Read [`docs/SciCap_Methods.md`](docs/SciCap_Methods.md) before writing code. This folder is a **Boutiques/CWL profile plus an invoke decision**, not a new descriptor language and not an MCP server.

Program build plan: [`../docs/BUILD_PLAN.md`](../docs/BUILD_PLAN.md) · S0 fixture: [`../shared/AGENTS.md`](../shared/AGENTS.md)

## Mission

On one capability and the S0 instances, bind scientific fields at invoke time and return exactly `ALLOW`, `REJECT`, or `ABSTAIN`. Missing `space` is never inferred as true.

## Do not build

- A new Boutiques/CWL/MCP (Coala, Nipoppy MCP already exist).
- Dataset-specific skills (`hcp-skill`).
- A workflow engine or composition checker (that is SciGuard).
- An LLM in the invoke path.
- A website before `scicap invoke` works offline.

## Locked methods you must implement

| ID | Rule |
|---|---|
| M1 | Capability ≠ dataset. Bind `space`, `atlas`, `units`, `value_type`, `modality` from the instance (BIDS/NIDM names). |
| M2 | Invoke returns one of `ALLOW` / `REJECT` / `ABSTAIN` plus a machine-readable reason. |
| M3 | Same facts can be shown as Boutiques-only later; do not bake SciCap fields into the Boutiques baseline. |
| M4 | `unsupported_cases`, `qc_required`, `qc_status`, `output_completeness`, `interpretation_limits`. Exit 0 is not scientific success. |

## Reuse

Boutiques or CWL for identity, CLI template, container digest. BIDS sidecar / `space-` / `atlas-` entities. Do not invent a parallel ontology.

## Current tree (keep)

```text
packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml
docs/SciCap_Methods.md
```

## Target tree

```text
packages/scicap-core/
  __init__.py
  bind.py          # instance → bound predicates; missing = absent, not default
  invoke.py        # ALLOW | REJECT | ABSTAIN
  cli.py
packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml
examples/instances/   # JSON sidecars for S0 fixtures (or copies of shared/)
benchmarks/pilot-v0/  # task list; do not tune on holdout
tests/test_invoke.py
pyproject.toml        # console_script: scicap
```

## CLI

```text
scicap invoke packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml \
  --instance examples/instances/complete_t1w.json
```

Stdout JSON (required keys):

```json
{
  "capability_id": "neuro.t1.hippocampal_volumes",
  "decision": "ALLOW",
  "bound": {"modality": "T1w", "space": "subject_native", "atlas": null},
  "missing": [],
  "reason": "required predicates established",
  "qc_status": "unknown",
  "approval_required": true
}
```

`decision` enum: `ALLOW` | `REJECT` | `ABSTAIN`. Do not execute the container in v0 unless approval is passed as an explicit flag; default is decide-only.

## First vertical slice (must pass)

| Instance | Gold |
|---|---|
| Complete T1w, space present, no atlas contradiction | `ALLOW` |
| DK labels declared as DKT | `REJECT` |
| `space` omitted | `ABSTAIN` |
| Wrong modality (DWI offered as T1w) | `REJECT` |

Never fill missing `space` from the capability default and then ALLOW.

## Bind rule

1. Read capability YAML (see existing hippocampal_volumes file).
2. Read instance JSON: BIDS-like fields `Modality`/`modality`, `Space`/`space`, `Atlas`/`atlas`, paths.
3. For each required predicate: if instance has a value, bind it; if absent, record in `missing`.
4. If any bound value contradicts the capability (modality, space, atlas) → `REJECT`.
5. Else if any required predicate is missing → `ABSTAIN`.
6. Else → `ALLOW` (still `approval_required: true`).

Required predicates for v0: `modality`, `space`. Atlas is required only when the instance claims a label set.

## Tests

`tests/test_invoke.py` must run with `OPENAI_API_KEY` unset (unset it in the test process). Cover the four instances above. Assert `ABSTAIN` is not coerced to `REJECT` or `ALLOW`.

## Boundaries

- Composition of two tools → SciGuard. Do not add DAG checking here.
- Scoring an agent run → NeuroAgentBench.
- Do not treat a later NeuroInsight call as this paper’s RCT.

## Done when

- `scicap invoke` works offline on the four instances.
- Capability YAML still carries M4 disclosure fields.
- `pytest` green with no model API.

Stop. Do not implement MCP adapters or the full M3 arm matrix until the go-gate in methods §5 is re-read.
