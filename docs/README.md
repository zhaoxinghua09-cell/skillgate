# SkillGate Documentation

## Getting Started

### Installation

```bash
# From source
git clone https://github.com/your-org/skillgate.git
cd skillgate
python skillgate.py scan ./my-skill/

# From PyPI (once published)
pip install skillgate
skillgate scan ./my-skill/
```

### Quick Start

```bash
# Scan a skill
python skillgate.py scan ./my-skill/

# CI mode: fail if score < 80
python skillgate.py scan ./my-skill/ --fail-under 80

# Generate badge for README
python skillgate.py scan ./my-skill/ --badge trust-badge.svg

# Batch scan all skills in a directory
python skillgate.py scan ./skills/ --batch

# AI-friendly output (for agent to relay to user)
python skillgate.py scan ./my-skill/ --format agent

# SARIF output for GitHub Code Scanning
python skillgate.py scan ./my-skill/ --format sarif
```

## Core Concepts

### Trust Score

SkillGate computes a 0-100 Trust Score based on weighted findings:

| Severity | Deduction per finding |
|----------|----------------------|
| CRITICAL | -15 |
| HIGH | -8 |
| MEDIUM | -4 |
| LOW | -1 |

Plus penalties for missing frontmatter (-10) or missing SKILL.md (-20).

### Grades

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A+ | Production ready |
| 80-89 | A | Good quality |
| 70-79 | B | Acceptable |
| 60-69 | C | Needs improvement |
| < 60 | D/F | Not recommended |

## Scanning Rules

### Category 1: Dangerous Code (18 rules)

Detects dangerous function calls that could lead to code execution:
- `eval()`, `exec()`, `compile()`
- `os.system()`, `subprocess shell=True`
- `pickle.load()`, `yaml.load()` (unsafe mode)

### Category 2: Network Calls (18 rules)

Detects network activity that could exfiltrate data:
- `requests`, `urllib`, `httpx`, `aiohttp`
- `socket`, `ftplib`, `smtplib`
- `post()` to external URLs

### Category 3: Credential Leaks (11 rules)

Detects hardcoded secrets and sensitive file access:
- Hardcoded API keys, tokens, passwords
- Access to `~/.ssh/`, `~/.aws/credentials`
- Environment variable access patterns

### Category 4: Filesystem Danger (11 rules)

Detects dangerous file operations:
- `shutil.rmtree()`, `os.remove()`
- Writing to system directories (`/etc/`, `C:\Windows\`)

### Category 5: Prompt Injection (15 rules)

Detects LLM-specific attack patterns:
- "ignore previous instructions"
- "jailbreak", "reveal system prompt"
- "do not tell the user"

### Category 6: Excessive Agency (8 rules)

Detects skills with too much power:
- "delete all files"
- "send all data"
- "run arbitrary commands"

### Category 7: Language-Specific

- **Python**: AST analysis + regex (double layer)
- **JavaScript/TypeScript**: 16 patterns
- **Go**: 11 patterns
- **Rust**: 8 patterns
- **Shell**: `rm -rf`, `curl|sh`, `sudo`

## Integration Guides

### GitHub Actions

See `.github/workflows/skill-gate.yml`

### GitLab CI

See `ci-templates/gitlab-ci.yml`

### Jenkins

See `ci-templates/Jenkinsfile`

### CircleCI

See `ci-templates/circleci-config.yml`

### pre-commit

See `.pre-commit-hooks.yaml`

### MCP Server

```json
{
  "mcpServers": {
    "skillgate": {
      "command": "python",
      "args": ["/path/to/skillgate-mcp.py"]
    }
  }
}
```

## API Reference

### CLI

```
skillgate scan <skill_dir> [OPTIONS]

Options:
  --format terminal|json|markdown|agent|sarif
  --output FILE
  --fail-under N
  --badge FILE.svg
  --batch
```

### Python Library

```python
from skillgate import scan_skill

result = scan_skill("./my-skill/")
print(f"Trust Score: {result.trust_score}/100")
print(f"Grade: {result.grade}")
print(f"Findings: {len(result.findings)}")
```

## FAQ

**Q: Is SkillGate a replacement for code review?**
A: No. It's a safety net that catches obvious issues early. Human review is still needed.

**Q: Why are there so many false positives?**
A: We use pattern matching + AST analysis. For fewer false positives, enable the LLM-as-judge mode.

**Q: Does SkillGate run offline?**
A: Yes, except for OSV.dev dependency scanning (optional).

**Q: What languages are supported?**
A: Python, JavaScript/TypeScript, Go, Rust, Shell, and Markdown.
