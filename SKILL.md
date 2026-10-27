---
name: skillgate
description: Trust infrastructure for AI agent skills. Scan any skill folder for security issues, calculate a Trust Score, check dependencies, and generate a report. Use when the user asks to audit, review, or check an AI skill's safety, quality, or trustworthiness.
version: 1.0.0
license: MIT
author: zhaoxinghua09-cell
tags:
- security
- trust
- audit
- scanner
- agent
- skills
---

# SkillGate — Skill Trust Scanner

## When to Use

- The user wants to **audit or review an AI agent skill** for security issues, quality, or trustworthiness.
- The user asks *"is this skill safe?"*, *"can I trust this skill?"*, *"check this skill for problems"*.
- You are about to **install or run a third-party skill** and want to make sure it's not malicious.
- You want to **compare two skills** and see which one has a better Trust Score.

## Usage

```bash
# Scan a skill folder and get a Trust Score
python scripts/skillgate.py scan ./path/to/skill/

# Scan with more output
python scripts/skillgate.py scan ./path/to/skill/ --verbose

# Output JSON (for programmatic use)
python scripts/skillgate.py scan ./path/to/skill/ --format json

# Output HTML report (beautiful, shareable)
python scripts/skillgate.py scan ./path/to/skill/ --format html
```

Exit code `0` = all good (Trust Score >= 80), `1` = issues found (Trust Score < 80), `2` = usage error.

## What It Checks

| Category | What it looks for |
|----------|-------------------|
| 🔒 **Secrets** | API keys, tokens, passwords hardcoded in the code |
| ☠️ **Dangerous code** | `eval()`, `exec()`, `os.system()`, `subprocess` with shell=True |
| 📦 **Dependencies** | Outdated or vulnerable dependencies |
| 📝 **SKILL.md quality** | Missing description, missing version, missing license |
| 🌐 **Network calls** | Unnecessary or suspicious network requests |
| 📂 **File system access** | Reading/writing files outside the skill folder |

## Trust Score

Start at 100 points, subtract based on findings:
- CRITICAL issue: -15 points
- HIGH issue: -8 points
- MEDIUM issue: -3 points
- LOW issue: -1 point

| Score | Grade | Meaning |
|-------|-------|---------|
| 90+ | A+ | Excellent — very safe |
| 80+ | A | Good — minor issues |
| 70+ | B | Fair — some concerns |
| 60+ | C | Poor — needs review |
| < 60 | D | Unsafe — do not use |

## Known Limits (be explicit with users)

- This is a **static scanner** — it looks at the code, it doesn't run it.
- It catches **known bad patterns**, not zero-day vulnerabilities.
- A clean scan means "no obvious red flags", not "100% safe".
- It only scans the code in the folder, not what the skill does when it runs.

## Output Discipline

- Always show the Trust Score and Grade prominently.
- List CRITICAL and HIGH findings first, don't bury them.
- Give a clear recommendation: *"safe to use"* / *"use with caution"* / *"do not use"*.
- Don't hide or downplay serious issues.
