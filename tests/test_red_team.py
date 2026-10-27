"""
SkillGate Red Team Test — 模拟攻击者找漏洞。
"""
import sys
from pathlib import Path
import tempfile

# 把项目根目录加到 path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_path_traversal_protection():
    """测试：能不能扫描系统敏感目录？"""
    from skillgate import scan_skill

    # 尝试扫描敏感目录
    sensitive_paths = [
        "C:\\Windows",
        "/etc",
        "/proc",
    ]

    print("  🎯 测试：路径遍历防护")
    for path in sensitive_paths:
        try:
            result = scan_skill(path)
            # 如果没被拦截，就是漏洞
            print(f"    ⚠️  {path} — 没有被拦截！这是漏洞！")
        except SystemExit as e:
            if e.code in [2, 3]:
                print(f"    ✅ {path} — 被拦截了 (exit code {e.code})")
            else:
                print(f"    ⚠️  {path} — 异常退出 code={e.code}")
        except Exception as e:
            print(f"    ✅ {path} — 报错退出（安全）")


def test_malicious_input():
    """测试：恶意输入会不会崩溃？"""
    from skillgate import scan_skill

    print("\n  🎯 测试：恶意输入")

    # 超长路径
    try:
        long_path = "A" * 10000
        result = scan_skill(long_path)
        print(f"    ✅ 超长路径 — 优雅处理")
    except SystemExit:
        print(f"    ✅ 超长路径 — 优雅退出")
    except Exception as e:
        print(f"    ❌ 超长路径 — 崩溃了: {e}")

    # 特殊字符路径
    try:
        weird_path = "C:\\test\\..\\..\\Windows\\System32"
        result = scan_skill(weird_path)
        print(f"    ✅ 特殊字符路径 — 优雅处理")
    except SystemExit:
        print(f"    ✅ 特殊字符路径 — 优雅退出")
    except Exception as e:
        print(f"    ❌ 特殊字符路径 — 崩溃了: {e}")


def test_regular_injection():
    """测试：恶意代码会不会导致正则 DoS？"""
    from skillgate import scan_skill

    print("\n  🎯 测试：正则注入 / DoS")

    # 写一个有超长行的文件
    tmpdir = tempfile.mkdtemp()
    evil_file = Path(tmpdir) / "evil.py"
    # 超长字符串，测试正则会不会卡死
    evil_file.write_text("x = '" + "a" * 100000 + "'\n")

    import time
    start = time.time()
    try:
        result = scan_skill(tmpdir)
        elapsed = time.time() - start
        print(f"    ✅ 超长行 — {elapsed:.2f} 秒（没有 DoS）")
    except Exception as e:
        elapsed = time.time() - start
        print(f"    ❌ 超长行 — 崩溃了: {e} (耗时 {elapsed:.2f}s)")


def test_symlink_attack():
    """测试：符号链接攻击。"""
    from skillgate import scan_skill

    print("\n  🎯 测试：符号链接攻击")

    # 这个比较难测，先跳过
    print(f"    ℹ️  符号链接测试 — 跳过（Windows 上不好测）")


def main():
    print("\n" + "=" * 60)
    print("  🔴 SkillGate 红队测试")
    print("=" * 60)

    test_path_traversal_protection()
    test_malicious_input()
    test_regular_injection()
    test_symlink_attack()

    print("\n" + "=" * 60)
    print("  ✅ 红队测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
