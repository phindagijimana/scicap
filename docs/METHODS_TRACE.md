# SciCap methods trace (wave 2)

Paper 1 · 26 October 2026 · wiring document, **no results claimed**

Locked protocol: [`SciCap_Methods.md`](SciCap_Methods.md) (M1–M4). This file cites what the public tool already owns versus the residual SciCap implements. It does not replace the methods memo. It does not invent M5. It does not add an MCP adapter.

**Blockers for adapter / novelty claims (do not reimplement).** Coala (Hu et al., *Bioinformatics* 2026, [10.1093/bioinformatics/btag641](https://doi.org/10.1093/bioinformatics/btag641)) already maps CWL → MCP. Nipoppy MCP already exposes Boutiques descriptors plus dataset status. Paper2Agent (Miao et al., *Nature* 2026, [10.1038/s41586-026-11044-y](https://doi.org/10.1038/s41586-026-11044-y)) already converts papers/code to MCP servers. Boutiques (Glatard et al., 2018, [10.1093/gigascience/giy016](https://doi.org/10.1093/gigascience/giy016)) already owns identity, CLI template, container pin, and invocation-schema checks. SciCap is a **profile plus invoke decision** on that substrate.

| Method | Public tool reused | Literature residual | Test |
|---|---|---|---|
| M1 | Boutiques descriptor + BIDS sidecar names | bind `space`/`atlas`/`modality` at invoke; capability ≠ dataset | `test_methods.py` |
| M2 | — | three-valued decision; Boutiques has no ABSTAIN | `test_invoke.py` (keep) |
| M3 | Boutiques-only descriptor | same facts, no SciCap fields in baseline | `test_public_boutiques.py` |
| M4 | ToolUniverse silent-failure prior | `qc_status` / `unsupported_cases`; exit 0 ≠ science | `test_methods.py` |

## Row notes

**M1.** Boutiques inputs are `File` / `String` / `Number` / `Flag`. BIDS already names `space-`, `atlas-`, and modality/suffix on **data**. The residual is late binding of those names onto the capability at invoke time. NeuroClaw skills that bake a dataset (`hcp-skill`) are out of scope.

**M2.** Boutiques invocation schema is binary: required typed inputs present → invocable. Coala and Nipoppy MCP inherit that binary. They do not return `ALLOW` / `REJECT` / `ABSTAIN`. Missing `space` is not an invocation miss. Comment in `packages/scicap-core/invoke.py`: `# M2 residual vs Boutiques:`.

**M3.** `packages/scicap-neuro/boutiques/neuro.t1.hippocampal_volumes.boutiques.json` is the matched Boutiques-only encoding (arm C). Same T1w file fact; no SciCap keys. The `boutiques` PyPI package is not installed here; the baseline implements the recorded 0.5 invocation-schema contract from that JSON.

**M4.** ToolUniverse silent-failure audit ([arXiv:2609.26836](https://arxiv.org/abs/2609.26836)) is the prior: a zero exit is not a scientific success. Residual lives on the capability YAML (`unsupported_cases`, `qc_required`, `qc_status`, `output_completeness`, `interpretation_limits`) and on the invoke result. v0 never executes the container.

## Go-gate (methods §5)

Boutiques does **not** already decide the four v0 cases as `ALLOW` / `REJECT` / `ABSTAIN`. File/type checks accept complete T1w, omitted `space`, DK-as-DKT, and DWI-as-File. SciCap invoke splits those four. Offer fields upstream only if a later descriptor audit shows Boutiques/Nipoppy already encode the predicates.

## Field audit (wave 3)

Re-checked against the Boutiques-only descriptor (`packages/scicap-neuro/boutiques/neuro.t1.hippocampal_volumes.boutiques.json`) and the recorded-or-real baseline (`packages/scicap-core/boutiques_baseline.py`). The `boutiques` PyPI package is not installed in this environment; the baseline stays `baseline_mode: recorded`. Boutiques File/type checks still accept complete T1w, omitted `space`, DK-as-DKT, and DWI-as-File. They still do not return `ALLOW` / `REJECT` / `ABSTAIN`. Nipoppy MCP is not present in this tree and was not found to encode `space` / `atlas` as invoke decisions. The four v0 cases remain a SciCap residual. Fields are not offered upstream.
