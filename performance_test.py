"""
Performance Test — 性能测试。
测试扫一个大项目要多久。
LGD: 有籍（测试有记录）、有证（测试有数据）、有门禁（测试通过才算数）。
"""
import time
from pathlib import Path


project_root = Path(__file__).parent


def test_scan_performance() -> dict:
    """测试扫描性能。"""
    print("=" * 60)
    print("(")
    print("  ⚡ 性能测试——扫一个大项目要多久")
    print("=" * 60)

    # 扫我们自己的项目（挺大的，有几十个 py 文件）
    start_time = time.time()

    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "skillgate.py", "scan", "."],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    duration = time.time() - start_time

    # 数一下扫了多少个文件
    file_count = len(list(project_root.glob("*.py")))

    print(f"\n  测试结果：")
    print(f"    扫了多少文件: {file_count} 个 .py 文件")
    print(f"    花了多少时间: {duration:.2f} 秒")
    print(f"    平均速度: {file_count / duration:.1f} 文件/秒")

    # 判断性能好不好
    if duration < 5:
        print(f"\n    ✅ 性能很好——扫完只用了 {duration:.1f} 秒")
    elif duration < 10:
        print(f"\n    ⚠️ 性能一般——花了 {duration:.1f} 秒")
    else:
        print(f"\n    ❌ 性能不好——花了 {duration:.1f} 秒，太慢了")

    print("\n" + "=" * 60)

    return {
        "file_count": file_count,
        "duration_seconds": duration,
        "files_per_second": file_count / duration
    }


if __name__ == "__main__":
    test_scan_performance()
