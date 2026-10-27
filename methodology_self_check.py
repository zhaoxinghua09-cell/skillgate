"""
Methodology Self-Check — 方法论自检。
检查这个工具有没有符合 LGD 三律。
LGD: 有籍（自检有记录）、有证（自检有证据）、有门禁（自检就是门禁）。
"""
from pathlib import Path


project_root = Path(__file__).parent


def check_registered() -> dict:
    """检查有籍：有没有记录文件。"""
    records = [
        "traces.json",
        "analytics.json",
        "cost-tracker.json",
        "improvement-log.json",
        "file-watcher-log.json",
        "proactive-executor-log.json",
        "proactive-monitor-log.json"
    ]

    found = []
    for record in records:
        if (project_root / record).exists():
            found.append(record)

    return {
        "name": "有籍（Registered）",
        "check": "有没有记录文件",
        "expected": len(records),
        "found": len(found),
        "passed": len(found) >= 3,  # 至少有 3 个记录文件就算过
        "evidence": f"找到 {len(found)}/{len(records)} 个记录文件"
    }


def check_evidenced() -> dict:
    """检查有证：有没有数据支撑的文档。"""
    evidence_docs = [
        "docs/lgd-evo-methodology.md",
        "docs/proactive-capabilities.md",
        "benchmarks/public-benchmark.md",
        "competitive-analysis.md"
    ]

    found = []
    for doc in evidence_docs:
        if (project_root / doc).exists():
            found.append(doc)

    return {
        "name": "有证（Evidenced）",
        "check": "有没有数据支撑的文档",
        "expected": len(evidence_docs),
        "found": len(found),
        "passed": len(found) >= 2,
        "evidence": f"找到 {len(found)}/{len(evidence_docs)} 个证据文档"
    }


def check_gated() -> dict:
    """检查有门禁：有没有检查机制。"""
    gates = [
        "tests/",  # 测试
        "ci-simulator.py",  # CI 模拟
        "skillgate.py",  # 安全扫描
        "proactive_monitor.py",  # 主动监控
    ]

    found = []
    for gate in gates:
        if (project_root / gate).exists():
            found.append(gate)

    return {
        "name": "有门禁（Gated）",
        "check": "有没有检查机制",
        "expected": len(gates),
        "found": len(found),
        "passed": len(found) >= 3,
        "evidence": f"找到 {len(found)}/{len(gates)} 个门禁"
    }


def run_all_checks() -> list:
    """跑所有检查。"""
    return [
        check_registered(),
        check_evidenced(),
        check_gated()
    ]


def main():
    print("=" * 60)
    print("(")
    print("  🔍 Methodology Self-Check — 方法论自检")
    print("=" * 60)

    print("\n  检查这个工具有没有符合 LGD 三律...\n")

    checks = run_all_checks()
    all_passed = True

    for check in checks:
        status = "✅" if check["passed"] else "❌"
        print(f"  {status} {check['name']}")
        print(f"     检查: {check['check']}")
        print(f"     结果: {check['evidence']}")
        if not check["passed"]:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("  ✅ 全部通过！这个工具符合 LGD 三律")
    else:
        print("  ❌ 有些没通过——需要改进")
    print("=" * 60)


if __name__ == "__main__":
    main()
