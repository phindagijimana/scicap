# Invoke instances

JSON sidecars for `scicap invoke`. No NIfTI bytes.

Wave-1 copies of `shared/fixtures/`: `complete_t1w.json`, `missing_space.json`, `dk_as_dkt.json`, `wrong_modality.json`.

Added for the five-capability slice: `complete_bids.json`, `complete_dkt.json`, `wrong_space_mni.json`.

Wave 6 S0 pointers (no NIfTI in this folder): `s0_public_t1w.json`, `s0_public_missing_space.json`, `s0_public_bids.json` point at `../shared/data/external/ds000003/`.

```text
scicap invoke packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml \
  --instance examples/instances/complete_t1w.json
```
