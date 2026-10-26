# SciCap

`scicap invoke` returns **ALLOW**, **REJECT**, or **ABSTAIN**. Missing `space` is never filled in.

Not a new Boutiques, CWL, or MCP.

## Go

```bash
pip install git+https://github.com/phindagijimana/scicap.git
scicap invoke packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml \
  --instance examples/instances/complete_t1w.json
```

```python
from scicap import invoke
invoke("cap.yaml", "instance.json")
```

Python 3.11+. No model API. `--approve` records approval only — no container pull. If `boutiques` is installed, the public baseline is `baseline_mode: live`; otherwise `recorded`. Pytest does not download OpenNeuro.

Optional agent transport (same `invoke`; not a Coala/Nipoppy product): `python -m scicap.mcp`

```bash
pytest tests
```

[Methods](docs/SciCap_Methods.md) · Apache-2.0 · no NIfTI or PHI
