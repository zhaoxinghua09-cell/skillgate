#!/usr/bin/env python3
"""
本地 CI/CD 模拟器。
模拟 GitHub Actions 的完整 CI 流程：
1. 环境检查
2. 单元测试
3. 集成测试
4. 安全扫描（自扫描）
5. Scorecard
6. 生成报告
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def run_step(name: str, cmd: str) -> bool:
    """Run a CI step and report."""
    print(f"\n{'='*60}")
    print(f"  [CI STEP] {name}")
    print(f"{'='*60}")

    start = datetime.now()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    elapsed = (datetime.now() - start).total_seconds()

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr[:500], "..." if len(result.stderr) > 500 else "")

    if result.returncode == 0:
        print(f"\n  ✅ PASS ({elapsed:.1f}s)")
        return True
    else:
        print(f"\n  ❌ FAIL ({elapsed:.1f}s, exit code: {result.returncode})")
        return False


def main():
    root = Path(__file__).parent
    import os
    os.chdir(root)

    print("=" * 60)
    print("  🔄 Local CI/CD Simulator")
    print("=" * 60)
    print(f"  Started: {datetime.now()}")
    print(f"  Working dir: {root}")
    print()

    steps = [
        ("Environment Check", "python --version"),
        ("Lint Check", "python lint.py"),
        ("Unit Tests", "python tests/test_skillgate.py"),
        ("Integration Tests", "python tests/test_integration.py"),
        ("Error Handling Tests", "python tests/test_error_handling.py"),
        ("Output Format Tests", "python tests/test_output_formats.py"),
        ("Red Team Tests", "python tests/test_red_team.py"),
        ("Strict Benchmark", "python tests/test_strict_benchmark.py"),
        ("E2E Simulation", "python tests/test_e2e_simulation.py"),
        ("Coverage Tests", "python tests/test_coverage.py"),
        ("Security Scan (Self)", "python auto-review.py"),
        ("OpenSSF Scorecard", "python scorecard.py ."),
        ("Performance Benchmark", "python benchmark.py"),
        ("Dependency Audit", "python sbom_generator.py ."),
        ("Pressure Test", "python pressure_test.py"),
    ]

    results = []
    for name, cmd in steps:
        passed = run_step(name, cmd)
        results.append((name, passed))

    # 总结
    print(f"\n{'='*60}")
    print(f"  📊 CI Summary")
    print(f"{'='*60}")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, r in results:
        status = "✅ PASS" if r else "❌ FAIL"
        print(f"  {name:25s} {status}")

    print(f"\n  Total: {passed}/{total} steps passed")

    if passed == total:
        print(f"\n  🎉 CI PASSED — ready to deploy!")
        sys.exit(0)
    else:
        print(f"\n  ⚠️ CI FAILED — fix errors first")
        sys.exit(1)


if __name__ == "__main__":
    main()
