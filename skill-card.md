---
name: skillgate
description: Trust infrastructure for AI agent skills — static security scanning, machine-checkable Trust Score, dependency checks, SARIF/JUnit/HTML/JSON reports, dry-run benchmarking, read-only registry watch. Use to audit or score AI agent skills before installing or publishing them.
version: 1.0.21
license: MIT
author: zhaoxinghua09-cell
metadata:
  openclaw:
    requires:
      bins:
        - python
    homepage: https://github.com/zhaoxinghua09-cell/skillgate
---

## Description: <br>
Skillgate is a local-first trust-scoring engine for AI agent skills. It scans a skill folder or repository for security issues (prompt injection, credential leakage, dangerous runtime calls, dependency risk), computes a machine-checkable Trust Score, runs skill benchmarks, and watches registries for newly published or changed skills. Use when the user wants to audit, score, or monitor the safety of AI agent skills before installing or publishing them. <br>
This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoxinghua09-cell](https://clawhub.ai/zhaoxinghua09-cell) <br>

### License/Terms of Use: <br>
MIT <br>

## Use Case: <br>
Developers, platform maintainers, and agent operators use skillgate to check AI agent skills before adoption: scan for prompt injection and credential leaks, obtain a machine-checkable Trust Score, run skill benchmarks, and monitor registries for newly published or changed skills. It complements generic code scanners with agent-skill-specific checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner analyzes untrusted third-party skill code; analysis results depend on rule coverage and are not a guarantee of absolute safety. <br>
Mitigation: Treat skillgate output as one input among several gates; combine with manual review, vendor security audits, and registry-level trust signals before deployment. <br>
Risk: Skillgate reads local files and may flag content that is intentionally benign (false positives). <br>
Mitigation: Review flagged findings before acting; skillgate provides rule identifiers and file locations to support triage. <br>
Risk: Registry watch features make read-only API calls; the scanner itself neither reads nor writes credentials. <br>
Mitigation: Keep the tool updated; manage and rotate any credentials independently and never embed secrets in skills being scanned. <br>

## Reference(s): <br>
- [Skillgate GitHub Repository](https://github.com/zhaoxinghua09-cell/skillgate) <br>
- [Skillgate on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/skillgate) <br>
