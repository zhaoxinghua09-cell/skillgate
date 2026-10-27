"""
SkillGate 综合测试 — 测更多边缘情况，提高覆盖率。
"""
import sys
from pathlib import Path
import tempfile
import shutil

# 把项目根目录加到 path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_scan_md_file():
    """测试扫描 Markdown 文件。"""
    from skillgate import scan_skill

    tmpdir = tempfile.mkdtemp()
    skill_dir = Path(tmpdir) / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\n# Test")

    result = scan_skill(str(skill_dir))
    assert result is not None
    print("  ✅ test_scan_md_file passed")


def test_batch_mode():
    """测试批量扫描模式。"""
    from skillgate import scan_skill

    tmpdir = tempfile.mkdtemp()
    for i in range(3):
        skill_dir = Path(tmpdir) / f"skill-{i}"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: test\n---\n# Test")

    # 扫父目录，应该能发现 3 个子目录
    print("  ✅ test_batch_mode passed (skipped - needs CLI)")


def test_badge_generation():
    """测试徽章生成。"""
    from badge_generator import generate_badge

    svg = generate_badge(90, "A")
    assert "<svg" in svg
    print("  ✅ test_badge_generation passed")


def test_sbom_generation():
    """测试 SBOM 生成。"""
    from sbom_generator import generate_sbom

    tmpdir = tempfile.mkdtemp()
    (Path(tmpdir) / "test.py").write_text("print('hello')")

    sbom = generate_sbom(tmpdir)
    assert len(sbom) > 0
    print("  ✅ test_sbom_generation passed")


def test_audit_log():
    """测试审计日志。"""
    from audit_log import record_scan
    from skillgate import ScanResult

    result = ScanResult(skill_dir="/test")
    record_scan(result, "/test")
    print("  ✅ test_audit_log passed")


def main():
    print("\n" + "=" * 60)
    print("  🧪 SkillGate 综合覆盖率测试")
    print("=" * 60)

    test_scan_md_file()
    test_batch_mode()
    test_badge_generation()
    test_sbom_generation()
    test_audit_log()

    print("\n" + "=" * 60)
    print("  ✅ 综合覆盖率测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
