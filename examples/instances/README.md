# Invoke instances

JSON sidecars for `scicap invoke`. No NIfTI bytes.

Wave-1 copies of `shared/fixtures/`: `complete_t1w.json`, `missing_space.json`, `dk_as_dkt.json`, `wrong_modality.json`.

Added for the five-capability slice: `complete_bids.json`, `complete_dkt.json`, `wrong_space_mni.json`.

```text
scicap invoke packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml \
  --instance examples/instances/complete_t1w.json
```
