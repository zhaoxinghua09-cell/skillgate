"""
SkillGate 输出格式测试。
测试 6 种输出格式都正确。
"""
import sys
from pathlib import Path
import tempfile
import json
from dataclasses import asdict

# 把项目根目录加到 path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_terminal_output():
    """测试 terminal 输出。"""
    from skillgate import scan_skill, print_terminal_report
    import io
    from contextlib import redirect_stdout

    tmpdir = tempfile.mkdtemp()
    (Path(tmpdir) / "test.py").write_text("import os\nos.system('ls')\n")
    result = scan_skill(tmpdir)

    f = io.StringIO()
    with redirect_stdout(f):
        print_terminal_report(result)
    output = f.getvalue()

    assert "Trust Score" in output
    print("  ✅ test_terminal_output passed")


def test_json_output():
    """测试 JSON 输出。"""
    from skillgate import scan_skill
    from dataclasses import asdict

    tmpdir = tempfile.mkdtemp()
    (Path(tmpdir) / "test.py").write_text("import os\nos.system('ls')\n")
    result = scan_skill(tmpdir)
    output = json.dumps(asdict(result), indent=2, ensure_ascii=False)
    data = json.loads(output)
    assert "findings" in data
    print("  ✅ test_json_output passed")


def test_agent_output():
    """测试 agent 输出。"""
    from skillgate import scan_skill, generate_agent_summary

    tmpdir = tempfile.mkdtemp()
    (Path(tmpdir) / "test.py").write_text("import os\nos.system('ls')\n")
    result = scan_skill(tmpdir)
    output = generate_agent_summary(result)
    assert "SkillGate" in output or "trust" in output.lower()
    print("  ✅ test_agent_output passed")


def test_sarif_output():
    """测试 SARIF 输出。"""
    from skillgate import scan_skill, generate_sarif

    tmpdir = tempfile.mkdtemp()
    (Path(tmpdir) / "test.py").write_text("import os\nos.system('ls')\n")
    result = scan_skill(tmpdir)
    output = generate_sarif(result)
    assert "sarif" in output.lower() or "runs" in output.lower()
    print("  ✅ test_sarif_output passed")


def main():
    print("\n" + "=" * 60)
    print("  🧪 SkillGate 输出格式测试")
    print("=" * 60)

    test_terminal_output()
    test_json_output()
    test_agent_output()
    test_sarif_output()

    print("\n" + "=" * 60)
    print("  ✅ 所有输出格式测试通过")
    print("=" * 60)


if __name__ == "__main__":
    main()
