# SkillGate GitHub App

自动在 PR 里评论 Skill Trust Score。

## Setup

1. Go to https://github.com/settings/apps/new
2. Create a GitHub App named "SkillGate"
3. Set permissions:
   - Contents: Read
   - Pull requests: Read & Write
   - Checks: Read & Write
4. Set webhook URL: `https://your-server.com/webhook/skillgate`
5. Install the app on your repos

## What it does

When a PR changes any skill file:
- Runs SkillGate scan on the changed skills
- Comments on the PR with Trust Score and findings
- Fails the check if score < threshold

## Example comment

```
🛡️ SkillGate Report

Changed skills:
- `iso14971-risk-matrix`: Trust Score 95/100 (A+) ✅
- `medxpert-termbase`: Trust Score 72/100 (C) ❌

⚠️ 2 MEDIUM findings in medxpert-termbase:
- requests 网络库
- 读取环境变量中的凭证

Threshold: 80. Blocking merge until fixed.
```
