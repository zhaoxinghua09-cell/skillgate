"""
SkillGate 错误处理测试。
测试传入坏输入会不会崩溃。
"""
import sys
from pathlib import Path
import tempfile

# 把项目根目录加到 path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_nonexistent_path():
    """测试传入不存在的路径。"""
    from skillgate import scan_skill
    try:
        result = scan_skill("/nonexistent/path/12345")
        # 如果没抛异常，也应该返回一个空结果
        assert result is not None
    except SystemExit:
        # 正常报错退出是预期行为
        pass
    print("  ✅ test_nonexistent_path passed")


def test_empty_file():
    """测试空文件。"""
    from skillgate import scan_skill
    tmpdir = tempfile.mkdtemp()
    empty_file = Path(tmpdir) / "empty.py"
    empty_file.write_text("")
    result = scan_skill(tmpdir)
    assert result is not None
    print("  ✅ test_empty_file passed")


def test_binary_file():
    """测试二进制文件。"""
    from skillgate import scan_skill
    tmpdir = tempfile.mkdtemp()
    binary_file = Path(tmpdir) / "binary.py"
    binary_file.write_bytes(b"\x00\x01\x02\x03\xff\xfe")
    result = scan_skill(tmpdir)
    assert result is not None
    print("  ✅ test_binary_file passed")


def test_very_long_line():
    """测试超长行。"""
    from skillgate import scan_skill
    tmpdir = tempfile.mkdtemp()
    long_file = Path(tmpdir) / "long.py"
    long_line = "x = '" + "a" * 10000 + "'"
    long_file.write_text(long_line)
    result = scan_skill(tmpdir)
    assert result is not None
    print("  ✅ test_very_long_line passed")


def test_special_characters():
    """测试特殊字符。"""
    from skillgate import scan_skill
    tmpdir = tempfile.mkdtemp()
    special_file = Path(tmpdir) / "special.py"
    special_file.write_text("# 中文注释 🎉\nx = '特殊字符'\n")
    result = scan_skill(tmpdir)
    assert result is not None
    print("  ✅ test_special_characters passed")


def main():
    print("\n" + "=" * 60)
    print("  🧪 SkillGate 错误处理测试")
    print("=" * 60)

    test_nonexistent_path()
    test_empty_file()
    test_binary_file()
    test_very_long_line()
    test_special_characters()

    print("\n" + "=" * 60)
    print("  ✅ 所有错误处理测试通过")
    print("=" * 60)


if __name__ == "__main__":
    main()
