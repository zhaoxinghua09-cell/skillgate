"""
SkillGate AutoFix Pro — 生成真实代码 diff 的自动修复。
"""
import difflib
from pathlib import Path


def generate_fix_diff(filepath: Path, line_number: int, old_code: str, new_code: str) -> str:
    """Generate a unified diff for a code fix."""
    try:
        original = filepath.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    except Exception:
        return ""

    # Create modified version
    modified = list(original)
    if 0 < line_number <= len(modified):
        modified[line_number - 1] = new_code + "\n"

    # Generate diff
    diff = difflib.unified_diff(
        original,
        modified,
        fromfile=str(filepath) + " (before)",
        tofile=str(filepath) + " (after)",
        lineterm=""
    )

    return "".join(diff)


def fix_hardcoded_secret(filepath: Path, line_number: int, old_line: str) -> str:
    """Fix hardcoded secret by replacing with env var."""
    import re
    # Extract variable name
    match = re.match(r"(\w+)\s*=\s*['\"]([^'\"]+)['\"]", old_line.strip())
    if match:
        var_name = match.group(1)
        new_line = f'{var_name} = os.getenv("{var_name.upper()}")'
        return generate_fix_diff(filepath, line_number, old_line, new_line)
    return ""


def fix_eval_to_literal_eval(filepath: Path, line_number: int, old_line: str) -> str:
    """Fix eval() by replacing with ast.literal_eval()."""
    if "eval(" in old_line:
        new_line = old_line.replace("eval(", "ast.literal_eval(")
        return generate_fix_diff(filepath, line_number, old_line, new_line)
    return ""


def fix_subprocess_shell_true(filepath: Path, line_number: int, old_line: str) -> str:
    """Fix subprocess shell=True by using list args."""
    if "shell=True" in old_line:
        # Simple fix: remove shell=True
        new_line = old_line.replace(", shell=True", "").replace("shell=True, ", "").replace("shell=True", "")
        return generate_fix_diff(filepath, line_number, old_line, new_line)
    return ""


class AutoFixEngine:
    """Main auto-fix engine."""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

    def fix(self, finding: dict) -> str:
        """Try to auto-fix a finding."""
        category = finding.get("category", "")
        line = finding.get("line", 0)

        if not line:
            return ""

        try:
            lines = self.filepath.read_text(encoding="utf-8", errors="replace").splitlines()
            old_line = lines[line - 1] if line <= len(lines) else ""
        except Exception:
            return ""

        # Route to specific fixer
        if "credential" in category:
            return fix_hardcoded_secret(self.filepath, line, old_line)
        elif "dangerous-code" in category and "eval" in finding.get("message", ""):
            return fix_eval_to_literal_eval(self.filepath, line, old_line)
        elif "subprocess" in finding.get("message", ""):
            return fix_subprocess_shell_true(self.filepath, line, old_line)

        return ""


if __name__ == "__main__":
    print("AutoFix Pro — real code diff generation")
