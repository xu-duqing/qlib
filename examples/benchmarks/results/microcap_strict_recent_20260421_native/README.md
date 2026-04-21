# Microcap strict recent benchmark export (native instruments)

This run uses the new strict universe rebuilt without `.BJ`, converted into a qlib-native instruments file instead of relying on `inst_processor` filtering.

## Linear vs LightGBM 简洁对比

| 模型 | Run ID | IC | ICIR | Rank IC | Rank ICIR | 带成本年化超额 | 带成本信息比率 | 带成本最大回撤 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Linear | `db368c58ca6f47a3b898e41fc9c848eb` | -0.0137 | -0.1146 | 0.0053 | 0.0400 | 0.1394 | 0.7866 | -0.0531 |
| LightGBM | `4002be5ec7bd4161834ec6267f44d62b` | 0.0411 | 0.5581 | 0.0353 | 0.4749 | 0.1631 | 0.8574 | -0.0531 |

**一句话结论：** 在这个 native strict microcap market 上，**LightGBM 明显优于 Linear**；信号指标更强，带成本年化超额也更高。

## Native market file

- source parquet: `examples/universe/a_share_microcap_10y/outputs/20260421_103028_strict_microcap_10y/members.parquet`
- native instruments: `examples/universe/a_share_microcap_10y/outputs/20260421_103028_strict_microcap_10y/microcap_strict_recent.txt`
- installed to local qlib data: `~/.qlib/qlib_data/cn_data/instruments/microcap_strict_recent.txt`

## Completed runs

### Linear
- run id: `db368c58ca6f47a3b898e41fc9c848eb`
- IC: `-0.013730738793051369`
- ICIR: `-0.11461565068492639`
- Rank IC: `0.005297296299442623`
- Rank ICIR: `0.03998646447031803`
- excess return without cost annualized: `0.1681217315757017`
- excess return with cost annualized: `0.13943710798142692`
- excess return with cost information ratio: `0.7865595733454844`
- max drawdown with cost: `-0.05312865972518921`

### LightGBM
- run id: `4002be5ec7bd4161834ec6267f44d62b`
- IC: `0.04112736871346318`
- ICIR: `0.558096254503645`
- Rank IC: `0.03529893048417808`
- Rank ICIR: `0.4748826974274604`
- l2.train: `0.9956236338606967`
- l2.valid: `0.9975905954761736`
- excess return without cost annualized: `0.19603461646812434`
- excess return with cost annualized: `0.16309483519608808`
- excess return with cost information ratio: `0.8574446495397802`
- max drawdown with cost: `-0.05312865972518921`

## Quick comparison

- On this native strict microcap market, **LightGBM beat Linear** on signal metrics (`IC`, `ICIR`) and also slightly beat it on costed annualized excess return.
- Linear costed annualized excess return: `0.13943710798142692`
- LightGBM costed annualized excess return: `0.16309483519608808`
- Both runs had the same reported max drawdown with cost: `-0.05312865972518921`

See `runs_summary.json` for the machine-readable export.
