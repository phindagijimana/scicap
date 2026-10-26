# SciCap methods

Paper 1 protocol · 26 October 2026 · planning document, no results claimed

This is the locked methods stack for SciCap. It follows the literature map and the limitations-to-methods filter. SciCap is a **Boutiques/CWL profile plus an invoke decision and a causal evaluation**, not a new descriptor language and not an MCP adapter.

Related documents: [blueprint](Paper1_Research_Blueprint.pdf) · [literature map](SciCap_Literature_Map.md) · [limitations to methods](SciCap_Limitations_to_Methods.md)

---

## 1. Scope

**Question.** On held-out neuroimaging intents, do explicit scientific fields — bound to the instance at invoke time — raise scientifically correct completions and appropriate abstention compared with matched standard tool interfaces?

**Unit.** One scientific intent, one data fixture, one available catalog. SciCap decides whether a *single* capability may be invoked, with what arguments, or must be refused.

**Non-scope.** Multi-step composition checking is Paper 2 (SciGuard). The public agent benchmark is Paper 3 (NeuroAgentBench). Generic CWL/Boutiques→MCP translation is prior art (Coala, Nipoppy MCP).

---

## 2. The four methods

These are the Paper 1 methods. They are not optional product features.

### M1. Late binding of scientific types

The contract describes a **capability**, not a dataset. Predicates such as modality, reference space, atlas, and units are bound at invoke time to BIDS/NIDM fields on the actual files.

- Do not write dataset-specific skills (`hcp-skill`).
- Reuse BIDS/NIDM vocabulary. Do not invent a parallel ontology.
- Transfer to an unseen accession is a required test of this method.

### M2. Three-valued invoke decision

Every invoke attempt returns exactly one of:

| Decision | Meaning | Gold use |
|---|---|---|
| `ALLOW` | Required scientific predicates are established | Run only after permission |
| `REJECT` | A contradiction is demonstrated (wrong space, wrong atlas) | Must not invoke |
| `ABSTAIN` | Evidence is missing or insufficient | Asking or stopping is correct |

`ABSTAIN` is never scored as success or as failure in the primary table. Report unsafe acceptance, valid acceptance, and abstention coverage as separate rates.

### M3. Information-budget-matched field ablation

Representation is the intervention. The same scientific facts appear in every arm; only the encoding changes.

**Required arms**

| Arm | Encoding |
|---|---|
| A | Official documentation + permitted commands |
| B | MCP / OpenAPI JSON Schema only |
| C | Real Boutiques or CWL descriptors, MCP-exposed |
| C2 | Nipoppy MCP, if installable |
| D | C plus SciCap scientific fields (late binding) |
| E | D minus one field group (space, atlas, preconditions, QC) |
| F | Length-matched prose stating the same facts |
| G | Markdown Skill stating the same facts (Balis / NeuroClaw style) |

Primary confirmatory contrast: **C vs D** on scientifically correct end-state or justified abstention. F and G exist so a gain cannot be explained as extra tokens or a Skill.

### M4. Silent-failure disclosure

A zero exit code is not a scientific success. The contract must declare:

- `unsupported_cases`
- `qc_required` / `qc_status`
- `output_completeness`: `full` | `partial` | `unknown`
- `interpretation_limits`

An agent that reports regional volumes from an incomplete segmentation without `qc_status=passed` is a **false success**.

---

## 3. Representation (what is implemented)

SciCap is a **profile** on Boutiques and CWL, with lossless import/export. The runtime must work with no LLM configured.

Scientific fields bound at invoke time (M1), when present on the instance:

- `kind`, `modality`, `format`
- `space` (BIDS `space-` / `tpl-` or NIDM coordinate space)
- `atlas` / label set
- `units`
- `value_type` (e.g. discrete labels vs continuous)

Disclosure fields (M4):

- `unsupported_cases`, `qc_required`, `qc_status`, `output_completeness`, `interpretation_limits`

Identity, container digest, command template, and syntactic input groups remain the underlying Boutiques/CWL descriptor. SciCap does not replace them.

---

## 4. Primary and secondary endpoints

**Primary (pre-register before confirmatory runs).** Proportion of held-out tasks whose end-state is scientifically correct: admissible tool and valid arguments, **or** justified `ABSTAIN` / `REJECT`, as defined by the task oracle.

**Secondary**

- Selection accuracy
- Argument validity
- Unsafe acceptance of invalid or incomplete requests
- Valid acceptance (to detect over-refusal)
- False-success rate (execution or claim of success with failed scientific checks)
- Abstention coverage and calibration
- Provenance completeness
- Latency, tokens, authoring time (exploratory)

Paired design; task-level resampling or mixed models; 95% intervals; one primary contrast. Do not treat repeated model draws as independent new tasks.

---

## 5. Pilot that decides the methods are real

Ten-or-so tasks, at least two model families, arms C, F, G, and D:

| Task class | Gold | Method under test |
|---|---|---|
| Complete metadata, right tool | `ALLOW` + correct args | M5 endpoint / M3 |
| Wrong space, complete metadata | `REJECT` | M1, M2 |
| Right tool, space missing | `ABSTAIN` | M2 |
| DK vs DKT label swap | `REJECT` | M1 |
| Incomplete segmentation asked for volumes | Do not report biological zeros | M4 |
| Unseen OpenNeuro accession | Transfer without a dataset skill | M1 vs arm G |
| Same facts in prose and Skill | Typed fields still win | M3 |

**Go.** D beats C and is not explained by F or G, especially on missing metadata and unseen data.  
**No-go for a methods paper.** Gains vanish under Boutiques/CWL/Nipoppy or vanish when token budget is matched. Then offer the fields upstream and publish software.

---

## 6. Boundaries with the other papers

| Method | Owner |
|---|---|
| M1–M4 as specified above | **SciCap (Paper 1)** |
| Edge-level space/atlas/interpolation checks on a DAG | SciGuard (Paper 2) |
| Public artifact-level agent benchmark | NeuroAgentBench (Paper 3) |
| Automated tool-knowledge-graph extraction | SciToolAgent future work; not ours |
| Generic descriptor-to-MCP adapter | Coala / Nipoppy; dependency only |

Paper 1 may use a small frozen held-out set to test the contract. Paper 3 must not republish that confirmatory table as an independent finding.

---

## 7. Journal gates (locked with the methods)

The methods above are enough for a specialist methods paper. They are **not**, by themselves, a Nature-family contribution.

| If the confirmatory study shows… | Venue |
|---|---|
| Clear paired gain in neuroimaging; fair C/C2/F/G arms; held-out tools; field ablations | **Write to *Imaging Neuroscience*** (or *NeuroImage*) |
| Modest or null effect; usable profile, tests, catalog | *GigaScience*, *SoftwareX*, or *JOSS* |
| Large gain, independent datasets, typed fields beat prose and Skills, **and** a second domain on the same schema | Reconsider *Nature Communications* only then |
| Same plus a general late-binding framework, not just neuro fields | *Nature Computational Science* remains a stretch, not a plan |

**Do not submit to *Nature Methods*.** That journal wants a general life-science method with biological impact. SciCap is an agent-interface increment on existing descriptors.

**Do not design the project as a Nature paper.** Default target is *Imaging Neuroscience*. Revisit only after the confirmatory results exist.

---

## 8. What these methods are not

Do not describe SciCap as any of the following in the manuscript:

- A new machine-readable tool descriptor (Boutiques, CWL)
- An MCP adapter for scientific CLIs (Coala, Nipoppy MCP)
- The first BIDS-aware neuroimaging agent (NeuroClaw)
- A scientific tool knowledge graph (SciToolAgent)
- A new EDAM-style ontology
- Formal composition verification (Paper 2)

---

## 9. Implementation correspondence

| Method | Code / schema location |
|---|---|
| M1 late binding | `packages/scicap-core` bind step; `packages/scicap-neuro/capabilities` |
| M2 ALLOW / REJECT / ABSTAIN | `packages/scicap-core` invoke decision; machine-readable error records |
| M3 matched arms and ablations | `benchmarks/` frozen tasks; do not tune contracts on the holdout |
| M4 disclosures | capability YAML fields; false-success scoring in `benchmarks/` |

The base registry, validation, and documentation generation must run with no model API configured.
