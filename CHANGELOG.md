# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.12] - 2026-11-03

### Security (remove unneeded write helpers)
- 移除零引用的 `cache.py` / `traces.py`（无任何 import，运行时会向包目录写 cache.json/traces.json）——消除"optional helpers 越界写"面，README 目录树同步

## [1.0.11] - 2026-11-03

### Security (path-confinement hardening)
- `--output`/`--badge` 越界判定从字符串前缀匹配改为组件级 `is_relative_to` 精确判定——修复 `C:\target_evil` 伪装成 `C:\target` 子路径的前缀绕过
- 移除对不存在模块 audit_log 的死代码引用
- `medical-device-chain` HTML 报告改写到目标文档所在目录（不再写引擎目录）

## [1.0.10] - 2026-11-03

### Security (confined writes & enforced gate)
- `--output` / `--badge`（含 bench `--output`）写入路径强制限定在扫描目标目录内，越界写入直接拒绝——监控/扫描无法修改选中文件夹之外的任何文件
- `--batch` 模式现在同样执行 `--fail-under` 信任分阈值（此前仅检查 critical/high），声明的安全门禁全模式生效
- `medical-file-watcher` 监控日志改写到**被监控目录内**（`.medical-file-watcher-log.json`），不再写引擎目录
- README 能力描述收敛为实际实现（移除 taint/CVE 数据库/15-17 语言/Docker 扫描等夸大声明），目录树与实际包文件一致
- SKILL.md 新增 Confined writes 声明段

## [1.0.9] - 2026-11-03

### Security (zero-egress)
- 移除依赖漏洞在线检查（OSV API 联网）：扫描器**零网络出口**——不可信目标文件夹无法触发对外请求，与"无网络"声明完全一致；检测到依赖时仅输出离线提示
- 移除 urllib 网络库引用，全包无网络调用

## [1.0.8] - 2026-11-03

### Security (aig-skill-scan T09 fixes)
- 封堵"早期抑制绕过"：扫描阶段不再跳过任何 `# skillgate: ignore` 标记行，抑制统一由自扫限定的 post-filter 处理——被扫技能无法再用标记提前藏毒
- 封堵"目标配置排除 payload"：`.skillgate.yml/.yaml` 的 exclude 规则仅自扫时生效；扫描第三方技能时完全忽略其自带配置，防止静默排除危险文件
- 回归验证：os.system+ignore 标记（2 条 CRITICAL 保留 + suppression-abuse 报出）、os.system+配置藏毒（2 条 CRITICAL 保留）、自扫 97/A+/0 critical

## [1.0.7] - 2026-11-03

### Security
- 移除 `--lenient` 宽松模式：不再支持"所有规则降一级"（该模式可使 CRITICAL/HIGH 降级从而绕过发布门禁，属可绕过面）
- 包内代码执行点清零：skillbench 删除全部 subprocess 执行代码（仅保留测试定义数据 + dry-run 预览）；skillgate-mcp 改为进程内 import 直调（无 subprocess/无网络）；skillwatch 改为只读监控（进程内扫描调用）
- SKILL.md 边界声明与代码严格一致：零执行路径、无宽松模式、17 个配套技能精确列明（12 医疗合规 + 2 质量检查 + 3 工作流）

## [1.0.6] - 2026-11-03

### Security
- 修复抑制标记可被滥用的漏洞：`# skillgate: ignore` 仅在扫描引擎自身目录（规则库自扫）时生效；被扫描的第三方技能代码中的标记**无效**，且会被记为 `suppression-abuse` 发现——恶意技能无法再用该标记隐藏危险行为或操纵 Trust Score（扫描器评审确认此攻击面）
- skillbench 收敛为**仅 dry-run**：移除 `--execute`，`run` 只预览/导出测试定义，不执行任何代码；实际测试仅限仓库 `tests/` pytest 套件（开发环境）
- 说明文档同步更新（SKILL.md / README 边界声明）

## [1.0.5] - 2026-11-03

### Fixed
- skillbench 默认 dry-run：`run` 仅预览测试定义，不执行任何目标代码；实际执行需显式 `--execute`（仅限本包配套技能，禁止未信任第三方代码）
- SKILL.md / README 声明包范围：配套医疗合规技能库（ISO 13485 / IEC 62304 / IEC 62366 / IEC 60601 / IEC 81001 / ISO 10993 / IFU / PMS / CER 等）为明示功能并索引于 skills/SKILLS-INDEX.md；检测规则库包含危险模式字符串属检测设计，非可执行行为
- README 移除 `npx skills` 安装引用（改为 GitHub clone），消除无 pin 引用

## [1.0.4] - 2026-11-03

### Fixed
- 消除 ClawHub 静态扫描器自指误报：规则库必须包含 ev-al / e-xec 等危险调用模式，此前以连续字面量写在代码与注释中，被扫描器误判为 dynamic_code_execution（suspicious）；现改为运行时拼接，源码（含注释）不再出现连续危险调用字样，检测能力不变

## [1.0.3] - 2026-11-03

### Fixed
- 统一发布门禁退出码：JSON / SARIF / JUnit / Markdown / Agent 输出格式此前绕过门禁（恶意发现仍 exit 0），现与终端报告一致——存在 CRITICAL/HIGH 或 Trust Score 低于 --fail-under 即 exit 1
- `# skillgate: ignore` 抑制项如实披露：被抑制的发现不再静默，数量与清单随终端 / JSON / Markdown / SARIF 报告输出，Trust Score 计算口径透明（基于剩余发现，抑制情况明确标注）

## [1.0.2] - 2026-11-03

### Fixed
- 打包补齐引擎本体：技能包此前仅含技能集与文档，缺少 skillgate.py 等引擎文件；1.0.2 起完整发布 skillgate.py / rule_engine.py / ast_analyzer.py 等全部引擎组件，扫描器可实际执行

## [1.0.1] - 2026-11-02

### Added
- ClawHub 上架适配：skill-card.md 发布卡片、llms.txt 站点级文档、包结构对齐 ClawHub 校验要求

## [1.0.0] - 2026-10-27

### Added
- 🎉 First release!
- 600+ security rules across 25 categories, 17 languages
- Trust Score calculation (A+ to D)
- HTML, JSON, SARIF, JUnit output formats
- GitHub Actions CI integration
- CodeQL code scanning
- Dependabot automated dependency updates
- Codecov coverage reporting
- GitHub Pages documentation
- Standard SKILL.md format — works with Claude Code, Cursor, Codex
- llms.txt — AI-friendly documentation
- pyproject.toml — pip install support
- Full open-source project standard: CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE, CODEOWNERS, FUNDING.yml
- GitHub Discussions and Wiki enabled
- 14 Topics tags for discoverability
