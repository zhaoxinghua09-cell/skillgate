#!/usr/bin/env python3
"""
SkillGate 全量自动化测试脚本。
一键跑：单元测试 + 集成测试 + 性能基准 + 自扫描。
"""

import subprocess
import sys
from pathlib import Path


def run_test(name: str, cmd: str) -> bool:
    """Run a test and report result."""
    print(f"\n{'='*60}")
    print(f"  Running: {name}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode == 0:
        print(f"  ✅ {name} PASSED")
        return True
    else:
        print(f"  ❌ {name} FAILED (exit code: {result.returncode})")
        return False


def main():
    root = Path(__file__).parent
    os.chdir(root)

    results = []

    # 1. 单元测试
    results.append(("单元测试", run_test("单元测试 (25 个)", "python tests/test_skillgate.py")))

    # 2. 性能基准
    results.append(("性能基准", run_test("性能基准测试", "python benchmark.py")))

    # 3. Scorecard
    results.append(("Scorecard", run_test("OpenSSF Scorecard", "python scorecard.py .")))

    # 4. 自扫描
    results.append(("自扫描", run_test("自扫描（扫自己）", "python skillgate.py scan . --format agent")))

    # 5. 审计日志
    results.append(("审计日志", run_test("审计日志检查", "python audit_log.py")))

    # 总结
    print(f"\n{'='*60}")
    print(f"  全量测试总结")
    print(f"{'='*60}")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, r in results:
        status = "✅ PASS" if r else "❌ FAIL"
        print(f"  {name:20s} {status}")

    print(f"\n  通过: {passed}/{total}")

    if passed == total:
        print(f"\n  🎉 全部通过！")
        sys.exit(0)
    else:
        print(f"\n  ⚠️ 有 {total - passed} 项失败")
        sys.exit(1)


if __name__ == "__main__":
    import os
    main()
