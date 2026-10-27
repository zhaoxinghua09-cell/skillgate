# LGD Trust Framework

**有籍 · 有证 · 有门禁**

---

## What is LGD?

LGD is a trust framework for AI agent skills. It answers three questions:

| Question | Principle |
|----------|-----------|
| **Who are you?** | 📇 **Registered** (有籍) |
| **Why should I trust you?** | 📜 **Evidenced** (有证) |
| **What stops you from going rogue?** | 🚪 **Guarded** (有门禁) |

---

## 📇 Registered (有籍)

Every skill has a traceable identity.

**What it means**:
- Author is known
- Version is tracked
- License is clear
- Rule version is recorded (so you know which rules were used to score you)

**Why it matters**:
- If something goes wrong, you know who to talk to
- If rules change, you can re-score and compare

---

## 📜 Evidenced (有证)

Every finding has proof and explanation.

**What it means**:
- Rule ID: exactly which rule flagged this
- Explanation: why this is a problem
- Fix suggestion: how to fix it

**Why it matters**:
- You don't have to guess "is this finding real?"
- You can verify it yourself
- You can learn from it

---

## 🚪 Guarded (有门禁)

Every gate is checked automatically.

**What it means**:
- CI blocks bad PRs
- Pre-commit hooks catch issues early
- Trust Score threshold = hard gate

**Why it matters**:
- Human review is slow and inconsistent
- Automation catches what people miss
- Gates make trust reproducible

---

## Why LGD?

Most "trust scores" are:
- ❌ Black box (you don't know how they calculate)
- ❌ No evidence (just a number, no explanation)
- ❌ No gates (just a report, no enforcement)

LGD fixes all three:
- ✅ Registered: you know who and what
- ✅ Evidenced: you see the proof
- ✅ Guarded: you can enforce it

---

## How SkillGate implements LGD

| LGD Principle | SkillGate Feature |
|---------------|-------------------|
| Registered | `rule_version` field, frontmatter parsing |
| Evidenced | `rule_id` + `explanation` on every finding |
| Guarded | `--fail-under`, pre-commit hooks, CI templates |

---

## Extending LGD

LGD is a framework, not just a tool. You can apply it to:
- Your own internal skills
- Your team's CI pipeline
- Your open source project
- Your company's security policy

**The core idea**: trust should be built, not assumed.

---

**© LGD Trust Framework · MIT License**
