# SkillGate Rule Writing Guide

Learn how to write custom rules for SkillGate.

---

## 📋 Rule Format

Rules are written in YAML. Create a file in `.skillgate/rules/`:

```yaml
rules:
  - id: my-custom-rule-001
    description: "Detected dangerous pattern"
    severity: HIGH
    languages: [python]
    patterns:
      - "regex-pattern-1"
      - "regex-pattern-2"
    fix: "Suggested fix message"
```

---

## 🏷️ Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | ✅ | Unique rule identifier (e.g. `python-dangerous-eval`) |
| `description` | ✅ | What this rule detects, shown to the user |
| `severity` | ✅ | `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` |
| `languages` | ❌ | Which languages to scan (default: all) |
| `patterns` | ✅ | List of regex patterns to match |
| `fix` | ❌ | Suggested fix message |

---

## 🎯 Severity Levels

| Level | Score Impact | When to use |
|-------|-------------|-------------|
| `CRITICAL` | -15 | Remote code execution, credential leaks, data exfiltration |
| `HIGH` | -8 | Command injection, SQL injection, unsafe deserialization |
| `MEDIUM` | -3 | XSS, CSRF, weak cryptography |
| `LOW` | -1 | Code smells, TODO comments, debug statements |

---

## 🌐 Languages

Valid language codes:

| Code | Language |
|------|----------|
| `python` | Python |
| `javascript` | JavaScript |
| `typescript` | TypeScript |
| `go` | Go |
| `rust` | Rust |
| `java` | Java |
| `php` | PHP |
| `ruby` | Ruby |
| `csharp` | C# |
| `*` | All languages |

---

## ✍️ Writing Good Regex

### Do:
- Be specific to reduce false positives
- Use word boundaries (`\b`) to avoid partial matches
- Test against real code samples

### Don't:
- Write overly broad patterns (e.g. just `exec`)
- Forget to escape special regex characters
- Match on comments when you only care about code

---

## 📚 Examples

### Example 1: Detect hardcoded API keys

```yaml
rules:
  - id: python-hardcoded-api-key
    description: "Hardcoded API key detected"
    severity: CRITICAL
    languages: [python]
    patterns:
      - "api_key\\s*=\\s*['\"][a-zA-Z0-9]{20,}['\"]"
    fix: "Move to environment variable: os.getenv('API_KEY')"
```

### Example 2: Detect XSS in JavaScript

```yaml
rules:
  - id: js-xss-innerhtml
    description: "Direct innerHTML assignment — risk of XSS"
    severity: MEDIUM
    languages: [javascript, typescript]
    patterns:
      - "\\.innerHTML\\s*="
    fix: "Use textContent() or sanitize input first"
```

### Example 3: Detect unsafe subprocess in Go

```yaml
rules:
  - id: go-subprocess-shell
    description: "exec.Command with shell=True"
    severity: HIGH
    languages: [go]
    patterns:
      - "exec\\.Command\\(\"sh\", \"-c\""
    fix: "Use exec.Command with separate arguments instead of shell=True"
```

---

## 🧪 Testing Your Rules

```bash
# Run SkillGate with your custom rules
skillgate scan ./my-skill/ --rules-dir ./.skillgate/rules/
```

Check that:
1. Your rule fires on bad code samples
2. Your rule does NOT fire on good code samples
3. The description and fix messages are clear and actionable

---

## 📤 Sharing Your Rules

Once you've written a useful rule:
1. Open a PR to add it to the default rule set
2. Or publish it as a separate rule pack
3. Share it with the community!

---

**Happy rule writing! 🎯**
