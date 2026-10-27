# LGD-Evo: A Methodology for Building Self-Improving AI Agent Ecosystems

**Xinghua Zhao**  
2026-10-27

---

## Abstract

We present LGD-Evo, a methodology for building trustworthy, self-improving AI agent ecosystems. LGD-Evo is built on three core principles: **Registered** (有籍), **Evidenced** (有证), and **Guarded** (有门禁). Combined with a four-level proactive capability model and a closed-loop self-evolution cycle, LGD-Evo provides a practical framework for developing and operating AI agent systems that are both effective and trustworthy.

---

## 1. Introduction

As AI agents become more capable and more widely deployed, two critical challenges emerge:
1. **Trust**: How do we know if an agent or skill is safe to use?
2. **Evolution**: How do we help agents and their skills improve over time?

Traditional software development methodologies were not designed for AI agents — which are dynamic, prompt-based, and can operate with significant autonomy. We need a new methodology.

LGD-Evo is our answer to this challenge. It has been developed through practical experience building and operating AI agent systems, and it forms the foundation of the SkillGate project.

---

## 2. The Three LGD Principles

LGD-Evo is built on three core principles:

### 2.1 Registered (有籍)

**Every artifact has a traceable identity.**

- Every skill, tool, or agent must have a clear identity: author, version, license, and provenance.
- Every decision or output must be traceable back to its source.
- No anonymous or untraceable components are allowed in the ecosystem.

**Why it matters**: Without identity, you cannot trust anything. You cannot fix problems if you don't know who made what.

### 2.2 Evidenced (有证)

**Every claim has evidence.**

- Every finding, recommendation, or conclusion must have proof.
- "I think" is not enough — you must show the work.
- Every rule must have an explanation and a suggested fix.

**Why it matters**: Without evidence, you cannot verify anything. You end up trusting black boxes.

### 2.3 Guarded (有门禁)

**Every gate is checked automatically.**

- Every step in the pipeline has an automated gate.
- Nothing goes through without passing the check.
- Gates are configurable — you set the threshold.

**Why it matters**: Without gates, human error creeps in. You cannot rely on people to remember to check everything.

---

## 3. The Four Levels of Proactivity

LGD-Evo defines four levels of proactive capability:

| Level | Name | Description |
|-------|------|-------------|
| 1 | **Reactive** | The agent only does what you explicitly ask. It waits for commands. |
| 2 | **Suggestive** | The agent proactively suggests improvements or next steps, but waits for approval. |
| 3 | **Semiautonomous** | The agent can make small, reversible decisions on its own. It reports what it did. |
| 4 | **Autonomous** | The agent can plan and execute multi-step tasks on its own. It only asks for help when it gets stuck. |

LGD-Evo's goal is to help systems move up this ladder — safely, with proper guards.

---

## 4. The Self-Evolution Closed Loop

LGD-Evo includes a closed-loop self-evolution cycle:

```
Observe → Measure → Reflect → Improve → Repeat
```

1. **Observe**: Collect data about what works and what doesn't.
2. **Measure**: Quantify performance, error rates, user satisfaction.
3. **Reflect**: Analyze the data — where are the bottlenecks? What can be improved?
4. **Improve**: Make changes — add rules, fix bugs, update prompts.
5. **Repeat**: Go back to step 1.

This loop ensures that the system gets better over time, rather than staying static.

---

## 5. Seventeen Principles of LGD-Evo

1. **Local first**: Run locally when possible. Don't send data to the cloud unless you have to.
2. **Offline capable**: The system must work without internet.
3. **Zero dependencies**: Minimize dependencies. The simpler, the more reliable.
4. **Explicit over implicit**: Be explicit about what you're doing. Don't hide magic.
5. **Falsifiable**: Every claim must be testable. You must be able to prove it wrong.
6. **Graduated severity**: Not all issues are equal. Prioritize by impact.
7. **Human in the loop**: For important decisions, a human should be able to intervene.
8. **Fail closed**: When in doubt, fail safe. Don't let unknown things through.
9. **Iterate fast**: Ship small, iterate quickly. Don't wait for perfection.
10. **Document everything**: If you didn't write it down, it didn't happen.
11. **Test everything**: Every change must be tested.
12. **Boring technology**: Use boring, well-understood technology. Don't chase hype.
13. **User-centric**: Build for the user, not for the technology.
14. **Open by default**: Open source, open data, open standards.
15. **Privacy by design**: Privacy is not an afterthought.
16. **Accessible**: Make it easy to use. If it's hard, people won't use it.
17. **Have fun**: If you're not enjoying it, you're doing it wrong.

---

## 6. Application to SkillGate

SkillGate is the first implementation of LGD-Evo:

- **Registered**: Every skill scanned gets a Trust Score report with author, version, license info.
- **Evidenced**: Every finding has a rule ID, explanation, and suggested fix.
- **Guarded**: CI integration means every PR gets automatically scanned.

---

## 7. Conclusion

LGD-Evo is a practical methodology for building trustworthy, self-improving AI agent ecosystems. It has been tested in practice through the development of SkillGate.
