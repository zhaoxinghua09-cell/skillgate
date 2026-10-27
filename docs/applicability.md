# SkillGate 适用性评估

## 🎯 谁能用 SkillGate？

| 用户角色 | 怎么用 | 适配性 |
|----------|--------|--------|
| **个人开发者** | CLI 本地跑 | ✅ 完美适配 |
| **AI Agent（LLM）** | MCP Server / --format agent | ✅ 完美适配 |
| **团队 / 企业** | CI 集成 + GitHub App + Dashboard | ✅ 适配 |
| **开源项目维护者** | pre-commit + badge + Scorecard | ✅ 完美适配 |
| **安全团队** | SARIF 输出 + 审计日志 | ✅ 适配 |

---

## 💻 什么环境能跑？

| 环境 | 能跑吗 |
|------|--------|
| Windows | ✅ |
| Mac | ✅ |
| Linux | ✅ |
| Docker 容器 | ✅ |
| GitHub Actions | ✅ |
| GitLab CI | ✅ |
| Vercel Serverless | ✅ |
| Cloudflare Workers | ✅ |
| Netlify Functions | ✅ |
| 离线环境 | ✅ 99% 功能 |

**只要有 Python 3.8+ 的地方就能跑。**

---

## 📦 支持哪些 Skill 格式？

| 格式 | 适配吗 |
|------|--------|
| SKILL.md（标准格式） | ✅ |
| AGENTS.md（OpenAI 格式） | ✅ |
| .cursorrules（Cursor 格式） | ✅ |
| .claude/skills/（Claude 格式） | ✅ |
| .agents/skills/（通用格式） | ✅ |

**不绑定任何特定 harness，全生态兼容。**

---

## 🗣️ 支持哪些编程语言？

现在支持 **17 种**：
- Python
- JavaScript / TypeScript
- Go / Rust
- Java / PHP
- Ruby / C#
- C / Perl
- Swift / Kotlin
- R / Lua
- Shell
- Markdown
- Dockerfile

---

## 🔌 怎么集成到工作流？

| 集成方式 | 适配吗 |
|----------|--------|
| CLI 命令行 | ✅ |
| pre-commit hook | ✅ |
| GitHub Action | ✅ |
| GitLab CI | ✅ |
| Jenkins | ✅ |
| CircleCI | ✅ |
| Bitbucket Pipelines | ✅ |
| AWS CodeBuild | ✅ |
| VSCode 插件 | ✅ |
| MCP Server（给 AI agent 用） | ✅ |
| GitHub App（PR 自动评论） | ✅ |
| Vercel / Cloudflare / Netlify | ✅ |

---

## ❌ 什么场景不适用？

| 场景 | 为什么不适用 |
|------|-------------|
| 移动端 App 内嵌 | 我们是 CLI / 服务器工具 |
| 嵌入式设备 | 需要 Python 环境 |
| 实时运行时防护 | 我们是静态分析，不是 runtime 安全 |
| 代码混淆 / 加密代码 | 我们是读明文文本扫描 |
| 图形化拖拽操作 | 我们是开发者工具 |

---

## 🆚 和竞品比适用性

| 维度 | SkillGate | SkillSpector (NVIDIA) | Snyk |
|------|-----------|----------------------|------|
| 本地运行 | ✅ 100% | ✅ | ❌ SaaS only |
| 离线可用 | ✅ 99% | ✅ | ❌ |
| 不绑定 harness | ✅ 全格式 | ❌ 只支持特定格式 | ✅ |
| AI agent 原生 | ✅ MCP + agent 输出 | ❌ | ❌ |
| 企业级 Dashboard | ✅ 有 | ❌ | ✅ SaaS |
| 移动端 | ❌ | ❌ | ❌ |

---

## 🏁 结论

**适用性现在是 9/10。**

✅ **做到最好的部分：**
- 全操作系统兼容
- 全 harness 格式兼容
- 全 CI 平台兼容
- 本地优先 + 离线可用
- AI agent 原生支持

❌ **还没覆盖的：**
- 移动端
- 嵌入式设备
- 运行时防护（不是静态分析能做的）

**核心判断**: 在"开发者工具 + CI/CD + AI agent"这个赛道里，我们的适用性已经做到最广了。剩下的是"移动端 + 嵌入式"——那是不同的产品形态，不是同一个工具能覆盖的。
