# Microcap strict recent benchmark export

This directory tracks the benchmark result summary exported from local MLflow runs under `mlruns/`.

## Why this exists

`mlruns/` is ignored by git in this repo, so benchmark results are exported here as a tracked, compact summary instead of committing the raw MLflow run directories.

## Source MLflow experiment

- Local MLflow root: `qlib-felix/mlruns/`
- Experiment id: `326446173096931478`

## What was found

For `microcap_strict_recent`, the local MLflow records currently show **two Linear runs** and **no successful LightGBM microcap_strict_recent run with full metrics/artifacts**.

Detected microcap-strict run ids:

- `05f867cae0d24e399ff86008ce94ecbf` — Linear — command recorded, but no metrics/artifacts beyond code snapshot files
- `923acc7cdde743808c16eacb2afdc0bd` — Linear — command recorded, but no metrics/artifacts beyond code snapshot files

## Notes

- These runs only contain minimal artifact files such as `code_diff.txt`, `code_cached.txt`, `task`, and `code_status.txt`.
- They do **not** contain the usual exported benchmark files like `pred.pkl`, `portfolio_analysis/*`, or `sig_analysis/*`.
- They also do **not** contain recorded MLflow metrics like `IC`, `ICIR`, annualized return, or information ratio.
- Therefore, there is currently no reliable benchmark metric block to export for `microcap_strict_recent` itself.

## Reference benchmark runs found in the same experiment

These are not microcap-strict runs, but they are the completed reference runs currently present in local MLflow:

- `350f036dd6b24c9bb74acf797d98055e` — Linear — `workflow_config_linear_Alpha158_csi1000.yaml`
- `598612866138484685245914a1e5d882` — Linear — `workflow_config_linear_Alpha158_csi1000_recent5y.yaml`
- `6f7a6bb8936c4e3082e0c2ffc1b93d26` — Linear — `workflow_config_linear_Alpha158_csi1000_recent5y_topk5.yaml`
- `41e9f2955d3f43c8922e4d23758fef3b` — LightGBM — `workflow_config_lightgbm_Alpha158_csi1000_recent5y.yaml`
- `f12dd9b441c54246abeabee9305ebef8` — LightGBM — `workflow_config_lightgbm_Alpha158_csi1000_recent5y_topk5.yaml`

See `runs_summary.json` for the extracted machine-readable details.
