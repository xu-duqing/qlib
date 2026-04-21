# 严格微盘池 benchmark 结果（2026-04-21，native 版本）

这份结果基于新的严格微盘池生成，不含 `.BJ`。这次没有再走 `inst_processor` 临时过滤，而是先把股票池转成 qlib 原生的 instruments 文件，再跑 Linear 和 LightGBM。

## 先看结论

- 这次 **LightGBM 好于 Linear**。
- LightGBM 的 `IC / ICIR` 更强。
- LightGBM 的**带成本年化超额收益**也更高。
- 两者这次的**带成本最大回撤一样**。

## Linear vs LightGBM 简洁对比

| 模型 | Run ID | IC | ICIR | Rank IC | Rank ICIR | 带成本年化超额 | 带成本信息比率 | 带成本最大回撤 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Linear | `db368c58ca6f47a3b898e41fc9c848eb` | -0.0137 | -0.1146 | 0.0053 | 0.0400 | 0.1394 | 0.7866 | -0.0531 |
| LightGBM | `4002be5ec7bd4161834ec6267f44d62b` | 0.0411 | 0.5581 | 0.0353 | 0.4749 | 0.1631 | 0.8574 | -0.0531 |

## 股票池文件

这次使用的股票池来源：

- 原始成员文件：`examples/universe/a_share_microcap_10y/outputs/20260421_103028_strict_microcap_10y/members.parquet`
- 转换后的 qlib instruments 文件：`examples/universe/a_share_microcap_10y/outputs/20260421_103028_strict_microcap_10y/microcap_strict_recent.txt`
- 本地安装位置：`~/.qlib/qlib_data/cn_data/instruments/microcap_strict_recent.txt`

## 两次运行结果

### Linear

- run id：`db368c58ca6f47a3b898e41fc9c848eb`
- IC：`-0.013730738793051369`
- ICIR：`-0.11461565068492639`
- Rank IC：`0.005297296299442623`
- Rank ICIR：`0.03998646447031803`
- 不计成本年化超额：`0.1681217315757017`
- 带成本年化超额：`0.13943710798142692`
- 带成本信息比率：`0.7865595733454844`
- 带成本最大回撤：`-0.05312865972518921`

### LightGBM

- run id：`4002be5ec7bd4161834ec6267f44d62b`
- IC：`0.04112736871346318`
- ICIR：`0.558096254503645`
- Rank IC：`0.03529893048417808`
- Rank ICIR：`0.4748826974274604`
- l2.train：`0.9956236338606967`
- l2.valid：`0.9975905954761736`
- 不计成本年化超额：`0.19603461646812434`
- 带成本年化超额：`0.16309483519608808`
- 带成本信息比率：`0.8574446495397802`
- 带成本最大回撤：`-0.05312865972518921`

## 一句话总结

如果按这次结果直接选，**优先选 LightGBM**。因为它不只是信号指标更好，实际带成本收益也更高。

更详细的机器可读结果见：`runs_summary.json`
