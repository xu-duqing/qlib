# Comparison runs archive

This directory stores saved comparison outputs for repeated benchmark experiments, especially for retail-style parameter changes such as smaller `topk` values.

## Layout

Each run should create a timestamped subdirectory such as:

```text
examples/benchmarks/comparison_runs/20260420_171500_csi1000_recent5y_topk5/
```

Recommended contents:

- `linear_stdout.log`
- `lightgbm_stdout.log`
- `summary.md`
- optional copied configs used in the run

## Current focus

- Universe: `csi1000`
- Time window: recent 5 years
- Comparison: `Linear` vs `LightGBM`
- Retail-style backtest setting: `topk=5`, `n_drop=1`
