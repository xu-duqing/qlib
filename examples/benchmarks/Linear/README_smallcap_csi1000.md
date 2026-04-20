# Small-cap Linear example (CSI1000)

This example is a practical small-cap stock pool variant for qlib using the CSI1000 universe and a Linear model.

## Why this exists

Qlib's default examples often target broader institutional-style universes such as CSI300 or CSI500. For a more small-cap oriented experiment, this config switches the universe to `csi1000`, which is a more suitable approximation of a small-cap stock pool in the public qlib CN dataset.

## Configs

### 1) Historical baseline
- File: `workflow_config_linear_Alpha158_csi1000.yaml`
- Universe: `csi1000`
- Benchmark: `SH000852`
- Model: `LinearModel(estimator=ridge)`
- Train: `2015-01-01 ~ 2017-12-31`
- Valid: `2018-01-01 ~ 2018-12-31`
- Test: `2019-01-01 ~ 2020-08-01`

### 2) Recent 5-year version
- File: `workflow_config_linear_Alpha158_csi1000_recent5y.yaml`
- Universe: `csi1000`
- Benchmark: `SH000852`
- Model: `LinearModel(estimator=ridge)`
- Full range: `2021-01-01 ~ 2026-04-17`
- Train: `2021-01-01 ~ 2023-12-31`
- Valid: `2024-01-01 ~ 2024-12-31`
- Test: `2025-01-01 ~ 2026-04-17`

## Run

```bash
python qlib/cli/run.py examples/benchmarks/Linear/workflow_config_linear_Alpha158_csi1000.yaml
python qlib/cli/run.py examples/benchmarks/Linear/workflow_config_linear_Alpha158_csi1000_recent5y.yaml
python qlib/cli/run.py examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158_csi1000_recent5y.yaml
```

## Recent 5-year comparison target

For direct comparison on the same `csi1000` small-cap-oriented universe and the same recent 5-year split:

- Linear: `examples/benchmarks/Linear/workflow_config_linear_Alpha158_csi1000_recent5y.yaml`
- LightGBM: `examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158_csi1000_recent5y.yaml`

## Note

This is still a research/backtest example, not a small-account execution-ready strategy. It uses a small-cap-oriented universe proxy (`csi1000`), but practical retail execution constraints such as lot size, concentrated holdings, and minimum-fee distortion still need a separate execution layer.
