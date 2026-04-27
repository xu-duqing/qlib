# Qlib Benchmark Report

后续运行结果统一记录在这里。

| 运行标识 | 股票池 | 模型 | IC | ICIR | Rank IC | Rank ICIR | 带成本年化超额 | 带成本信息比率 | 带成本最大回撤 | 日志 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 20260422_145426_csi1000_recent5y_topk5 | csi1000_recent5y | Linear | 0.00813561206637587 | 0.05103456851357552 | 0.055099528718901766 | 0.30387853311865815 | -0.020000 | -0.103538 | -0.245820 | `examples/benchmarks/comparison_runs/20260422_145426_csi1000_recent5y_topk5/linear_stdout.log` |
| 20260422_145426_csi1000_recent5y_topk5 | csi1000_recent5y | LightGBM | 0.01856549811596614 | 0.17957283642713237 | 0.03066605204457275 | 0.34547233117093445 | -0.056409 | -0.294429 | -0.303162 | `examples/benchmarks/comparison_runs/20260422_145426_csi1000_recent5y_topk5/lightgbm_stdout.log` |
| 20260422_155938_csi1000_recent5y_rr_topk5 | csi1000_recent5y | RR[Linear] | 0.013078086761560345 | 0.07884925826006921 | 0.08389441314353427 | 0.44567556549303594 | -0.163908 | -0.845681 | -0.407577 | `examples/benchmarks/comparison_runs/20260422_155938_csi1000_recent5y_rr_topk5/RR_Linear_stdout.log` |
| 20260422_155938_csi1000_recent5y_rr_topk5 | csi1000_recent5y | RR[LightGBM] | 0.02211097337592498 | 0.17035052469016448 | 0.07518632880117257 | 0.5275184697123183 | -0.009116 | -0.041174 | -0.291130 | `examples/benchmarks/comparison_runs/20260422_155938_csi1000_recent5y_rr_topk5/RR_LightGBM_stdout.log` |
| 20260427_152515_csi1000_recent_usable_topk5 | csi1000_recent2y | linear | -0.0002082031847114145 | -0.0013582015765295562 | 0.039427583246114756 | 0.22169908516176762 | -0.374312 | -1.672011 | -0.105397 | `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5/linear_recent2y_stdout.log` |
| 20260427_152515_csi1000_recent_usable_topk5 | csi1000_recent2y | lightgbm | 0.006716974791382605 | 0.06012170848377766 | 0.028901850549687743 | 0.24403944005969347 | -0.636658 | -2.821270 | -0.253364 | `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5/lightgbm_recent2y_stdout.log` |
| 20260427_152515_csi1000_recent_usable_topk5 | csi1000_recent3y | linear | 0.0004800064049762163 | 0.00290014898731162 | 0.047635822631639055 | 0.26091990677646937 | -0.453494 | -1.944058 | -0.108688 | `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5/linear_recent3y_stdout.log` |
| 20260427_152515_csi1000_recent_usable_topk5 | csi1000_recent3y | lightgbm | 0.00887121257192031 | 0.07299444503080597 | 0.02726964934798768 | 0.19962259137033392 | -1.075264 | -4.653375 | -0.308011 | `examples/benchmarks/comparison_runs/20260427_152515_csi1000_recent_usable_topk5/lightgbm_recent3y_stdout.log` |
