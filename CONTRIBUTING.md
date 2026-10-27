# Contributing to SkillGate

Thank you for your interest in contributing to SkillGate! We welcome all kinds of contributions.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/your-org/skillgate.git
cd skillgate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run the linter
flake8 skillgate.py
```

---

## 📝 Types of Contributions

### 1. Adding New Rules

The easiest way to contribute is adding new security rules.

**Where to add:**
- Built-in rules: add to `skillgate.py` in the appropriate `*_PATTERNS` list
- Custom rule examples: add YAML files to `rules/`

**Rule format (YAML):**
```yaml
rules:
  - id: category-rule-number
    description: "What this rule detects"
    severity: CRITICAL | HIGH | MEDIUM | LOW
    languages: [python, javascript]
    patterns:
      - "regex-pattern-here"
    fix: "Suggested fix"
```

**Guidelines:**
- Use specific, precise regex patterns
- Write clear, actionable descriptions
- Test against real code samples
- Cite CVE or vulnerability references when applicable

### 2. Adding New Language Support

1. Create a new file: `<language>_analyzer.py`
2. Implement the scan function: `scan_<lang>_file(filepath: Path) -> List[Tuple]`
3. Add dangerous patterns for that language
4. Register in `skillgate.py` main scan function
5. Add tests in `tests/test_skillgate.py`

### 3. Improving Documentation

- Fix typos or clarify confusing parts
- Add more examples
- Translate to other languages
- Write tutorials or blog posts

### 4. Bug Reports & Feature Requests

- Open an issue on GitHub
- Include steps to reproduce (for bugs)
- Describe expected vs actual behavior

---

## 🧪 Testing

Before submitting a PR:

```bash
# Run all tests
pytest tests/ -v

# Test against real sample skills
python skillgate.py scan ./tests/fixtures/
```

Make sure all tests pass and your new code has test coverage.

---

## 🎨 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to all public functions
- Keep functions small and focused

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 💬 Questions?

Open a discussion on GitHub or reach out to the maintainers.

**Happy hacking! 🎉**
