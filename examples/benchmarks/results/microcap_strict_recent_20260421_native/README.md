# 严格微盘池 benchmark 结果（2026-04-21，native 版本）

这份结果基于新的严格微盘池生成，不含 `.BJ`。这次没有再走 `inst_processor` 临时过滤，而是先把股票池转成 qlib 原生的 instruments 文件，再跑普通 benchmark 和动态 RR benchmark。

## 先看结论

- 静态 benchmark 里，**LightGBM 好于 Linear**。
- 动态 RR benchmark 里，**RR[LightGBM] 和 RR[Linear] 都明显强于静态版本**。
- RR 这次在收益上明显放大了，但信号指标（IC / ICIR）不一定同步更强。
- **DDG-DA 这次还没跑出来**，不是策略问题，而是当前环境缺少可安装的 PyTorch。

## 简洁对比表

| 方法 | Run / 状态 | IC | ICIR | Rank IC | Rank ICIR | 带成本年化超额 | 带成本信息比率 | 带成本最大回撤 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Linear | `db368c58ca6f47a3b898e41fc9c848eb` | -0.0137 | -0.1146 | 0.0053 | 0.0400 | 0.1394 | 0.7866 | -0.0531 |
| LightGBM | `4002be5ec7bd4161834ec6267f44d62b` | 0.0411 | 0.5581 | 0.0353 | 0.4749 | 0.1631 | 0.8574 | -0.0531 |
| RR[Linear] | 已跑通 | -0.0036 | -0.0645 | 0.0627 | 0.7748 | 0.8047 | 3.6969 | -0.0531 |
| RR[LightGBM] | 已跑通 | -0.0191 | -0.2899 | -0.0379 | -0.4124 | 0.8152 | 3.3394 | -0.0531 |
| DDG-DA[Linear] | 未跑通 | - | - | - | - | - | - | - |
| DDG-DA[LightGBM] | 未跑通 | - | - | - | - | - | - | - |

## 当前怎么理解

### 静态 benchmark

- **LightGBM 优于 Linear**。
- 它的信号指标更好，带成本年化超额也更高。

### 动态 RR benchmark

- RR 版本这次收益明显更高。
- `RR[LightGBM]` 的带成本年化超额最高：`0.815210`
- `RR[Linear]` 略低一点：`0.804747`
- 但如果只看 IC / ICIR，这次 RR 并没有比静态版本更漂亮。
- 所以这组结果更像是：**动态滚动训练在这段样本里把收益做上去了，但不能只拿 IC 单独下结论。**

### DDG-DA

这次没跑出来，原因不是配置错了，也不是股票池有问题，而是：

- 当前环境：`Python 3.14.4`
- 平台：`macOS x86_64`
- `pip install torch` 失败
- 报错：`No matching distribution found for torch`

也就是说，**当前这个 Python / 平台组合拿不到可用的 torch 包**，所以 DDG-DA 入口就被卡住了。

## 股票池文件

这次使用的股票池来源：

- 原始成员文件：`examples/universe/a_share_microcap_10y/outputs/20260421_103028_strict_microcap_10y/members.parquet`
- 转换后的 qlib instruments 文件：`examples/universe/a_share_microcap_10y/outputs/20260421_103028_strict_microcap_10y/microcap_strict_recent.txt`
- 本地安装位置：`~/.qlib/qlib_data/cn_data/instruments/microcap_strict_recent.txt`

## 静态 benchmark 结果

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

## 动态 RR benchmark 结果

### RR[Linear]

- IC：`-0.003609183563012218`
- ICIR：`-0.06452689843606861`
- Rank IC：`0.06273299596012825`
- Rank ICIR：`0.7748020853843213`
- 带成本年化超额：`0.804747`
- 带成本信息比率：`3.696948`
- 带成本最大回撤：`-0.053129`

### RR[LightGBM]

- IC：`-0.01913861966806506`
- ICIR：`-0.2899105983623223`
- Rank IC：`-0.03785410091836211`
- Rank ICIR：`-0.41243059069322824`
- 带成本年化超额：`0.815210`
- 带成本信息比率：`3.339370`
- 带成本最大回撤：`-0.053129`

## 一句话总结

如果现在只看已经真实跑出来的结果：

- 静态版本里，**LightGBM 胜出**。
- 动态 RR 版本里，**RR[LightGBM] 和 RR[Linear] 都把收益显著拉高了**。
- DDG-DA 需要换一个能装 PyTorch 的环境后再继续。

更详细的机器可读结果见：
- `runs_summary.json`
- `rr_runs_summary.json`
