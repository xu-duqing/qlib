# Qlib Benchmark Report

后续运行结果统一记录在这里。

| 运行标识 | 股票池 | 模型 | IC | ICIR | Rank IC | Rank ICIR | 带成本年化超额 | 带成本信息比率 | 带成本最大回撤 | 日志 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 20260422_145426_csi1000_recent5y_topk5 | csi1000_recent5y | Linear | 0.00813561206637587 | 0.05103456851357552 | 0.055099528718901766 | 0.30387853311865815 | -0.020000 | -0.103538 | -0.245820 | `examples/benchmarks/comparison_runs/20260422_145426_csi1000_recent5y_topk5/linear_stdout.log` |
| 20260422_145426_csi1000_recent5y_topk5 | csi1000_recent5y | LightGBM | 0.01856549811596614 | 0.17957283642713237 | 0.03066605204457275 | 0.34547233117093445 | -0.056409 | -0.294429 | -0.303162 | `examples/benchmarks/comparison_runs/20260422_145426_csi1000_recent5y_topk5/lightgbm_stdout.log` |
| 20260422_155938_csi1000_recent5y_rr_topk5 | csi1000_recent5y | RR[Linear] | 0.013078086761560345 | 0.07884925826006921 | 0.08389441314353427 | 0.44567556549303594 | -0.163908 | -0.845681 | -0.407577 | `examples/benchmarks/comparison_runs/20260422_155938_csi1000_recent5y_rr_topk5/RR_Linear_stdout.log` |
| 20260422_155938_csi1000_recent5y_rr_topk5 | csi1000_recent5y | RR[LightGBM] | 0.02211097337592498 | 0.17035052469016448 | 0.07518632880117257 | 0.5275184697123183 | -0.009116 | -0.041174 | -0.291130 | `examples/benchmarks/comparison_runs/20260422_155938_csi1000_recent5y_rr_topk5/RR_LightGBM_stdout.log` |
