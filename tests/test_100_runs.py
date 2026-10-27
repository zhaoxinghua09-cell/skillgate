"""
SkillGate 100 次使用模拟测试。
跑 100 次扫描，看稳定性、一致性、性能。
"""
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_scan(skill_path: str):
    """跑一次扫描，返回 (trust_score, time_seconds, error)"""
    start = time.time()
    try:
        from skillgate import scan_skill
        result = scan_skill(skill_path)
        elapsed = time.time() - start
        return (result.trust_score, elapsed, None)
    except Exception as e:
        elapsed = time.time() - start
        return (None, elapsed, str(e))


def main():
    print("=" * 60)
    print("  🧪 SkillGate 100 次使用模拟测试")
    print("=" * 60)

    # 测试目标：我们自己的三个自研 skill
    test_targets = [
        ("iso14971-risk-matrix", r"C:\Users\Administrator\.agents\skills\skills-iso14971-risk-matrix-master-956b23753b38c681010bc1f1bf41c801b273780f"),
        ("medxpert-termbase", r"C:\Users\Administrator\.agents\skills\skills-medxpert-termbase-master-a1b96dcc19f833337027b4cf23c50bfddef8f8f0"),
        ("reg-citation-normalizer", r"C:\Users\Administrator\.agents\skills\skills-reg-citation-normalizer-master-809eea69d1597f344da648041dfec729078b1103"),
    ]

    total_runs = 100
    results = []

    print(f"\n  开始跑 {total_runs} 次扫描...")
    print(f"  测试目标：3 个自研 skill")
    print()

    for i in range(total_runs):
        # 轮着扫三个 skill
        target_name, target_path = test_targets[i % 3]
        score, elapsed, error = run_scan(target_path)
        results.append({
            "run": i + 1,
            "target": target_name,
            "score": score,
            "time": elapsed,
            "error": error
        })

        # 每 10 次打印一次进度
        if (i + 1) % 10 == 0:
            print(f"    进度: {i+1}/{total_runs}")

    # 统计结果
    print("\n" + "=" * 60)
    print("  📊 测试结果统计")
    print("=" * 60)

    # 错误率
    errors = [r for r in results if r["error"] is not None]
    error_rate = len(errors) / total_runs * 100
    print(f"\n  总运行次数: {total_runs}")
    print(f"  错误次数: {len(errors)}")
    print(f"  错误率: {error_rate:.1f}%")

    # 一致性
    scores = [r["score"] for r in results if r["score"] is not None]
    unique_scores = set(scores)
    print(f"\n  分数种类: {len(unique_scores)} 种")
    print(f"  分数列表: {sorted(unique_scores)}")

    # 性能
    times = [r["time"] for r in results]
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    print(f"\n  平均耗时: {avg_time:.3f} 秒")
    print(f"  最快: {min_time:.3f} 秒")
    print(f"  最慢: {max_time:.3f} 秒")

    # 按目标分组
    print(f"\n  按目标分组:")
    for target_name, _ in test_targets:
        target_results = [r for r in results if r["target"] == target_name]
        target_scores = [r["score"] for r in target_results]
        unique = set(target_scores)
        print(f"    {target_name}: {len(target_scores)} 次, 分数 {unique}")

    print("\n" + "=" * 60)
    if error_rate == 0 and len(unique_scores) == 1:
        print("  ✅ 全部通过：零错误，分数一致")
    else:
        print("  ⚠️ 有问题需要检查")
    print("=" * 60)


if __name__ == "__main__":
    main()
