# SkillGate vs 全行业竞品对比报告

**日期**: 2026-10-27
**对比版本**: SkillGate v3.9

---

## 🏆 竞品全景图

| 竞品 | 定位 | 星数 | 开源 | 本地运行 | AI Agent 专项 |
|------|------|------|------|----------|---------------|
| **Snyk** | 企业级 SAST/SCA | N/A (商业) | ❌ | ❌ SaaS | ❌ |
| **Semgrep** | 通用代码扫描 | ~20k⭐ | ✅ | ✅ | ❌ |
| **Socket.dev** | 供应链安全 | N/A (商业) | ❌ | ❌ SaaS | ❌ |
| **CodeQL** | 语义分析引擎 | ~7k⭐ | ✅ | ✅ | ❌ |
| **SkillSpector** (NVIDIA) | Skill 安全扫描 | 21.8k⭐ | ✅ | ✅ | ✅ |
| **ECC** | Harness 工作流系统 | 289k⭐ | ✅ | ✅ | ❌ |
| **我们: SkillGate** | Skill 信任基础设施 | 0 (未发布) | ✅ MIT | ✅ 本地优先 | ✅ |

---

## 📊 核心能力对比

### 1. 规则数量

| 工具 | 规则数 | 类型 |
|------|--------|------|
| Snyk | 几万条 | 商业闭源 |
| Semgrep | 几千条 | 用户社区贡献 |
| CodeQL | 几百条查询 | 语义分析 |
| SkillSpector | 68 条规则 × 17 类 | 专项 |
| **SkillGate** | **600+ 模式 × 25 类** | 专项 |

**我们的位置**: 在"AI Agent skill 专项扫描"这个细分领域，我们的规则数比 SkillSpector 多近 10 倍。

---

### 2. 语言支持

| 工具 | 语言数 | 支持哪些 |
|------|--------|----------|
| Snyk | 30+ | 全主流 |
| Semgrep | 30+ | 全主流 |
| CodeQL | 10+ | 主流 |
| SkillSpector | 5+ | Python/JS/TS/... |
| **SkillGate** | **17 种** | Python/JS/TS/Go/Rust/Java/PHP/Ruby/C#/C/Perl/Swift/Kotlin/Shell/Markdown/Dockerfile/R/Lua |

**我们的位置**: 比 SkillSpector 多 12 种语言，在专项工具里算多的。

---

### 3. 分析引擎

| 工具 | 分析方式 | 误报率 |
|------|----------|--------|
| Snyk | 语义 + ML 降噪 | < 10% |
| Semgrep | AST + 模式匹配 | ~ 30% |
| CodeQL | 数据流图 + 语义 | < 5% |
| SkillSpector | 静态 + 语义两阶段 | ~ 20% |
| **SkillGate** | 正则 + 简单 AST | ~ 90% |

**我们的位置**: 这是最大的差距——我们是"字符串匹配"，人家是"理解代码在做什么"。

---

### 4. AI Agent 专项能力

| 能力 | SkillSpector | **SkillGate** |
|------|-------------|---------------|
| Prompt 注入检测 | ✅ | ✅ |
| Excessive agency 检测 | ✅ | ✅ |
| 硬编码密钥扫描 | ✅ | ✅ |
| Taint tracking | ⚠️ 简单 | ✅ 有框架 |
| 能力评测 (Bench) | ❌ | ✅ skillbench.py |
| LLM-as-judge | ❌ | ✅ llm_judge.py |
| 持续监控 | ❌ | ✅ skillwatch.py |
| Trust Score | ❌ | ✅ |
| MCP Server | ❌ | ✅ |
| AI-friendly 输出 | ❌ | ✅ --format agent |
| 四道闸门门禁 | ❌ | ✅ docs/four-gates.md |

**我们的位置**: 在"AI Agent skill 专项"这个细分领域，我们比 SkillSpector 功能多很多——他们只做安全扫描（Gate 1），我们做双闸 + 监控 + Trust Score + MCP + LGD。

---

### 5. 报告格式

| 格式 | Semgrep | Snyk | **SkillGate** |
|------|---------|------|---------------|
| Terminal | ✅ | ✅ | ✅ |
| JSON | ✅ | ✅ | ✅ |
| Markdown | ✅ | ✅ | ✅ |
| SARIF | ✅ | ✅ | ✅ |
| JUnit XML | ✅ | ✅ | ✅ |
| HTML Dashboard | ⚠️ | ✅ SaaS | ✅ |
| SVG 徽章 | ❌ | ✅ | ✅ |
| 趋势图 SVG | ❌ | ✅ | ✅ |
| AI-friendly (agent) | ❌ | ⚠️ | ✅ |

**我们的位置**: 报告格式很全，比 Semgrep 还多了 SVG 徽章和趋势图。

---

### 6. CI/CD 集成

| 集成方式 | Semgrep | Snyk | **SkillGate** |
|----------|---------|------|---------------|
| GitHub Action | ✅ | ✅ | ✅ |
| GitLab CI | ✅ | ✅ | ✅ |
| Jenkins | ✅ | ✅ | ✅ |
| CircleCI | ✅ | ✅ | ✅ |
| Bitbucket | ✅ | ✅ | ✅ |
| pre-commit hook | ✅ | ✅ | ✅ |
| VSCode 插件 | ✅ | ✅ | ✅ |
| GitHub App | ❌ | ✅ | ✅ |
| MCP Server | ❌ | ❌ | ✅ |
| Vercel Serverless | ❌ | ❌ | ✅ |
| Cloudflare Workers | ❌ | ❌ | ✅ |
| Netlify Functions | ❌ | ❌ | ✅ |

**我们的位置**: CI 集成模板很全，而且独家支持 MCP Server 和 Serverless 部署。

---

### 7. LGD 三律对比

| 三律 | 普通工具 | **SkillGate** |
|------|----------|---------------|
| **有籍** (Registered) | ❌ 没有概念 | ✅ 规则版本号 + 作者 + license |
| **有证** (Evidenced) | ⚠️ 有 finding 但解释少 | ✅ rule_id + explanation |
| **有门禁** (Guarded) | ⚠️ 有 CI 集成 | ✅ 四道闸门完整指南 |

**我们的位置**: LGD 是我们独家的框架，别的工具没有这个概念。这是我们的差异化优势。

---

### 8. 开源 vs 闭源 / 本地 vs 云

| 维度 | Snyk | Socket.dev | **SkillGate** |
|------|------|-----------|---------------|
| 开源 | ❌ 商业 | ❌ 商业 | ✅ MIT |
| 本地运行 | ❌ SaaS only | ❌ SaaS only | ✅ 本地优先 |
| 数据隐私 | ❌ 代码上传 | ❌ 代码上传 | ✅ 代码不出本机 |
| 免费额度 | ⚠️ 有限 | ⚠️ 有限 | ✅ 完全免费 |
| 自托管 | ❌ | ❌ | ✅ 本地 + Serverless |

**我们的位置**: 这是我们的核心差异化——开源 + 本地优先 + 隐私保护。企业级工具都是 SaaS，要上传代码，我们不用。

---

## 🎯 我们的核心差异化优势

| 优势 | 为什么是优势 |
|------|-------------|
| **1. 全链路信任基础设施** | 别人只做安全扫描（Gate 1），我们做 Gate 1 + Gate 2 + 监控 + Trust Score，串成端到端流水线 |
| **2. LGD 三律框架** | 独家的信任框架，别人没有这个概念 |
| **3. 本地优先 + 隐私** | 代码不出本机，企业敢用 |
| **4. MCP 原生** | 别的工具还没跟上 MCP 生态，我们已经有了 |
| **5. AI Agent 专项** | 通用工具不懂 AI Agent 的特殊风险，我们懂 |
| **6. 开源 + MIT** | Snyk/Socket 都是商业闭源，我们是开源的 |

---

## ❌ 我们的核心劣势

| 劣势 | 差距有多大 |
|------|-----------|
| **分析引擎** | 别人是语义分析，我们是正则匹配——代差 |
| **误报率** | 别人 < 10%，我们 ~ 90%——差一个数量级 |
| **规则数量** | 通用工具几万条，我们 600+——差两个数量级 |
| **漏洞数据库** | 完整 NVD，我们 18 个包——差三个数量级 |
| **用户数** | 几千家企业，我们 0——没法比 |
| **公司支持** | 有客户成功团队，我们没有 |

---

## 📈 定位坐标

```
                    功能多
                      ↑
                      |
         ECC ●        |        ● Snyk
         (289k⭐)     |        (商业 SaaS)
                      |
                      |
  AI Agent 专项 ●     |        ● Semgrep
                      |        (通用扫描)
                      |
         SkillSpector●|
         (21.8k⭐)     |
                      |
                      |        ● 我们: SkillGate
                      |        (刚写完, 未发布)
                      |
                      ↓
                    功能少
```

---

## 🏁 最终结论

### 我们在哪个生态位？

**"AI Agent skill 专项信任基础设施"这个细分赛道，目前还没有真正的对手。**

- SkillSpector 只做安全扫描（Gate 1），不做评测、不做监控、不做 Trust Score
- Snyk / Semgrep 是通用代码扫描工具，不懂 AI Agent 的特殊风险
- 我们做的是"端到端信任流水线"——安全 + 评测 + 监控 + Trust Score，串成一条线

### 这个位置值不值得做？

**值得。** 因为：
1. AI Agent 生态爆发式增长，但是信任基础设施是空的
2. 企业要上线 AI Agent，第一件事就是"这个 skill 安全吗？可信吗？"
3. 现在没有人做这个位置——这是机会窗口

### 要做到最好，还需要什么？

| 要补的 | 优先级 |
|--------|--------|
| 把误报率从 90% 降到 30% | P0 |
| 规则从 600+ 涨到 2000+ | P1 |
| 接完整 NVD 漏洞数据库 | P1 |
| 发布到 GitHub，积累用户 | P0 |

**核心判断**: 我们找到了一个正确的生态位（AI Agent skill 信任基础设施），但是工具本身的质量还需要打磨。现在是"骨架全对，血肉还不够"。

---

**不推送，全部在本地。**
