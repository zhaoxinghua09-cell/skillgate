"""
代码风格 Lint 检查。
检查：行长度、tab/space、尾随空格等。
"""

from pathlib import Path


def lint_file(file_path: Path) -> list:
    """Lint a single Python file."""
    issues = []
    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    for i, line in enumerate(lines, 1):
        # 行太长
        if len(line) > 120:
            issues.append(f"Line {i}: too long ({len(line)} chars > 120)")

        # 尾随空格
        if line.endswith(" ") or line.endswith("\t"):
            issues.append(f"Line {i}: trailing whitespace")

        # Tab 缩进
        if line.startswith("\t"):
            issues.append(f"Line {i}: uses tab instead of spaces")

    return issues


def run_lint() -> int:
    """Run lint on all Python files in the project."""
    root = Path(__file__).parent
    py_files = list(root.glob("*.py")) + list((root / "tests").glob("*.py"))

    total_issues = 0

    print("=" * 50)
    print("  🔍 Lint Check")
    print("=" * 50)

    for py_file in py_files:
        issues = lint_file(py_file)
        if issues:
            print(f"\n  {py_file.name}:")
            for issue in issues[:5]:  # 只显示前 5 个
                print(f"    - {issue}")
            if len(issues) > 5:
                print(f"    ... and {len(issues) - 5} more")
            total_issues += len(issues)

    print(f"\n  Total issues: {total_issues}")

    if total_issues == 0:
        print("  ✅ Lint passed")
        return 0
    else:
        print("  ⚠️ Lint warnings (not blocking)")
        return 0  # 不阻断，只是警告


if __name__ == "__main__":
    exit(run_lint())
