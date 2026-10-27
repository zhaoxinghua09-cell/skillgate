# SkillGate Best Practices

## Writing Secure Skills

### 1. Never Use Dynamic Code Execution

**Bad:**
```python
result = eval(user_input)
os.system(f"ls {user_dir}")
```

**Good:**
```python
import ast
result = ast.literal_eval(user_input)
subprocess.run(["ls", user_dir])
```

### 2. Never Hardcode Credentials

**Bad:**
```python
API_KEY = "sk-1234567890abcdef"
```

**Good:**
```python
import os
API_KEY = os.getenv("API_KEY")
```

### 3. Declare Your Dependencies

Add a `requirements.txt` with pinned versions:
```
requests==2.31.0
pyyaml==6.0.1
```

### 4. Write Good Frontmatter

```yaml
---
name: my-skill
description: Clear description of what this skill does.
version: 1.0.0
license: MIT
author: Your Name
tags:
  - category
  - subcategory
---
```

### 5. Document Known Limitations

Always include a "Known Limits" section in your SKILL.md:
```markdown
## Known Limits
- This tool only works with English input
- Does not handle edge cases with empty strings
- Not a substitute for human review
```

### 6. Test Your Skill

Add a test suite in `tests/`:
```python
def test_basic_functionality():
    result = run_tool("test input")
    assert "expected output" in result
```

## CI/CD Best Practices

### Block on Critical/High Findings

```yaml
# GitHub Actions
- name: SkillGate Scan
  run: python skillgate.py scan ./my-skill/ --fail-under 80
```

### Generate Badge for README

```markdown
![Trust Score](https://your-badge-server.com/skill/my-skill.svg)
```

### Run on Every PR

Add to your CI workflow to block unsafe skills from being merged.

## Monitoring Best Practices

### Set Up Alerts

Configure webhook alerts when Trust Score drops:
```yaml
alerts:
  webhook_url: "https://hooks.slack.com/..."
  drop_threshold: 10
```

### Track Over Time

Use SkillWatch to run weekly scans and track score trends.

## Performance Best Practices

### Use Incremental Scans

Enable caching to only scan changed files:
```bash
python skillgate.py scan ./my-skill/ --use-cache
```

### Exclude Unnecessary Files

Add to `.skillgate.yml`:
```yaml
paths:
  exclude:
    - "**/node_modules/**"
    - "**/dist/**"
```

## Security Best Practices

### Least Privilege

Your skill should only have the permissions it needs.
- Don't request network access if you don't need it
- Don't read files outside your working directory
- Don't use `eval` when you can use a parser

### Defense in Depth

Even if your skill is trusted, add:
- Input validation
- Output sanitization
- Error handling that doesn't leak information

### Open Source Hygiene

- Sign your commits
- Use two-factor auth for your Git provider
- Review all dependencies
- Keep your skills up to date
