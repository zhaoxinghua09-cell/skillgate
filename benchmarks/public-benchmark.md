# SkillGate Public Benchmark Suite

标准测试用例集，用来对比不同 skill 的质量和安全性。

## Benchmark Categories

### 1. Security Hardening (20 tests)
测试 skill 的安全防护能力。

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| SEC-001 | Skill doesn't contain eval() calls | No eval found |
| SEC-002 | Skill doesn't hardcode credentials | No hardcoded secrets |
| SEC-003 | Skill doesn't have prompt injection patterns | No injection patterns |
| SEC-004 | Skill has proper frontmatter | name + description present |
| SEC-005 | Skill declares network access needs | network note in SKILL.md |
| SEC-006 | Skill doesn't access sensitive files | No ~/.ssh, ~/.aws access |
| SEC-007 | Skill has license file | LICENSE present |
| SEC-008 | Skill has README | README.md present |
| SEC-009 | Skill has version in frontmatter | version field present |
| SEC-010 | Skill has author in frontmatter | author field present |

### 2. Output Quality (15 tests)
测试 skill 输出的准确性和一致性。

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| QUAL-001 | Output follows skill description | No description-behavior mismatch |
| QUAL-002 | Output is deterministic for same input | Same input → same output |
| QUAL-003 | Error messages are clear | No vague errors |
| QUAL-004 | Output format is consistent | Consistent formatting |
| QUAL-005 | Exit codes are correct | 0 = ok, 1 = error |
| QUAL-006 | Handles edge cases gracefully | No crashes on empty input |
| QUAL-007 | Documents known limitations | Has "Known Limits" section |
| QUAL-008 | Documents output discipline | Has "Output Discipline" section |
| QUAL-009 | No hallucinated information | All facts verifiable |
| QUAL-010 | Bilingual support (EN+ZH) | Covers both languages |

### 3. Usability (10 tests)
测试 skill 的易用性。

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| USE-001 | Has clear usage examples | Code blocks in README |
| USE-002 | Zero or minimal dependencies | No pip install needed |
| USE-003 | Works offline | No network calls needed |
| USE-004 | Fast execution | < 1 second response time |
| USE-005 | Clear error messages | Tells user what went wrong |
| USE-006 | Has help command | --help works |
| USE-007 | Tested on Python 3.8+ | Compatibility declared |
| USE-008 | No magic numbers | Constants are named |
| USE-009 | Code is readable | Comments where needed |
| USE-010 | Has test suite | tests/ directory present |

## Scoring

- Each test: 0 (fail) or 1 (pass)
- Total: 45 points max
- Weighted: Security 40%, Quality 35%, Usability 25%
- Final Trust Score = weighted percentage × 100

## Grade Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A+ | Production ready, recommended |
| 80-89 | A | Good, minor issues |
| 70-79 | B | Acceptable, needs improvements |
| 60-69 | C | Not recommended for production |
| < 60 | D/F | Do not use |

## Usage

```bash
# Run benchmark on a skill
python skillgate.py scan ./my-skill/ --benchmark

# Output: detailed score breakdown
```

## Adding New Tests

PRs welcome! Add new test cases to this file and update the scoring logic.
