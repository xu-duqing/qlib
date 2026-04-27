# CSI1000 recent usable topk=5 comparison

Run dir: `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5`

| Model | Window | Exit | IC | ICIR | Rank IC | Rank ICIR | annualized_return(cost) | information_ratio(cost) | max_drawdown(cost) | Log |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| linear | recent2y | 0 | -0.0002082031847114145 | -0.0013582015765295562 | 0.039427583246114756 | 0.22169908516176762 | -0.374312 | -1.672011 | -0.105397 | `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5/linear_recent2y_stdout.log` |
| lightgbm | recent2y | 0 | 0.006716974791382605 | 0.06012170848377766 | 0.028901850549687743 | 0.24403944005969347 | -0.636658 | -2.821270 | -0.253364 | `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5/lightgbm_recent2y_stdout.log` |
| linear | recent3y | 0 | 0.0004800064049762163 | 0.00290014898731162 | 0.047635822631639055 | 0.26091990677646937 | -0.453494 | -1.944058 | -0.108688 | `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5/linear_recent3y_stdout.log` |
| lightgbm | recent3y | 0 | 0.00887121257192031 | 0.07299444503080597 | 0.02726964934798768 | 0.19962259137033392 | -1.075264 | -4.653375 | -0.308011 | `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5/lightgbm_recent3y_stdout.log` |
