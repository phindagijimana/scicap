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

**M3.** `packages/scicap-neuro/boutiques/neuro.t1.hippocampal_volumes.boutiques.json` is the matched Boutiques-only encoding (arm C). Same T1w file fact; no SciCap keys. Wave 5 calls installed Boutiques when `import boutiques` works (`baseline_mode: live`); otherwise the recorded 0.5 invocation-schema contract (`baseline_mode: recorded`).

**M4.** ToolUniverse silent-failure audit ([arXiv:2609.26836](https://arxiv.org/abs/2609.26836)) is the prior: a zero exit is not a scientific success. Residual lives on the capability YAML (`unsupported_cases`, `qc_required`, `qc_status`, `output_completeness`, `interpretation_limits`) and on the invoke result. v0 never executes the container.

## Go-gate (methods §5)

Boutiques does **not** already decide the four v0 cases as `ALLOW` / `REJECT` / `ABSTAIN`. File/type checks accept complete T1w, omitted `space`, DK-as-DKT, and DWI-as-File. SciCap invoke splits those four. Offer fields upstream only if a later descriptor audit shows Boutiques/Nipoppy already encode the predicates.

## Field audit (wave 3)

Re-checked against the Boutiques-only descriptor (`packages/scicap-neuro/boutiques/neuro.t1.hippocampal_volumes.boutiques.json`) and the recorded-or-real baseline (`packages/scicap-core/boutiques_baseline.py`). Wave 3 ran without the PyPI package. Wave 5 (below) updates the install state.

## Wave 5 (toward production)

`pip install boutiques` from PyPI succeeded in this environment: `boutiques` 0.5.33 imports. The baseline calls `boutiques.validator.validate_descriptor` and `boutiques.invocationSchemaHandler.validateSchema` on `packages/scicap-neuro/boutiques/neuro.t1.hippocampal_volumes.boutiques.json` (no container launch, no image pull) and sets `baseline_mode: live`. If `import boutiques` fails, the same module keeps `baseline_mode: recorded`.

Installed Boutiques 0.5 input types remain `String` / `File` / `Flag` / `Number`. The shipped schema has no `atlas`, `ALLOW`, `REJECT`, `ABSTAIN`, `qc_status`, or `modality` keys. Occurrences of the word “space” are list-separator defaults and `disk-space`, not BIDS reference space. Live File/invocation checks still accept complete T1w, omitted `space`, DK-as-DKT, and DWI-as-File. They still do not return `ALLOW` / `REJECT` / `ABSTAIN`. Nipoppy MCP is not present in this tree. Fields are not offered upstream. Pytest uses JSON sidecars only; OpenNeuro bytes are not downloaded.

No confirmatory rates are claimed.

## Wave 6 (fetched S0)

Public T1w bytes are on disk at `shared/data/external/ds000003/sub-01/anat/sub-01_T1w.nii.gz` after `shared/scripts/fetch_s0.py --i-accept-public-data` (OpenNeuro S3). The file is gzip (`\x1f\x8b`), about 5.7 MB, not a 140-byte git-annex pointer. `packages/scicap-core/s0.py` locates that path and treats annex/LFS stand-ins as absent. `benchmarks/pilot-v0/tasks.yaml` now includes tasks that **point at that path**. Bytes are not copied into `01_SciCap/`. `bytes_in_git` stays false. Pytest does not download. Holdout stays empty of tasks.

SciCap still returns `ALLOW` / `REJECT` / `ABSTAIN`. The Boutiques-only baseline still does not emit those tokens. The container is not executed. No confirmatory rates are claimed.
