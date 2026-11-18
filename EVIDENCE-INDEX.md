# EVIDENCE-INDEX — skillgate

## 现状

| 级 | 结果 | 证据位置 | 说明 |
|---|---|---|---|
| L1 自我复现 | **有** | `tests/`（`test_skillgate.py`、`test_red_team.py`、`test_100_runs.py`、`test_runtime_100_runs.py`、`test_e2e_simulation.py`、`test_error_handling.py`、`test_output_formats.py`、`test_coverage.py`、`test_integration.py`、`test_strict_benchmark.py`）、`run-all-tests.py`、`benchmark.py`、`skillbench.py`、`methodology_self_check.py`、`.github/workflows/{ci,codeql,scorecard,auto-eval}.yml` | 含红队用例与 100 次重复运行；CI 每次 push 跑 |
| L2 异体审查 | **待核** | `third-party-security-audit.md`、`external-user-test-report.md`、`mutual-scoring.md`、`competitive-analysis.md` | 文件标题声称第三方/外部用户，但**报告内是否写明审查者身份、范围、结论**尚未逐份核对；核对前不计 L2 |
| L3 第二实现 | **0** | — | 规则引擎与扫描器同源，无独立实现对照 |
| L3.5 外部语料 | **0** | — | `benchmarks/public-benchmark.md` 是自建基准，属 L1 范围 |
| L4 外部节点 | **0** | — | 无第三方组织实际采用并可指认 |

## 已知不硬的地方

1. **自评分被排版成评分卡。** README 顶部 `LGD Trust Score: 97/100` 是**本仓自评**，与旁边的 OpenSSF Scorecard 5.4/10（第三方计算）并列展示，容易被读成同一性质。对外引用必须区分：5.4 是外部，97 是自评。
2. **"第三方"三字需证据。** `third-party-security-audit.md` 若不写明审查方名称与时间，就只是"一份自述文件"。
3. **规则覆盖有限。** `rules/example-rules.yml` 是示例规则；扫描能力随规则增长，不宣称覆盖全部漏洞类型。
4. **分数不是合规结论。** 评分用于排序与发现，不构成安全认证。

## 维护约定

- 新增规则 → 同步负控样本 → 更新本表 L1 行。
- 引用的第三方报告必须附审查者标识；否则从 L2 降级。
- 等级只降不升，除非新证据落盘。
