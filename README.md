# SciCap

Late-bound capability contracts. `scicap invoke` returns **ALLOW**, **REJECT**, or **ABSTAIN**. Missing `space` is never filled in.

Not a new Boutiques/CWL/MCP. Coala and Nipoppy already own adapters.

## Install

```bash
pip install -e .
```

Python 3.11+. No model API.

## Use

```bash
scicap invoke packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml \
  --instance examples/instances/complete_t1w.json
scicap invoke packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml \
  --instance examples/instances/missing_space.json
```

`--approve` records approval only. It does not pull a container.

## Tests

```bash
pytest tests
```

## Docs

- [Methods](docs/SciCap_Methods.md) (M1–M4)
- [Literature map](docs/SciCap_Literature_Map.md)
- [Methods trace](docs/METHODS_TRACE.md)

Apache-2.0. No NIfTI or PHI in this repo.
