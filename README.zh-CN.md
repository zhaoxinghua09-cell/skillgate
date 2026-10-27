<div align="center">

# 🛡️ SkillGate

**AI Agent 技能的信任基础设施。**

开源安全扫描器 + 能力评估器 + 持续监控，为 AI Agent 生态打造。

<p align="center">
  <strong>语言：</strong>
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a>
</p>

</div>

---

## 🤔 为什么我做这个

我喜欢 AI Agent 技能——它们让 Claude Code、Cursor、Codex 变得强大得多。

但是有个问题：**当你从网上安装一个随机的技能时，你真的知道它做了什么吗？**

它会读你的文件吗？会把你的数据发到服务器吗？有硬编码的 API 密钥吗？会在你的输入上跑 `eval()` 吗？

我试过用 Snyk 和 CodeQL 来做这个，但是它们是为普通代码设计的——不是为 AI 技能设计的。技能有自己的模式：SKILL.md 文件、用你的 Agent 权限运行的脚本、告诉 Agent 做什么的指令。

所以我做了 SkillGate。它是一个**专门为 AI Agent 技能设计的安全扫描器**。它用一个数字告诉你：*我能信任这个技能吗？*

这只是个开始。随着 Agent 生态的发展，我们会需要这样的基础设施——就像我们需要 npm audit、Snyk、Dependabot 来管理普通包一样。

---

## ✨ 特性

- 🔍 **600+ 条安全规则**，覆盖 25 大类，17 种语言
- 🏆 **信任评分**（A+ 到 D）——一个数字你就能信任
- 📦 **全平台支持**：Claude Code、Cursor、Codex、Gemini、Copilot
- 🚀 **一行命令安装**：`npx skills add zhaoxinghua09-cell/skillgate`
- 📴 **离线可用**：不需要联网，本地运行
- 🪶 **零依赖**：装完就能跑，不需要装一堆东西
- 🌐 **跨平台**：Windows / Mac / Linux 都能用

---

## 🚀 快速开始

### 作为 Agent 技能安装（推荐）

一行命令安装——支持 Claude Code、Cursor、Codex 和任何支持 skills 标准的 Agent：

```bash
npx skills add zhaoxinghua09-cell/skillgate
```

然后问你的 Agent：*"帮我检查一下这个技能安全吗"*——它会自动用 SkillGate！

### 作为 CLI 工具安装

```bash
# Clone 仓库
git clone https://github.com/zhaoxinghua09-cell/skillgate.git
cd skillgate

# 安装（不需要依赖！）
pip install -e .
```

### 扫描你的第一个技能

```bash
python skillgate.py scan ./my-skill/
```

---

## 📄 许可证

[MIT](LICENSE) — 对所有人免费。

---

<div align="center">

**用 ❤️ 为开源 Agent 生态打造。**

⭐ 觉得有用就给我们点个 star 吧！

</div>
