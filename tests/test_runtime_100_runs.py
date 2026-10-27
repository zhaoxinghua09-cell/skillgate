"""
Skill Runtime 100 次使用模拟测试。
跑 100 次运行时，看稳定性、一致性、性能。
"""
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_once(query: str):
    """跑一次运行时，返回 (success, time_seconds, error)。"""
    start = time.time()
    try:
        from runtime import run
        run(query)
        elapsed = time.time() - start
        return (True, elapsed, None)
    except Exception as e:
        elapsed = time.time() - start
        return (False, elapsed, str(e))


def main():
    print("=" * 60)
    print("  🧪 Skill Runtime 100 次使用模拟测试")
    print("=" * 60)

    total_runs = 100
    queries = [
        "帮我检查一下 21 CFR 820 的引用格式",
        "做个风险评估，严重度 4，概率 2",
        "帮我扫描一下这个 skill 安全吗",
        "帮我做个术语质检",
    ]

    results = []

    print(f"\n  开始跑 {total_runs} 次运行时...")
    print(f"  测试查询：{len(queries)} 种")
    print()

    for i in range(total_runs):
        query = queries[i % len(queries)]
        success, elapsed, error = run_once(query)
        results.append({
            "run": i + 1,
            "query": query,
            "success": success,
            "time": elapsed,
            "error": error
        })

        if (i + 1) % 10 == 0:
            print(f"    进度: {i+1}/{total_runs}")

    # 统计结果
    print("\n" + "=" * 60)
    print("  📊 测试结果统计")
    print("=" * 60)

    # 成功率
    successes = [r for r in results if r["success"]]
    success_rate = len(successes) / total_runs * 100
    print(f"\n  总运行次数: {total_runs}")
    print(f"  成功次数: {len(successes)}")
    print(f"  成功率: {success_rate:.1f}%")

    # 性能
    times = [r["time"] for r in results]
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    print(f"\n  平均耗时: {avg_time:.3f} 秒")
    print(f"  最快: {min_time:.3f} 秒")
    print(f"  最慢: {max_time:.3f} 秒")

    print("\n" + "=" * 60)
    if success_rate == 100:
        print("  ✅ 全部通过：零错误，运行稳定")
    else:
        print("  ⚠️ 有失败的运行")
    print("=" * 60)


if __name__ == "__main__":
    main()
