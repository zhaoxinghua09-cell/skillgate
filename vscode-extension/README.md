# SkillGate VS Code Extension

AI Agent Skill 安全扫描与信任评分扩展。

## Features

- **Scan Current File** — 扫描当前文件的安全问题
- **Scan Workspace** — 扫描整个工作区
- **Show Dashboard** — 显示 SkillGate Dashboard
- **Auto-scan on save** — 保存文件时自动扫描（可选）

## Commands

| Command | Description |
|---------|-------------|
| `SkillGate: Scan Current File` | 扫描当前打开的文件 |
| `SkillGate: Scan Workspace` | 扫描整个工作区 |
| `SkillGate: Show Dashboard` | 打开 SkillGate Dashboard |

## Extension Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `skillgate.path` | `skillgate` | skillgate 可执行文件的路径 |
| `skillgate.autoScanOnSave` | `false` | 保存文件时自动扫描 |

## Requirements

- VS Code 1.75.0 or higher
- SkillGate CLI installed and in PATH

## License

MIT
