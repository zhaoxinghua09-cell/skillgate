# STRUCTURE — skillgate 的分层与改动代价

## 五层

| 层 | 文件 | 内容 |
|---|---|---|
| L1 规则 | `rules/example-rules.yml`、`docs/rules.md`、`.skillgate.yml` | 规则格式与仓内配置 |
| L2 分析 | `ast_analyzer.py`、`taint_tracker.py`、`{js,java_php,ruby_csharp,c_perl,go_rust,swift_kotlin}_analyzer.py`、`dockerfile_scanner.py`、`k8s_scanner.py`、`terraform_scanner.py`、`cve_database.py` | 多语言静态分析、污点追踪、基础设施扫描 |
| L3 门禁 | `runtime.py`、`skillgate.py`、`scripts/skillgate.py`、`rule_engine.py`、`router.py`、`ci-templates/*`、`serverless/*` | 扫描入口、规则执行、CI/无服务部署 |
| L4 评测 | `benchmark.py`、`skillbench.py`、`tests/`、`run-all-tests.py`、`pressure_test.py`、`stress_test.py`、`performance_test.py` | 红队、100 次重复、压力与性能 |
| L5 输出与治理 | `html_report.py`、`dashboard.html`、`badge_generator.py`、`scorecard.py`、`governance.py`、`audit_log.py`、`EVIDENCE-INDEX.md` | 报告、徽章、审计日志 |

## 改动代价

| 你想做 | 改哪里 | 必须重跑 | 必须同步 |
|---|---|---|---|
| 加一条规则 | `rules/` | `tests/test_skillgate.py`（每规则须有命中样本与不命中样本） | `docs/rules.md`、`benchmark.py` 基准 |
| 改评分口径 | `scorecard.py` | `test_strict_benchmark.py`、`benchmark.py` | README 分数说明（**须写明"自评"**） |
| 加语言分析器 | 新 `*_analyzer.py` + 注册 | `run-all-tests.py` | `docs/applicability.md` |
| 改 CI 模板 | `ci-templates/` | `ci-simulator.py` | 各平台示例 |

## 边界

本仓判"技能/产物能不能发"；`lcas` 判"变更是否越界"；`uibc-core` 判"证据有没有被换"。
三者共用证据分级口径，**证据不互借**。
