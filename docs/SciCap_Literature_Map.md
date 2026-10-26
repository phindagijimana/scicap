# SciCap literature map

**Paper 1 — Scientific capability contracts**  
Scoping review and novelty matrix · 26 October 2026 · search cutoff 26 October 2026

**Status.** Deep literature map for claim-setting, not a PRISMA systematic review and not a finding that SciCap works. Quantitative targets in the blueprint remain proposed. Re-run the searches and lock bibliographic metadata before any manuscript submission. This refresh does **not** claim a new descriptor language.

**Bottom line.** A new tool-descriptor language, a new MCP server, or a new workflow engine is not a defensible contribution. Boutiques, CWL, OWL-S/WINGS, EDAM/bio.tools, Coala, Nipoppy MCP, ToolUniverse, SciToolAgent, Paper2Agent, and NeuroClaw already occupy those slots. The only claim that still looks testable is whether **neuroimaging-specific scientific fields** — reference space, atlas identity, units, scientific preconditions, QC obligations, and calibrated abstention — improve held-out agent end-states when added to a **matched** Boutiques/CWL/MCP baseline.

---

## 1. Search protocol

### 1.1 Sources queried on 26 October 2026

Web search over publisher sites, arXiv, PubMed/PMC, official specifications, and GitHub, using the Paper 1 Boolean clusters plus snowball from the closest 2025–2026 hits. Clusters A–E and the Extra registry cluster were re-run on this date. No new descriptor language was found or claimed.

| Cluster | Query family | What it was meant to catch |
|---|---|---|
| A | scientific workflow + semantic / ontology / type system + validation / composition | Kepler, WINGS, APE, OWL-S, SAWSDL |
| B | LLM/AI agent + tool discovery / selection + benchmark / metadata | ToolBench, Gorilla/BFCL, TOOLRET, SciToolAgent, SciAgentGym |
| C | MCP / OpenAPI / Boutiques / CWL / Nipype + scientific / neuroimaging | Coala, Nipoppy MCP, Boutiques schema, BIDS execution spec |
| D | science automation / agentic science + workflow generation / execution | Balis 2026, Paper2Agent, NeuroClaw |
| E | BIDS / neuroimaging + interoperability / semantic constraints / agent | NIDM, BIDS-prov, BABS, Nipoppy |
| Extra | EDAM, bio.tools, Galaxy, WorkflowHub, RO-Crate, ToolUniverse, NIDM | registries, provenance, coordinate semantics |

### 1.2 What this map is not

- Not an exhaustive ACM / IEEE / PubMed screen with recorded inclusion counts.
- Not a field-by-field audit of every Boutiques or CWL document in the wild.
- Not a claim that all 2026 preprints will remain the version of record.
- Peer-review status of NeuroClaw, SciToolAgent-Evo, SciAgentGym, and Balis et al. must be rechecked at submission.

### 1.3 How to read threat levels

| Level | Meaning for SciCap |
|---|---|
| **Blocker** | Already implements the thing SciCap would otherwise call novel. Do not claim that object. |
| **High** | Same job, different encoding. Must be a baseline or a hard differentiator. |
| **Must-cite baseline** | Fair experimental comparator even if conceptually older. |
| **Adjacent** | Method or evaluation lesson; not a direct product competitor. |
| **Reuse** | Emit or import this standard; do not replace it. |

### 1.4 Refresh log (26 October 2026)

Re-ran clusters A–E plus Extra. Live hits confirmed; **no fabricated DOIs**. Five material updates relative to the 25 October map:

1. **Coala** remains *Bioinformatics* **42(9):btag641**, published 26 August 2026, DOI [10.1093/bioinformatics/btag641](https://doi.org/10.1093/bioinformatics/btag641). CWL→MCP adapter + containerized `cwltool` execution. Still a **blocker** for any SciCap-as-adapter claim.
2. **Nipoppy MCP** remains the Brainhack 2026 neuroimaging catalog (`nipoppy://pipelines/{name}/{version}/descriptor` is the Boutiques descriptor). Nipoppy **0.4.6** is listed as a 2 April 2026 release. OHBM BrainHack 2026 issue [#72](https://github.com/ohbm/hackathon2026/issues/72) automates Boutiques authoring; it does **not** add space, atlas, QC, or abstain.
3. **NeuroClaw** technical report is still [arXiv:2604.24696](https://arxiv.org/abs/2604.24696) (27 April 2026; HTML versions v1–v3 visible). The public repo now brands **NeuroDiscovery** (v1.0.0 noted 15 September 2026 on the project README): knowledge graph + hypothesis generator + NeuroRuntime. Still BIDS-grounded **skills**, not invoke-time `ALLOW`/`REJECT`/`ABSTAIN`.
4. **Paper2Agent** remains *Nature*, 16 September 2026, DOI [10.1038/s41586-026-11044-y](https://doi.org/10.1038/s41586-026-11044-y). Companion news item: [10.1038/d41586-026-02899-2](https://doi.org/10.1038/d41586-026-02899-2). Paper→MCP conversion; not a neuroimaging capability contract.
5. **Go-gate vs Boutiques/Nipoppy.** Neither Boutiques invocation schema nor Nipoppy MCP status resources decide the four v0 gold cases (complete T1w `ALLOW`; DK-as-DKT `REJECT`; omitted `space` `ABSTAIN`; DWI-as-T1w `REJECT`). They check files/types/catalog status. SciCap invoke is therefore not redundant with those systems. Offer fields upstream only if a later descriptor audit shows they already encode the predicates.

Cluster A (WINGS, APE, EDAM, Kepler OWL types) and cluster B (SciToolAgent-Evo / OpenSciToolBench, SciAgentGym) were re-queried; identities match the 25 October entries. ToolUniverse silent-failure audit [arXiv:2609.26836](https://arxiv.org/abs/2609.26836) remains the M4 prior (NeurIPS 2026 workshop acceptance is stated on the HTML preprint; not treated as a journal version of record).

---

## 2. Landscape in six layers

SciCap sits at the intersection of six mature literatures. Novelty has to survive all six, not just “agent papers from 2024.”

```
Layer 6  Evaluation of agents and tool retrieval
Layer 5  Neuroimaging data semantics (BIDS, NIDM, atlases, spaces)
Layer 4  Agentic science systems (Paper2Agent, Balis, NeuroClaw, SciToolAgent)
Layer 3  Agent transport (MCP, OpenAPI, Coala, ToolUniverse, Nipoppy MCP)
Layer 2  Semantic service and workflow typing (OWL-S, WINGS, EDAM, APE)
Layer 1  Executable tool descriptors (Nipype, Boutiques, CWL, BIDS Apps)
```

Paper 1’s original seed list covered Layer 1 well and Layer 4 partly. It under-weighted Layer 2 (WINGS, APE, EDAM) and missed three 2026 **direct** competitors in Layer 3–4: **Coala**, **Nipoppy MCP**, and **NeuroClaw**.

---

## 3. Layer 1 — executable descriptors (the strongest baseline)

These systems already give agents typed inputs, containers, and invocation checks. SciCap must treat them as the control condition, not as missing infrastructure.

### 3.1 Nipype (Gorgolewski et al., 2011)

Typed Python interfaces, workflow DAGs, execution plugins, and provenance. `nipype2boutiques` already exports Nipype interfaces to Boutiques JSON, including FSL descriptor corpora. **SciCap must not rebuild Nipype.** Use it as an import source and as a typed-interface baseline.

### 3.2 BIDS and BIDS Apps (2016, 2017)

Dataset layout, sidecar metadata, and a portable app invocation pattern (`/bids /out participant`). fMRIPrep is the mature-pipeline exemplar, not a thing to reimplement. The **BIDS Apps execution specification** goes further: machine-readable input descriptors with types, choices, groups, and constraints (all-or-none, mutually exclusive, one-required). That is already a command contract for neuroimaging apps.

### 3.3 Boutiques (Glatard et al., 2018) — essential counterexample

JSON descriptors with name, version, description, command-line template, container image **and hash**, inputs (String/File/Flag/Number), input groups, outputs, error codes, DOI/URL, and invocation-schema validation. Intentionally **no workflow language** and **no ontology**. Tags exist (`domain:neuroinformatics`) but are free-form. Used by CBRAIN and, later, Nipoppy.

Boutiques already does: identity, CLI binding, container pinning, syntactic validation, publication.

Boutiques does **not** first-class: reference space, atlas identity, modality as a scientific type, units, QC obligations, or “abstain if precondition missing.”

### 3.4 CWL

CommandLineTool + Workflow, SALAD validation, Docker/Apptainer, richer types than Boutiques, and optional semantic annotations. WorkflowHub encourages Abstract CWL **with EDAM topic/operation annotations**. CWL is the closest “typed scientific tool contract” in production use.

### 3.5 What Layer 1 implies

If SciCap’s paper is “we wrote a JSON schema for tools and an MCP wrapper,” reviewers will cite Boutiques + CWL + Coala and reject. The intervention has to be the **scientific fields**, measured incrementally.

---

## 4. Layer 2 — semantic services and ontology-aware composition

This is the lineage Paper 1’s blueprint already flagged (OWL-S / SAWSDL) and that must be in the related-work table.

### 4.1 OWL-S (2004)

Service **Profile / Model / Grounding**. Functional attributes are IOPE: inputs, outputs, **preconditions**, results. That is the ancestor of SciCap’s “scientific capability contract.” OWL-S failed to become the industrial default because of complexity and top-down modeling — a warning, not a license to ignore it.

### 4.2 SAWSDL / WSDL-S

Bottom-up semantic annotations on existing interface documents. Closer to what SciCap should do: **annotate Boutiques/CWL**, do not replace them.

### 4.3 WINGS (Gil et al.)

The closest historical scientific system. Workflow representations carry **semantic constraints on datasets and components**. WINGS selects components, datasets, and parameters; rejects invalid combinations; propagates metadata to products; uses OWL/RDF/SPARQL. This is “scientific contracts for workflow design” in 2011-era form.

**Positioning.** SciCap is not WINGS. WINGS composes workflows. SciCap (Paper 1) evaluates **agent discovery and invocation**. But you cannot claim “scientific metadata for tools is new.” You can claim it was never isolated as an agent-facing intervention against modern descriptor/MCP baselines.

### 4.4 Kepler semantic types (Ratcliffe et al.; Bowers et al.)

OWL-typed operators and data; detect incompatible bindings; insert shims (unit conversion, interpolation). Directly anticipates “file type matches, scientific type does not.”

### 4.5 EDAM, bio.tools, Galaxy, APE

- **EDAM**: Topic, Operation, Data, Format taxonomies for life-science tools.
- **bio.tools**: large EDAM-annotated tool registry.
- **Galaxy**: `xref` to bio.tools; EDAM topics/operations on wrappers.
- **APE** (Kasalica et al., 2020): SAT-based workflow synthesis from an OWL domain ontology + bio.tools-style JSON annotations; export to CWL/Snakemake.

A 2025–2026 annotation study even built EDAM ground truth that **includes neuroimaging tools** (44 tools, 532 annotations across seven domains including neuroimaging).

**Positioning.** Scientific tool annotation at registry scale exists. Neuroimaging lacks an EDAM-equivalent that first-classes **space, atlas, and transform direction**. That is a more honest gap than “no one annotates tools.”

### 4.6 SciToolAgent and SciToolKG (Ding et al., *Nature Computational Science*, 2025)

LLM planner/executor plus a **scientific tool knowledge graph** encoding dependencies, prerequisites, and compatibility across biology, chemistry, and materials. SciToolEval: 531 tasks (152 single-tool, 379 multi-tool). Safety-checking module. Follow-on **SciToolAgent-Evo** (2026 preprint) adds ontology-aware open-world tool acquisition and OpenSciToolBench (900 tasks).

**Positioning.** This is the strongest *computational* competitor to “capability contracts help agents pick tools.” Domain is not neuroimaging; graph is not an inspectable, versioned, LLM-independent contract library. Still: if SciCap only shows that a knowledge graph of tools helps selection, SciToolAgent already published that in Nat Comput Sci.

---

## 5. Layer 3 — agent transport and catalogs

### 5.1 MCP and OpenAPI

Transport and JSON Schema for tools. Not scientific meaning. Paper 1 is correct to use MCP as the **common pipe** across conditions.

### 5.2 Coala (Hu et al., *Bioinformatics*, 26 August 2026) — blocker for the adapter claim

Command-line LLM-agent Adapter. Generic MCP server **parses CWL and exposes tools as MCP schemas**. Containerized execution via `cwltool` / Docker / Apptainer. “Tool definitions as data rather than code.” Just-in-time tool retrieval to avoid context pollution.

This **is** SciCap’s proposed adapter architecture, already published, for CWL rather than for a new contract language. 26 October 2026 check: *Bioinformatics* volume **42**, issue **9**, article **btag641**; site https://coala.info and https://github.com/coala-info/coala still describe CWL parse → MCP schema → containerized run. Coala does not return `ALLOW`/`REJECT`/`ABSTAIN` on space or atlas.

**Required response.** Import CWL/Boutiques via Coala-like mapping. Do not present an MCP adapter as the contribution. If you implement adapters, cite Coala as prior art and compete on **what extra fields** the agent sees.

### 5.3 Nipoppy and Nipoppy MCP (Brainhack 2026) — blocker for “first neuroimaging MCP catalog”

Nipoppy: BIDS-extended dataset protocol, Boutiques pipeline descriptors, Apptainer, processing-status tracking.  
Nipoppy MCP resources already include:

- `nipoppy://pipelines/{name}/{version}/descriptor` — the **Boutiques descriptor**
- dataset manifest, BIDS description, curation/processing status, pipeline config

**Required response.** Nipoppy MCP is the neuroimaging-native “catalog + Boutiques + MCP” system. SciCap must either build on it or show a measured gain from scientific fields **beyond** exposing Boutiques over MCP.

26 October 2026 check: Nipoppy **0.4.6** (2 April 2026) still runs Boutiques via `bosh exec launch` / simulate. OHBM BrainHack 2026 [#72](https://github.com/ohbm/hackathon2026/issues/72) is about *authoring* Boutiques descriptors from argparse, not about scientific invoke legality. Dataset **status** is not “this T1w is in the wrong space” or “DK labels declared as DKT.”

### 5.4 ToolUniverse (Zitnik lab, 2025–2026)

2,700+ scientific tools (July 2026 count) via Python, HTTP, and MCP. Tool Finder (keyword / embedding / LLM), Tool Caller with validated inputs, Tool Composer, human review before registering generated tools. Evaluated as improving agent scientific-task performance.

**Required response.** Scale of catalog and MCP exposure is not SciCap’s novelty. ToolUniverse is general scientific tools, not neuroimaging spatial contracts.

### 5.5 Paper2Agent (Miao et al., *Nature*, 16 September 2026)

Papers and code → validated MCP servers, tested against reference outputs, locked for reproducibility. Multi-paper MCP collaboration. Adjacent: paper-to-agent, not a maintained scientific tool catalog. Still kills “we made tools agent-accessible via MCP.”

26 October 2026 check: journal record unchanged (16 September 2026). Nature news DOI [10.1038/d41586-026-02899-2](https://doi.org/10.1038/d41586-026-02899-2) describes the same system. Public MCP examples listed by the authors (AlphaGenome, Scanpy, TISSUE) are not neuroimaging capability contracts.

---

## 6. Layer 4 — agentic science systems

### 6.1 Balis et al., 2026 (arXiv:2604.21910)

Natural-language research question → structured intent (LLM) → **deterministic** workflow DAG. Domain **Skills** (markdown) encode vocabulary mappings, parameter constraints, and optimization. On 150 queries, Skills raised full-match intent accuracy 44% → 83%. Human approval gates. Kubernetes execution.

**Positioning.** Closest “intent + domain knowledge + deterministic generation” paper. SciCap must not be another skill prompt. The differentiator is an **inspectable, typed, reusable contract** with field-level ablations — if those fields beat skill-style prose under an equal information budget.

### 6.2 NeuroClaw / NeuroDiscovery (Wang et al., arXiv:2604.24696, 27 April 2026)

Domain-specialized multi-agent system for **executable, reproducible neuroimaging**. Grounds planning in BIDS metadata and dataset semantics (organization, compliance, modality, preprocessing stage). Three-tier skill hierarchy. Environment pinning, Docker, audit traces. **NeuroBench**: system-level benchmark for executability, artifact validity, reproducibility readiness (later expanded to ~100 tasks / processing + model training).

**Positioning.** Highest neuroimaging-agent overlap with Papers 1 and 3. Skills + BIDS grounding, not a public capability-contract library with controlled descriptor ablations. Must appear in the related-work matrix. Do not claim “first agent that uses BIDS semantics.”

26 October 2026 check: arXiv HTML v2/v3 and the GitHub project [CUHK-AIM-Group/NeuroDiscovery](https://github.com/cuhk-aim-group/neuroclaw) document a rename/expansion (NeuroDiscovery v1.0.0, 15 September 2026 on the project README: knowledge graph, hypothesis generator, NeuroRuntime). That is still early-bound dataset/skill knowledge plus an execution harness. It does not isolate late binding of `space`/`atlas` or a three-valued invoke decision. No separate journal DOI for NeuroDiscovery was found; do not invent one.

---

## 7. Layer 5 — neuroimaging semantics already exist as *data* models

The fields SciCap wants to add to **tools** already exist for **datasets and results**.

| Semantic object | Where it already lives |
|---|---|
| Modality, suffix, entities | BIDS |
| `space-`, `tpl-`, `atlas-`, transforms `from-T1w_to-MNI` | BIDS Derivatives |
| Coordinate space, voxel-to-world, MNI vs subject | **NIDM** `Coordinate Space` |
| Provenance of transforms | BEP028 BIDS-prov (NIDM-compatible, still a proposal) |
| Processing status across participants | Nipoppy |

**Implication.** SciCap should **bind tool contracts to BIDS/NIDM terms**, not invent a parallel vocabulary. The candidate gap is that **tool descriptors** (Boutiques/CWL/MCP) usually do not carry those terms, so an agent can pick a syntactically valid tool that is scientifically illegal for the input’s space or atlas.

---

## 8. Layer 6 — evaluation priors

Use these for method, not as neuroimaging validity oracles.

| Work | Lesson for SciCap |
|---|---|
| ToolBench / ToolLLM | Large API pools; selection is the hard step |
| Gorilla / APIBench / BFCL (v4 updated Apr 2026) | Function-call correctness ≠ scientific correctness |
| TOOLRET (ACL Findings 2025) | 7.6k tasks / 43k tools; retrieval quality drives pass rate |
| ScienceAgentBench (ICLR 2025) | Expert-validated scientific tasks; 2026 verified split |
| SciAgentArena (2026) | Interactive multi-domain science; weak domain-semantic scoring |
| SciAgentGym / SciAgentBench (Shen et al., 2026) | 1,780 scientific tools; long-horizon tool use degrades |
| SciToolEval | Tool-path accuracy + answer accuracy, single vs multi-tool |
| NeuroBench (NeuroClaw) | Neuroimaging executability / artifact checks — Paper 3 overlap |

SciCap’s evaluation must remain **paired, descriptor-matched, scientifically scored**. Do not use BFCL-style AST match as the primary endpoint.

---

## 9. Field-by-field coverage (the decisive matrix)

Proposed SciCap contract fields versus what already exists. “Gap” means *not first-class on a widely used tool descriptor that an agent would see*, not “the science does not exist.”

| SciCap field group | Covered by | Residual gap? |
|---|---|---|
| Identity (id, version, license, citation) | Boutiques, CWL, bio.tools, WorkflowHub | No |
| Task taxonomy / intended use | EDAM Topic/Operation, Boutiques tags, Galaxy, BIDS analysis-level | Weak neuroimaging taxonomy; do not invent a competing ontology |
| Modality | BIDS; not first-class in Boutiques/CWL | **Yes — on the tool contract** |
| Format / file kind | Boutiques File, CWL types, EDAM Format | No |
| Reference space | NIDM, BIDS `space-`/`tpl-` | **Yes — on the tool contract** |
| Atlas / label ontology | BIDS `atlas-`; FreeSurfer/MRtrix docs | **Yes — on the tool contract** |
| Units | NIDM voxel units; Kepler OWL types | **Yes — weakly specified on tools** |
| Preconditions / incompatibilities | OWL-S IOPE, WINGS, SciToolKG, Boutiques input groups (syntactic only) | **Yes — scientific preconditions** |
| Output interpretation / QC links | Sparse; pipeline reports exist but are not contract fields | **Yes** |
| Container digest / command | Boutiques `container-hash`, CWL DockerRequirement | No |
| Schema / fixture tests | Boutiques invocation schema, CWL tests, Paper2Agent | No |
| Provenance bundle | PROV, RO-Crate, CWLProv, NIDM, BIDS-prov | Reuse, do not replace |
| Approval / permission boundary | Balis gates, Gorilla GoEx, agent-safety work | **Yes — as a contract field** |
| Calibrated abstention | Rarely a first-class tool behavior | **Yes** |

**Honest unique-ish remainder:** space, atlas, scientific preconditions, QC obligations, permission/abstention — attached to an otherwise standard descriptor and **ablated**.

---

## 10. What would not be novel (do not write these sentences)

- “We introduce a machine-readable scientific tool descriptor.”
- “We expose neuroimaging tools to agents via MCP.”
- “We add containers, JSON Schema, and provenance.”
- “We use a knowledge graph so the agent can pick compatible tools.”
- “We convert papers or CLIs into agent tools.”
- “We are the first BIDS-aware neuroimaging agent.”
- “Typed interfaces for neuroimaging tools.” (Nipype, 2011)
- “Semantic constraints on scientific workflow components.” (WINGS)

---

## 11. Remaining testable claim

**Primary (keep).** On held-out neuroimaging intents, adding explicit scientific fields (modality, reference space, atlas, units, preconditions, QC/unsupported cases) to a descriptor that is otherwise information-matched to Boutiques/CWL/MCP **raises scientifically correct end-states and appropriate abstention**.

**Necessary controls, now sharper because of 2026 work:**

1. **Same transport:** MCP in the schema-only arm and the SciCap arm (Coala/Nipoppy pattern).
2. **Same executors and containers.**
3. **Length-matched prose** that states the same scientific facts in documentation, to kill “you just wrote more tokens.”
4. **Boutiques-native and CWL-native arms**, not a weakened strawman.
5. **Skill-document arm** (Balis/NeuroClaw style) if you want to claim typed contracts beat prompt skills.
6. **Field ablations** of space, atlas, preconditions, QC.
7. **Held-out tools** never shown in examples.
8. **Nipoppy MCP** as a real-world neuroimaging catalog baseline if installation is feasible.

If those comparisons are flat, SciCap is a useful annotation convention, not a methods paper. Publish software/JOSS or contribute fields upstream to Boutiques/CWL/Nipoppy.

---

## 12. Required experimental baselines (updated)

| Arm | Implement as | Isolates |
|---|---|---|
| A Documentation | Official readmes + allowed commands | Human docs |
| B Schema MCP | OpenAPI/MCP JSON Schema only | Generic agent tool use |
| C Boutiques / CWL | Real descriptors, Coala-style MCP exposure | Mature scientific CLIs |
| C2 Nipoppy MCP | Boutiques descriptors + BIDS dataset context | Best existing neuro catalog |
| D SciCap | C plus scientific fields | Incremental semantics |
| E Ablations | D minus one field group | Causal fields |
| F Length-matched prose | Scientific facts as text, same token budget | Representation vs wording |
| G Skills (optional) | Markdown skills with same facts | Typed contract vs Balis/NeuroClaw skills |

---

## 13. Work-by-work novelty matrix

| Work | Year | Layer | Threat | SciCap must add or test |
|---|---|---|---|---|
| OWL-S | 2004 | Semantic | Blocker for “IOPE is new” | Inspectable modern contract + agent RCT, not a new service ontology |
| SAWSDL | 2007 | Semantic | High | Annotation-on-existing-schema pattern |
| WINGS | 2011 | Semantic | Blocker for “semantic tool constraints” | Agent invocation, not workflow synthesis |
| Nipype | 2011 | Descriptor | Must-cite | Import traits; do not rebuild |
| Kepler OWL types | ~2012 | Semantic | High | Shim/type-mismatch lesson |
| BIDS | 2016 | Neuro data | Reuse | Bind contracts to BIDS terms |
| BIDS Apps | 2017 | Descriptor | Must-cite | App-level CLI contract |
| Boutiques | 2018 | Descriptor | **Blocker for new schema** | Scientific fields + measured agent gain |
| CWL | living | Descriptor | **Blocker for new schema** | Same; import via Coala-like adapter |
| EDAM / bio.tools / Galaxy | living | Semantic | High | Neuro-specific space/atlas, not another Topic/Operation list |
| APE | 2020 | Semantic | High | Paper 2 composition; Paper 1 stays at single-capability choice |
| fMRIPrep | 2019 | Pipeline | Adjacent | Exemplar, not a competitor |
| RO-Crate / PROV / CWLProv / WorkflowHub | living | Provenance | Reuse | Compatible receipts |
| NIDM / BIDS Derivatives | living | Neuro data | Reuse | Space/atlas vocabulary source |
| MCP / OpenAPI | living | Transport | Must-cite | Common pipe across arms |
| ToolBench / Gorilla / BFCL / TOOLRET | 2023–26 | Evaluation | Adjacent | Retrieval/call metrics only |
| ScienceAgentBench | 2025 | Evaluation | Adjacent | Annotation rigor |
| SciToolAgent / SciToolKG | 2025 | Sci agents | **High** | Neuro fields; inspectable contracts; descriptor-matched RCT |
| ToolUniverse | 2025–26 | Transport | **High** | Not a 2,700-tool catalog paper |
| Balis et al. | 2026 | Sci agents | **High** | Typed contracts vs Skills; equal info |
| Paper2Agent | 2026 | Transport | Blocker for “MCP from science artifacts” | Catalog + controlled metadata, not paper conversion |
| Coala | 2026 | Transport | **Blocker for MCP adapter** | Extra scientific fields only |
| Nipoppy MCP | 2026 | Neuro + transport | **Blocker for neuro MCP catalog** | Fields beyond Boutiques + dataset status |
| NeuroClaw / NeuroBench | 2026 | Neuro agents | **High** | Contract ablation vs BIDS-grounded skills |
| NeuroDiscovery (NeuroClaw follow-on repo) | 2026 | Neuro agents | **High** | Same object family; still not late-bound invoke |
| OHBM #72 Boutiques authoring | 2026 | Descriptor | Adjacent | Automates Boutiques JSON; no scientific predicates |
| SciToolAgent-Evo / OpenSciToolBench | 2026 | Sci agents | Adjacent | Open-world acquisition is out of scope |
| SciAgentGym | 2026 | Evaluation | Adjacent | Long-horizon tool use, not neuro validity |
| BIDS Apps execution spec | living | Descriptor | Must-cite | Do not duplicate app input groups |

---

## 14. Annotated seed bibliography (verified starting set)

Links checked as live search hits on 26 October 2026. Export into a citation manager and lock author/volume/page before submission.

### Standards and neuroimaging

1. Gorgolewski et al. (2011). Nipype. *Front Neuroinform*. https://doi.org/10.3389/fninf.2011.00013  
2. Gorgolewski et al. (2016). BIDS. *Sci Data*. https://doi.org/10.1038/sdata.2016.44  
3. Gorgolewski et al. (2017). BIDS Apps. *PLOS Comput Biol*. https://doi.org/10.1371/journal.pcbi.1005209  
4. Glatard et al. (2018). Boutiques. *GigaScience*. https://doi.org/10.1093/gigascience/giy016 — schema: https://github.com/boutiques/boutiques/blob/master/boutiques/schema/descriptor.schema.json  
5. Esteban et al. (2019). fMRIPrep. *Nat Methods*. https://doi.org/10.1038/s41592-018-0235-4  
6. Common Workflow Language. https://www.commonwl.org/user_guide/  
7. BIDS specification, derivatives, common principles. https://bids-specification.readthedocs.io/  
8. BIDS Apps execution specification. https://bids-standard.github.io/execution-spec/  
9. NIDM-Results Coordinate Space. https://nidm.nidash.org/specs/nidm-results_130.html  
10. BEP028 BIDS-prov. https://github.com/bids-standard/BEP028_BIDSprov  
11. Nipype `nipype2boutiques`. https://nipype.readthedocs.io/en/latest/api/generated/nipype.utils.nipype2boutiques.html  
12. Nipoppy. https://github.com/neurodatascience/nipoppy  
13. Nipoppy MCP (2026). https://github.com/nipoppy/mcp  

### Semantic services and composition

14. OWL-S. https://www.w3.org/submissions/OWL-S/  
15. SAWSDL / semantic scientific workflow survey. Zhao & Paschke (semantic-web-journal draft).  
16. WINGS. https://wings-workflows.org/about.html ; Gil et al., IEEE Intelligent Systems 2011.  
17. Ratcliffe et al. Semantic validation and correction of scientific workflows (Kepler/OWL).  
18. Kasalica et al. (2020). APE. https://pmc.ncbi.nlm.nih.gov/articles/PMC7304703/  
19. Perspectives on automated composition of workflows in the life sciences. https://pmc.ncbi.nlm.nih.gov/articles/PMC8573700/  
20. EDAM / bio.tools / Galaxy tool annotation. https://galaxy-iuc-standards.readthedocs.io/en/latest/best_practices/tool_xml.html  
21. WorkflowHub. https://arxiv.org/html/2410.06941 ; https://about.workflowhub.eu/  
22. RO-Crate. https://www.researchobject.org/ro-crate/specification  
23. W3C PROV-O. https://www.w3.org/TR/prov-o/  

### Agent transport and 2025–2026 systems

24. Model Context Protocol tools spec. https://modelcontextprotocol.io/specification/2025-06-18/server/tools  
25. OpenAPI. https://spec.openapis.org/oas/latest.html  
26. Hu et al. (2026). Coala. *Bioinformatics* 42(9):btag641. https://doi.org/10.1093/bioinformatics/btag641 — https://coala.info — https://github.com/coala-info/coala  
27. Miao et al. (2026). Paper2Agent. *Nature*. https://doi.org/10.1038/s41586-026-11044-y — news: https://doi.org/10.1038/d41586-026-02899-2  
28. Balis et al. (2026). From Research Question to Scientific Workflow. https://arxiv.org/abs/2604.21910  
29. Ding et al. (2025). SciToolAgent. *Nat Comput Sci*. https://doi.org/10.1038/s43588-025-00849-y — https://arxiv.org/abs/2507.20280  
30. SciToolAgent-Evo (2026). https://arxiv.org/html/2607.28692v1  
31. ToolUniverse (2025–26). https://arxiv.org/html/2509.23426 — https://aiscientist.tools  
32. Wang et al. (2026). NeuroClaw. https://arxiv.org/abs/2604.24696 — follow-on repo branding: https://github.com/cuhk-aim-group/neuroclaw  

### Agent evaluation

33. Jimenez et al. (2024). SWE-bench. ICLR.  
34. Patil et al. Gorilla / APIBench; BFCL v4 (updated 12 Apr 2026). https://gorilla.cs.berkeley.edu/leaderboard.html  
35. Qin et al. ToolLLM / ToolBench.  
36. Shi et al. (2025). TOOLRET. ACL Findings. https://aclanthology.org/2025.findings-acl.1258.pdf  
37. Chen et al. (2025). ScienceAgentBench. ICLR.  
38. Liu et al. (2026). SciAgentArena. https://arxiv.org/abs/2606.12736  
39. Shen et al. (2026). SciAgentGym. https://proceedings.mlr.press/v306/shen26aa.html  
40. Glickman (2026). Nature news on Paper2Agent. https://doi.org/10.1038/d41586-026-02899-2  
41. OHBM BrainHack 2026 #72. Automated Boutiques descriptor creation. https://github.com/ohbm/hackathon2026/issues/72  
42. Singh, Gopalan, Narayanan (2026). Silent Failures in Agent–Tool Interaction. https://arxiv.org/abs/2609.26836  

---

## 15. Open questions before the novelty claim is frozen

1. Does any Boutiques or CWL corpus already encode `space` / `atlas` as custom tags at a rate that makes SciCap fields redundant? **Audit real descriptors.**
2. Does the BIDS Apps execution spec already have extension points for scientific types? If yes, extend it rather than fork.
3. Can Coala ingest Boutiques as well as CWL, or only CWL? If only CWL, a Boutiques→MCP path may still be engineering, not science.
4. How much of NeuroClaw’s gain is BIDS metadata versus skill prompts versus environment pinning? Read the paper fully before designing arm G.
5. Is NIDM still maintained enough to be the space vocabulary, or should contracts speak BIDS entity language only?
6. What fraction of SciCap’s proposed fields can be expressed as CWL `format` + EDAM-style identifiers without a new schema version?

---

## 16. Immediate next actions

1. Build a **descriptor-field spreadsheet**: Boutiques 0.5, CWL CommandLineTool, BIDS App execution spec, Nipype traits, SciCap v0.1 — one row per field.
2. Download 20 public Boutiques neuroimaging descriptors (Nipoppy / boutiques-nipype-fsl) and mark which scientific fields are already present as tags or descriptions.
3. Read Coala, NeuroClaw, SciToolAgent, and Balis end-to-end; update this matrix with page-level quotes.
4. Decide: **extend Boutiques/CWL** with a SciCap profile, or keep a parallel schema with lossless import/export. Reviewers will prefer a profile.
5. Rewrite Paper 1 §1.3 so the contribution sentence starts from “incremental scientific fields + controlled agent evaluation,” not “a capability contract.”

---

## 17. Go-gate note (methods §5, re-read 26 October 2026)

Methods §5: if Boutiques / CWL / Nipoppy already decide the gold cases, stop and offer fields upstream.

**They do not.** On 26 October 2026:

| Gold case | Boutiques invocation schema | Nipoppy MCP |
|---|---|---|
| Complete T1w, space present | File/type valid → would *run*, not `ALLOW` | Descriptor + status, no scientific bind |
| DK labels declared as DKT | Not a Boutiques input-group check | Not a processing-status resource |
| `space` omitted | Omitted sidecar is not an invocation-schema miss | Status ≠ insufficient evidence |
| Wrong modality (DWI as T1w) | A `File` input still validates | Catalog does not type-check modality vs capability |

Therefore the v0 invoke decision is not already owned by those systems. Implement `scicap invoke` as a **profile + decision**. Do **not** add an MCP adapter or the full M3 arm matrix until this gate is re-read after a real Boutiques-descriptor field audit (open question 1).

---

**Decision for the research program.** Start SciCap as a **profile and evaluation**, not as a new ecosystem. If the RCT is positive, the methods paper is “scientific fields on tool contracts change agent neuroimaging decisions.” If it is negative, the public artifact is still useful annotations — and should be offered upstream.
