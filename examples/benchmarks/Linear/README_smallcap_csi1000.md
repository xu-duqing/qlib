# Small-cap Linear example (CSI1000)

This example is a practical small-cap stock pool variant for qlib using the CSI1000 universe and a Linear model.

## Why this exists

Qlib's default examples often target broader institutional-style universes such as CSI300 or CSI500. For a more small-cap oriented experiment, this config switches the universe to `csi1000`, which is a more suitable approximation of a small-cap stock pool in the public qlib CN dataset.

## Config

- File: `workflow_config_linear_Alpha158_csi1000.yaml`
- Universe: `csi1000`
- Benchmark: `SH000852`
- Model: `LinearModel(estimator=ridge)`
- Train: `2015-01-01 ~ 2017-12-31`
- Valid: `2018-01-01 ~ 2018-12-31`
- Test: `2019-01-01 ~ 2020-08-01`

## Run

```bash
python qlib/cli/run.py examples/benchmarks/Linear/workflow_config_linear_Alpha158_csi1000.yaml
```

## Note

This is still a research/backtest example, not a small-account execution-ready strategy. It uses a small-cap-oriented universe proxy (`csi1000`), but practical retail execution constraints such as lot size, concentrated holdings, and minimum-fee distortion still need a separate execution layer.
