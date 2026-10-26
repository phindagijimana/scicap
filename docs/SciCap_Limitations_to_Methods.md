# Limitations that can become methods

SciCap / agent-navigable scientific computing · 26 October 2026

This note takes stated or structural limits of the closest systems and asks which ones are **methods**, not missing features. A limitation is a method only if it yields a representation, decision rule, or evaluation protocol that can be tested against a fair baseline. The locked Paper 1 protocol is [`SciCap_Methods.md`](SciCap_Methods.md).

**Filter used here**

| Keep as a method | Discard as a feature gap |
|---|---|
| New decision rule or type | “They do not cover neuroimaging” |
| New scoring or evidence rule | “They need more tools in the catalog” |
| Isolates representation from extra tokens | “Write a GUI / automate the KG” |
| Survives Boutiques + CWL + MCP + Skills | “Expose the same descriptor over MCP” |

---

## 1. What the closest systems cannot do

| System | Limitation they state or structurally have | Why it is not already a SciCap paper |
|---|---|---|
| Boutiques / CWL | Encode syntax, files, containers. No space, atlas, units, QC, abstain. | Adding fields is a **profile**. The method is the *decision rule + RCT*, not the YAML. |
| Coala (2026) | CWL → MCP only. Depends on existing CWL. Treats valid invocation as success. LLM becomes the workflow engine. | Adapter is taken. Residual: they never score **scientific** success or **UNKNOWN**. |
| Nipoppy MCP | Exposes Boutiques + dataset *status*, not invoke-time scientific legality. | Catalog baseline. Residual: status ≠ “this T1w is in the wrong space for this tool.” |
| SciToolAgent | Manual KG; compatibility is operational (I/O, deps). Safety is ethics/toxicity. Score is answer accuracy. Relies on GPT-4o. | “Tool KG helps planning” is published. Residual: inspectable, LLM-independent contracts + scientific (not ethical) gates. |
| Balis Skills | Domain knowledge is markdown. Extra information is confounded with representation. | Skills are a **required control arm**, not something to reimplement. |
| NeuroClaw | BIDS-grounded **skills**, often dataset-specific (`hcp-skill`). Gains mix environment pinning, skills, and metadata. No descriptor ablation. | First BIDS-aware agent is taken. Residual: **late binding** of types from instance metadata vs early binding in skills. |
| EDAM / bio.tools / APE | Topic, Operation, Data, Format. No coordinate space, atlas identity, transform direction. | Do not invent a competing Topic list. Residual: a **small dependent type** for imaging artifacts. |
| NIDM / BIDS Derivatives | Space and atlas exist on **data/results**, not on **tool contracts**. | Reuse the vocabulary. The method is the **binding at invoke time**. |
| ToolUniverse audit (2026) | Silent failures: tool returns partial/ambiguous output; agent treats it as complete. | Directly motivates **unsupported-cases** and **QC-not-run** as first-class outcomes. |
| Agent benchmarks | Mean task success; AST/execution match; Unknown dropped or scored as fail. | Residual belongs partly to Paper 3. Paper 1 still needs **abstention ≠ failure**. |

SciToolAgent’s own discussion names two limits: manual KG curation and proprietary-LLM dependence. Those are engineering/scaling limits. Automating the KG is **their** future work, not a SciCap method.

---

## 2. Methods worth keeping (Paper 1)

Ranked by how much they change the paper if the pilot works.

### M1. Late binding of scientific types (strongest distinction vs NeuroClaw)

**Limitation.** NeuroClaw skills bake dataset knowledge into the agent (`hcp-skill` plans HCP). Boutiques/CWL never see instance metadata. The agent either overfits a dataset or ignores space/atlas.

**Method.** Separate *capability* from *instance*:

- Contract says: input must be `kind=parcellation, atlas=DK, space=subject_T1w`.
- At invoke time, bind those predicates to BIDS/NIDM fields on the actual files.
- Compatible / incompatible / insufficient evidence is computed **now**, not written into a dataset skill.

**Test.** Same agent, same tools: (G) NeuroClaw-style skill that names the dataset versus (D) dataset-agnostic contract + instance metadata. Transfer to an unseen accession is the point.

**Owner.** Paper 1. Paper 2 uses the same binding on workflow edges.

### M2. Three-valued invoke decision (not binary schema check)

**Limitation.** Coala/Boutiques/MCP: schema valid → run. Missing space metadata is either ignored or treated as invalid. Agent-eval papers now warn that scoring Unknown as fail or success biases the result (evidence-supported bounds, 2026).

**Method.** Every invoke returns one of:

- `ALLOW` — required scientific predicates established
- `REJECT` — contradiction demonstrated (wrong space, wrong atlas)
- `ABSTAIN` — evidence missing; asking or stopping is the correct action

Never collapse `ABSTAIN` into success or failure in the primary table. Report unsafe acceptance **and** valid acceptance **and** abstention coverage.

**Test.** Include incomplete-metadata tasks whose gold label is abstain. Primary contrast: schema-MCP vs SciCap on unsafe acceptance, with abstention reported separately.

**Owner.** Paper 1 for single-tool invoke. Paper 2 for composition. Do not claim a new formal logic unless you prove a property on a closed predicate subset.

### M3. Information-budget-matched field ablation (the paper’s causal method)

**Limitation.** Every 2026 agent paper that “adds metadata” also adds words. Balis Skills raised intent accuracy 44% → 83%, but Skills are extra documents. NeuroClaw mixes skills, BIDS context, and pinned environments.

**Method.** Treat representation as the intervention:

1. Same facts in Boutiques/CWL, in length-matched prose, in a Skill file, and in typed SciCap fields.
2. Ablate space, atlas, preconditions, QC one group at a time.
3. Pre-register the primary contrast (e.g. Boutiques-MCP vs SciCap on scientific end-state).

If typed fields do not beat length-matched prose and Skills, there is no methods paper.

**Owner.** Paper 1. This is how you answer “you just wrote more tokens.”

### M4. Silent-failure disclosures on the contract

**Limitation.** ToolUniverse audit (arXiv:2609.26836): invocation can succeed while output is truncated, unqualified, or scientifically incomplete, and the agent amplifies it. SciToolAgent “safety” is toxicity, not “QC was not run.”

**Method.** First-class contract fields:

- `unsupported_cases`
- `qc_required` / `qc_status`
- `output_completeness` (full | partial | unknown)
- `interpretation_limits`

An agent that reports hippocampal volume from a failed segmentation without `qc_status=passed` is a **false success**, even if the CLI exited 0.

**Test.** Seed tasks whose correct behavior is “do not treat missing regions as biological zero” (already in the Paper 3 draft). Score false-success rate.

**Owner.** Paper 1 fields + Paper 3 scoring. Closest thing to a timely 2026 methods hook.

### M5. Scientific end-state as the primary endpoint (evaluation method)

**Limitation.** BFCL, ToolBench, Coala demos, and SciToolEval score call shape, tool path, or answer text. NeuroClaw’s NeuroBench is closer but not a controlled descriptor intervention.

**Method.** For each task, lock before scoring: admissible tools, admissible arguments, required abstention, artifact checks. Primary number: scientifically correct end-state **or** justified abstention. Report execution success beside it, never instead of it.

**Owner.** Shared by Papers 1 and 3. Paper 1 uses a small held-out set to test the contract. Paper 3 is the public benchmark. Do not publish the same confirmatory table twice.

---

## 3. Methods that belong next door (do not steal them)

| Method | Whose limitation | Which paper |
|---|---|---|
| Edge-level semantic checking (space/atlas/interpolation along a DAG) | CWL/Nipype type-check files, not meaning | **Paper 2 SciGuard** |
| Artifact-level neuroimaging agent benchmark | NeuroClaw/ScienceAgentBench do not isolate descriptor fields | **Paper 3 NeuroAgentBench** |
| Automated KG extraction from papers/docs | SciToolAgent’s stated future work | Not SciCap; they claimed it |
| Generic CWL/Boutiques → MCP adapter | Coala / Nipoppy | Dependency, not a result |
| New Topic/Operation ontology | EDAM already exists | Bind to BIDS/NIDM instead |

---

## 4. Feature gaps that look like methods but are not

Do not build a paper on these:

- “Neuroimaging is missing from SciToolAgent / ToolUniverse / Coala.” That is a domain application.
- “We have more tools / a nicer catalog / a website.”
- “We automate contract authoring with an LLM.” That is SciToolAgent’s own roadmap and will look derivative.
- “We add containers and provenance.” Already Boutiques, CWL, RO-Crate.
- “We add a permission dialog.” Product, unless you show calibrated abstention (M2).

---

## 5. Recommended methods stack for the Imaging Neuroscience paper

One representation, one decision rule, one evaluation protocol:

1. **Representation (M1):** Boutiques/CWL *profile* that late-binds BIDS/NIDM fields (modality, space, atlas, units) plus unsupported/QC disclosures (M4).
2. **Decision rule (M2):** `ALLOW` / `REJECT` / `ABSTAIN` at invoke time; UNKNOWN never scored as success.
3. **Evaluation (M3 + M5):** paired RCT against Boutiques-MCP, Nipoppy MCP, length-matched prose, and a Skill arm; field ablations; scientific end-state + false-success + abstention coverage.

That stack uses other people’s limitations without claiming their objects. It is enough for a specialist methods paper if the pilot moves those three numbers. It is not enough for *Nature Computational Science* unless M1 is shown to be a general late-binding pattern in a second domain.

---

## 6. Pilot that tells you if these are real methods

Ten tasks, two models, four arms (Boutiques-MCP, prose, Skill, SciCap):

| Task class | Gold | Which method it tests |
|---|---|---|
| Right tool, complete metadata | ALLOW + correct args | M5 |
| Wrong space, complete metadata | REJECT / do not invoke | M1, M2 |
| Right tool, space missing | ABSTAIN | M2 |
| DK vs DKT label swap | REJECT | M1 |
| Segmentation incomplete, agent asked for volumes | do not report zeros; flag QC | M4 |
| Unseen OpenNeuro accession, same tool | transfer | M1 vs NeuroClaw-style skill |
| Length-matched docs state the space rule | SciCap should still win if typing matters | M3 |

If SciCap only wins when it has more words than Boutiques, stop. If it wins on incomplete metadata and unseen datasets, you have methods M1–M2, not a wrapper.

---

## 7. Decision

Turn **late binding**, **three-valued invoke**, **matched ablation**, and **silent-failure disclosure** into the Paper 1 methods. Leave composition to SciGuard, the large benchmark to NeuroAgentBench, and KG automation to SciToolAgent. That is the limitation set this field will actually grant you.
