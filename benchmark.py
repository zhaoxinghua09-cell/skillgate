"""
SkillGate 性能基准测试。
测量扫描速度、内存占用、规则数量等指标。
"""

import time
import tracemalloc
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))


def benchmark_scan_speed():
    """测量扫描一个标准 skill 目录需要多久。"""
    from skillgate import scan_skill

    # 用一个小的测试目录
    test_dir = Path(__file__).parent / "tests" / "fixtures"
    if not test_dir.exists():
        test_dir = Path(__file__).parent

    start = time.time()
    result = scan_skill(str(test_dir))
    elapsed = time.time() - start

    print(f"  扫描耗时: {elapsed:.2f} 秒")
    print(f"  文件数量: {result.files_scanned}")
    print(f"  发现问题: {len(result.findings)}")

    return elapsed


def benchmark_memory():
    """测量内存占用。"""
    from skillgate import scan_skill

    tracemalloc.start()
    scan_skill(str(Path(__file__).parent))
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"  当前内存: {current / 1024 / 1024:.2f} MB")
    print(f"  峰值内存: {peak / 1024 / 1024:.2f} MB")

    return peak


def benchmark_rule_count():
    """统计规则数量。"""
    from skillgate import DANGEROUS_CODE_PATTERNS, NETWORK_PATTERNS

    total = len(DANGEROUS_CODE_PATTERNS) + len(NETWORK_PATTERNS)
    print(f"  危险代码规则: {len(DANGEROUS_CODE_PATTERNS)} 条")
    print(f"  网络规则: {len(NETWORK_PATTERNS)} 条")
    print(f"  核心规则总数: {total} 条")

    return total


def run_all_benchmarks():
    """跑所有性能基准测试。"""
    print("=" * 50)
    print("  SkillGate 性能基准测试")
    print("=" * 50)
    print()

    print("📊 1. 扫描速度")
    benchmark_scan_speed()
    print()

    print("📊 2. 内存占用")
    benchmark_memory()
    print()

    print("📊 3. 规则数量")
    benchmark_rule_count()
    print()

    print("=" * 50)
    print("  ✅ 基准测试完成")
    print("=" * 50)


if __name__ == "__main__":
    run_all_benchmarks()
