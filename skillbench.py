#!/usr/bin/env python3
"""skillbench — Skill 能力评测运行器

自动跑标准测试用例，记录 pass/fail，对比基线。

Usage:
    python skillbench.py run <skill_dir>
    python skillbench.py run <skill_dir> --baseline baseline.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path


@dataclass
class BenchResult:
    test_name: str
    passed: bool
    output: str = ""
    error: str = ""


@dataclass
class SkillBenchResult:
    skill_name: str
    total_tests: int = 0
    passed_tests: int = 0
    results: list[BenchResult] = field(default_factory=list)

    @property
    def pass_rate(self):
        return round(self.passed_tests / self.total_tests * 100, 1) if self.total_tests > 0 else 0


# ── Test definitions per skill ───────────────────────────────────────────

TESTS = {
    "iso14971-risk-matrix": [
        {
            "name": "basic_assess_s4_p2",
            "cmd": ["python", "scripts/risk_matrix.py", "assess", "-s", "4", "-p", "2"],
            "expect_in_output": ["风险评分", "8", "M"],
        },
        {
            "name": "high_risk_s5_p5",
            "cmd": ["python", "scripts/risk_matrix.py", "assess", "-s", "5", "-p", "5"],
            "expect_in_output": ["25", "H"],
        },
        {
            "name": "residual_risk_comparison",
            "cmd": ["python", "scripts/risk_matrix.py", "assess", "-s", "5", "-p", "4", "--rs", "2", "--rp", "1"],
            "expect_in_output": ["剩余风险", "L"],
        },
        {
            "name": "risk_options_hierarchy",
            "cmd": ["python", "scripts/risk_matrix.py", "options"],
            "expect_in_output": ["固有安全", "防护措施", "安全信息"],
        },
    ],
    "medxpert-termbase": [
        {
            "name": "term_lookup_biocompatibility",
            "cmd": ["python", "scripts/term_check.py", "lookup", "biocompatibility"],
            "expect_in_output": ["生物相容性"],
        },
        {
            "name": "term_lookup_chinese",
            "cmd": ["python", "scripts/term_check.py", "lookup", "风险"],
            "expect_in_output": [],
        },
        {
            "name": "stats_inventory",
            "cmd": ["python", "scripts/term_check.py", "stats"],
            "expect_in_output": ["entries"],
        },
    ],
    "reg-citation-normalizer": [
        {
            "name": "normalize_21cfr",
            "cmd": ["python", "scripts/cite_normalize.py", "normalize", "21 CFR 820.30 (a)(6)"],
            "expect_in_output": ["820.30(a)(6)"],
        },
        {
            "name": "normalize_iso",
            "cmd": ["python", "scripts/cite_normalize.py", "normalize", "ISO 13485:2016 clause 7.5.1"],
            "expect_in_output": ["ISO 13485:2016"],
        },
        {
            "name": "parse_json",
            "cmd": ["python", "scripts/cite_normalize.py", "parse", "ISO 13485:2016", "--json"],
            "expect_in_output": ["type", "iso-iec"],
        },
    ],
}


def run_test(skill_dir: Path, test: dict) -> BenchResult:
    cmd = test["cmd"]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(skill_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = proc.stdout + proc.stderr
        passed = True
        for expected in test.get("expect_in_output", []):
            if expected not in output:
                passed = False
                break
        return BenchResult(
            test_name=test["name"],
            passed=passed,
            output=output[:500],  # truncate
        )
    except Exception as e:
        return BenchResult(
            test_name=test["name"],
            passed=False,
            error=str(e),
        )


def run_bench(skill_dir: str) -> SkillBenchResult:
    skill_path = Path(skill_dir).resolve()

    # Find skill name from SKILL.md
    skill_name = skill_path.name
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                for line in content[3:end].splitlines():
                    if line.startswith("name:"):
                        skill_name = line.split(":", 1)[1].strip()
                        break

    result = SkillBenchResult(skill_name=skill_name)

    # Find matching tests
    tests = TESTS.get(skill_name, [])
    if not tests:
        # Try matching by directory name
        for key in TESTS:
            if key in skill_path.name:
                tests = TESTS[key]
                break

    if not tests:
        print(f"⚠️  No benchmark tests defined for: {skill_name}")
        return result

    for test in tests:
        tr = run_test(skill_path, test)
        result.results.append(tr)
        result.total_tests += 1
        if tr.passed:
            result.passed_tests += 1
        status = "✅" if tr.passed else "❌"
        print(f"  {status} {test['name']}")
        if not tr.passed and tr.error:
            print(f"      Error: {tr.error}")

    return result


def main():
    ap = argparse.ArgumentParser(description="SkillBench — Skill 能力评测运行器")
    sub = ap.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="运行 skill benchmark")
    run_parser.add_argument("skill_dir", help="skill 目录路径")
    run_parser.add_argument("--baseline", help="基线 JSON 文件路径")
    run_parser.add_argument("--output", help="输出结果 JSON 文件路径")

    args = ap.parse_args()

    if args.command == "run":
        result = run_bench(args.skill_dir)

        print(f"\n{'='*50}")
        print(f"  SkillBench 结果: {result.skill_name}")
        print(f"  通过: {result.passed_tests}/{result.total_tests} ({result.pass_rate}%)")
        print(f"{'='*50}")

        # Compare with baseline if provided
        if args.baseline and Path(args.baseline).exists():
            baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
            old_rate = baseline.get("pass_rate", 0)
            delta = result.pass_rate - old_rate
            if delta < 0:
                print(f"  ⚠️  退化: {old_rate}% → {result.pass_rate}% ({delta:+.1f}%)")
            elif delta > 0:
                print(f"  📈  提升: {old_rate}% → {result.pass_rate}% ({delta:+.1f}%)")
            else:
                print(f"  →  持平: {result.pass_rate}%")

        # Save results
        output_data = asdict(result)
        if args.output:
            Path(args.output).write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"\n结果已保存: {args.output}")
        else:
            # Save as baseline by default
            baseline_path = Path(args.skill_dir) / ".skillbench-baseline.json"
            baseline_path.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"\n基线已保存: {baseline_path}")

        # Exit code
        if result.total_tests > 0 and result.passed_tests == result.total_tests:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
