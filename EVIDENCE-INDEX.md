# EVIDENCE-INDEX — skillgate

## 现状

| 级 | 结果 | 证据位置 | 说明 |
|---|---|---|---|
| L1 自我复现 | **有** | `tests/`（`test_skillgate.py`、`test_red_team.py`、`test_100_runs.py`、`test_runtime_100_runs.py`、`test_e2e_simulation.py`、`test_error_handling.py`、`test_output_formats.py`、`test_coverage.py`、`test_integration.py`、`test_strict_benchmark.py`）、`run-all-tests.py`、`benchmark.py`、`skillbench.py`、`methodology_self_check.py`、`.github/workflows/{ci,codeql,scorecard,auto-eval}.yml` | 含红队用例与 100 次重复运行；CI 每次 push 跑 |
| L2 异体审查 | **0（已取证，不成立）** | `third-party-security-audit.md`、`external-user-test-report.md`、`mutual-scoring.md`、`competitive-analysis.md` | 2026-11-18 逐份核对：前者的"评测机构"写的是 **SkillGate Internal Red Team**——**内部红队，不是第三方**；后者未指明测试者身份与所用模型版本。标题写"第三方"、内容写"内部"，属标签与实质不符。**两份均不计 L2** |
| L3 第二实现 | **0** | — | 规则引擎与扫描器同源，无独立实现对照 |
| L3.5 外部语料 | **0** | — | `benchmarks/public-benchmark.md` 是自建基准，属 L1 范围 |
| L4 外部节点 | **0** | — | 无第三方组织实际采用并可指认 |

## 已知不硬的地方

1. **自评分被排版成评分卡。** README 顶部 `LGD Trust Score: 97/100` 是**本仓自评**，与旁边的 OpenSSF Scorecard 5.4/10（第三方计算）并列展示，容易被读成同一性质。对外引用必须区分：5.4 是外部，97 是自评。
2. **同一仓里同时存在 97/100 与 44/100。** `third-party-security-audit.md` 给自己的综合信任分是 **44/100（D+）**，其中"失控风险 4/10"、"准确率 5/10"。这与 README 的 97/100 并列在同一仓库里，**读者无法判断哪个才是当前结论**。这不是数据错误，是口径没有统一——两者评的维度不同、时间不同（v2.7 vs 当前版本），必须各自标明版本与口径，否则 97 这个数字经不起追问。
3. **"第三方"三字已证伪。** 见上表 L2 行。
3. **规则覆盖有限。** `rules/example-rules.yml` 是示例规则；扫描能力随规则增长，不宣称覆盖全部漏洞类型。
4. **分数不是合规结论。** 评分用于排序与发现，不构成安全认证。

## 维护约定

- 新增规则 → 同步负控样本 → 更新本表 L1 行。
- 引用的第三方报告必须附审查者标识；否则从 L2 降级。
- 等级只降不升，除非新证据落盘。
