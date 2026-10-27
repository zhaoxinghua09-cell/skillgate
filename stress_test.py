"""
Stress Test — 压力测试。
连续跑很多次，看看会不会崩。
LGD: 有籍（测试有记录）、有证（测试有数据）、有门禁（测试通过才算数）。
"""
import time


def test_stress() -> dict:
    """压力测试——连续跑 10 次。"""
    print("=" * 60)
    print("(")
    print("  💪 压力测试——连续跑 10 次，看看会不会崩")
    print("=" * 60)

    import subprocess
    import sys

    successes = 0
    failures = 0
    total_time = 0

    for i in range(1, 11):
        start_time = time.time()

        try:
            result = subprocess.run(
                [sys.executable, "ecosystem.py", "health"],
                capture_output=True,
                text=True,
                timeout=10
            )

            duration = time.time() - start_time
            total_time += duration

            if result.returncode == 0:
                successes += 1
                print(f"    第 {i} 次: ✅ 成功 ({duration:.2f}s)")
            else:
                failures += 1
                print(f"    第 {i} 次: ❌ 失败 ({duration:.2f}s)")

        except Exception as e:
            failures += 1
            print(f"    第 {i} 次: ❌ 崩溃: {e}")

    success_rate = successes / 10 * 100
    avg_time = total_time / 10

    print(f"\n  测试结果：")
    print(f"    成功: {successes}/10 次 ({success_rate:.0f}%)")
    print(f"    失败: {failures}/10 次")
    print(f"    平均时间: {avg_time:.2f} 秒/次")

    if success_rate == 100:
        print(f"\n    ✅ 压力测试通过——连续跑 10 次都没崩")
    elif success_rate >= 90:
        print(f"\n    ⚠️ 压力测试一般——成功率 {success_rate:.0f}%")
    else:
        print(f"\n    ❌ 压力测试不通过——成功率只有 {success_rate:.0f}%")

    print("\n" + "=" * 60)

    return {
        "successes": successes,
        "failures": failures,
        "success_rate": success_rate,
        "avg_time": avg_time
    }


if __name__ == "__main__":
    test_stress()
