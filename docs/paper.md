# SkillGate: Trust Infrastructure for AI Agent Skills

**Xinghua Zhao**  
Independent Researcher  
2026-10-27

---

## Abstract

As AI coding agents like Claude Code, Cursor, and Codex become mainstream, the ecosystem of shareable "skills" — reusable, prompt-based packages that extend agent capabilities — is growing rapidly. However, unlike traditional software packages, agent skills lack standardized trust infrastructure: users have no way to quickly assess whether a skill is safe, whether it will exfiltrate data, or whether it contains hidden malicious logic.

We present **SkillGate**, the first open-source, local-first trust infrastructure specifically designed for AI agent skills. SkillGate combines:

1. **Static security scanning** — 600+ rules across 25 categories, detecting hardcoded secrets, dangerous code patterns, and suspicious network calls across 17 programming languages
2. **SKILL.md quality evaluation** — checking for missing metadata, inconsistent descriptions, and structural issues that confuse agent selection
3. **A single Trust Score** (A+ to D) that distills all findings into one number users can understand at a glance

SkillGate is designed to be:
- **Local-first**: runs entirely offline, no cloud required — critical for enterprises handling sensitive code
- **Zero-dependency**: pure Python standard library only, works on Windows, Mac, and Linux
- **Standard-compatible**: works with any agent that supports the emerging SKILL.md format

We evaluate SkillGate on a dataset of 50 real-world and intentionally malicious skills, showing that it correctly identifies all critical security issues and common quality problems. SkillGate runs in under 500ms on a typical skill folder, making it fast enough for local development and CI/CD integration.

---

## 1. Introduction

AI agents are increasingly being extended by "skills" — small, shareable packages of instructions and scripts that tell an agent how to do a specific task. The SKILL.md standard has emerged as a common format, supported by Claude Code, Cursor, Codex, Gemini CLI, and other leading agents.

However, this ecosystem has a critical gap: **there is no standardized way to evaluate whether a skill is safe to use**. When a user installs a third-party skill from the internet, they must either:
- Read every line of code themselves (impractical at scale)
- Trust the skill author blindly (risky, especially in a post-supply-chain-attack world)
- Use generic code scanners like Snyk or CodeQL (not designed for the unique patterns of agent skills)

Agent skills have unique characteristics that make generic scanners insufficient:
1. They include **natural language instructions** (the SKILL.md file) that can manipulate the agent
2. They run with the **full permissions of the host agent** — reading files, executing commands, accessing the network
3. They are often **short and simple** — just a markdown file and a small script — but can still cause significant damage

SkillGate fills this gap by building a scanner specifically for the patterns that matter in agent skills.

---

## 2. Related Work

### 2.1 Traditional Security Scanners

- **Snyk** and **Dependabot** scan traditional package dependencies for known vulnerabilities. They work well for npm and PyPI packages, but they don't understand the SKILL.md format or the agent-specific attack surface.
- **GitHub CodeQL** provides semantic code analysis for general-purpose languages. It is powerful but heavyweight, requires a server, and doesn't check skill-specific metadata.
- **Semgrep** allows custom rule writing, but users must write all the skill-specific rules themselves.

### 2.2 AI Agent Safety Research

Recent work on AI agent safety has focused on:
- **Alignment and value learning** — making agents behave as intended
- **Prompt injection** — defending against malicious inputs
- **Tool use safety** — ensuring agents call tools appropriately

However, there has been little work on **evaluating the skills themselves** — the third-party packages that extend agent capabilities. This is the gap SkillGate addresses.

### 2.3 The SKILL.md Ecosystem

The SKILL.md format has exploded in popularity in 2026, with hundreds of community-built skills available for Claude Code, Cursor, and other agents. Platforms like devsly.io and agentskillslist.com now catalog thousands of skills. But there is no standardized way to evaluate their trustworthiness.

---

## 3. The LGD Trust Framework

SkillGate is built on the **LGD Trust Framework** (有籍 / 有证 / 有门禁):

| Principle | Meaning | How SkillGate implements it |
|-----------|---------|------------------------------|
| **Registered** (有籍) | Every skill has a traceable identity | Author, version, license, rule version tracking in the Trust Score report |
| **Evidenced** (有证) | Every finding has proof & explanation | Rule IDs, human-readable explanations, and suggested fixes |
| **Guarded** (有门禁) | Every gate is checked automatically | CI integration, pre-commit hooks, fail-under-threshold configuration |

This framework ensures that the Trust Score is not just a random number — it is grounded in evidence, process, and auditability.

---

## 4. System Design

SkillGate has three layers:

### 4.1 Security Scanner

The security scanner checks for 25 categories of issues across 17 programming languages:

| Category | Examples |
|----------|----------|
| Secrets | Hardcoded API keys, tokens, passwords |
| Dangerous code | `eval()`, `exec()`, `os.system()`, `subprocess` with shell=True |
| Network calls | Unnecessary or suspicious outbound HTTP requests |
| File system access | Reading/writing files outside the skill directory |
| Dependency vulnerabilities | Known CVEs in required packages |
| Docker issues | Outdated base images, EOL packages |

The scanner uses a combination of:
- **Regex pattern matching** for known bad patterns
- **AST analysis** for Python and JavaScript code
- **CVE database** lookup for common vulnerable package versions

### 4.2 SKILL.md Quality Checker

The quality checker validates the SKILL.md file itself:

1. **Required metadata**: name, description, version, license
2. **Description quality**: does it clearly state *when* to use the skill? (This is critical for agent selection — a vague description means the agent won't know when to use the skill)
3. **Structural consistency**: does the SKILL.md reference scripts that actually exist?
4. **Permission creep**: does the skill request more permissions than it needs?

### 4.3 Trust Score Calculator

The Trust Score starts at 100 points, subtracting points based on severity:

| Severity | Points deducted | Example |
|----------|-----------------|---------|
| CRITICAL | -15 | Hardcoded API key, `eval()` on user input |
| HIGH | -8 | Unnecessary network call, missing license |
| MEDIUM | -3 | Vague description, missing version |
| LOW | -1 | Minor style issues, typos |

Final grades:
- **A+** (90+): Excellent — very safe
- **A** (80+): Good — minor issues
- **B** (70+): Fair — some concerns
- **C** (60+): Poor — needs review
- **D** (< 60): Unsafe — do not use

---

## 5. Evaluation

We evaluated SkillGate on a dataset of 50 skills:

### 5.1 Test Dataset

- **25 "good" skills**: Real-world skills from the community, written by experienced developers
- **25 "bad" skills**: Intentionally malicious or low-quality skills, designed to test the scanner

### 5.2 Results

| Metric | Result |
|--------|--------|
| True positive rate (bad skills flagged) | 100% — all critical issues detected |
| True negative rate (good skills passed) | 92% — false positives on 2 well-written skills |
| Average scan time | 320ms per skill folder |
| Memory usage | ~45MB peak |

### 5.3 Case Studies

**Case 1: Good skill (95/100, Grade A+)**
- ✅ Clear SKILL.md description
- ✅ No dangerous code
- ✅ No hardcoded secrets
- ⚠️ Minor: missing author field

**Case 2: Bad skill (42/100, Grade D)**
- ❌ Hardcoded OpenAI API key
- ❌ Uses `eval()` on user input
- ❌ Sends data to an unknown server
- ❌ Missing license and version

---

## 6. Discussion

### 6.1 Why not just use Snyk?

Snyk is excellent for traditional packages, but:
- It doesn't understand the SKILL.md format
- It doesn't check skill-specific metadata (description quality, permission creep)
- It requires a cloud account
- It's expensive for enterprise use

SkillGate is built specifically for the agent skill ecosystem.

### 6.2 Limitations

- **Static analysis only**: SkillGate doesn't run the skill, so it can't detect runtime behavior
- **Language coverage**: 17 languages supported, but some niche languages are not yet covered
- **False positives**: Like all scanners, SkillGate can flag legitimate patterns as suspicious. The `--lenient` mode is provided to reduce noise.

### 6.3 Future Work

- **MCP Server integration**: let other agents call SkillGate as a tool
- **GitHub App**: automatic PR comments with Trust Score
- **Team dashboards**: shared policy, continuous monitoring, trend tracking
- **More languages**: extend coverage to Rust, Go, and other popular languages

---

## 7. Conclusion

SkillGate provides the first trust infrastructure for the AI agent skill ecosystem. As the ecosystem grows, we believe that trust infrastructure will be as essential as Snyk and Dependabot are for npm and PyPI today.

By making it easy for users to answer the question *"can I trust this skill?"*, we hope to help the agent ecosystem grow safely and sustainably.

---

## Availability

SkillGate is open source and available at: https://github.com/zhaoxinghua09-cell/skillgate

---

## References

1. Snyk. (2026). *Find and fix vulnerabilities in your dependencies*. https://snyk.io/
2. GitHub. (2026). *CodeQL code scanning*. https://codeql.github.com/
3. GitHub. (2026). *Dependabot version updates*. https://github.com/dependabot
4. Semgrep. (2026). *Lightweight static analysis*. https://semgrep.dev/
5. Anthropic. (2026). *Claude Code skills*. https://docs.anthropic.com/claude-code
6. Cursor. (2026). *Cursor skills*. https://cursor.com/docs/skills
