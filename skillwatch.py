#!/usr/bin/env python3
"""skillwatch — Skill 发布后持续监控

每周定时跑回归测试，对比基线，分数暴跌就告警。

Usage:
    python skillwatch.py watch <skill_dir>
    python skillwatch.py watch <skill_dir> --drop-threshold 10
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_scan(skill_dir: str) -> dict:
    """Run skillgate scan and return parsed JSON result."""
    proc = subprocess.run(
        ["python", "skillgate.py", "scan", skill_dir, "--format", "json"],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent),
    )
    if proc.returncode not in (0, 1):
        return {"error": proc.stderr}
    return json.loads(proc.stdout)


def run_bench(skill_dir: str) -> dict:
    """Run skillbench and return result."""
    baseline_path = Path(skill_dir) / ".skillbench-baseline.json"
    cmd = ["python", "skillbench.py", "run", skill_dir]
    if baseline_path.exists():
        cmd.extend(["--baseline", str(baseline_path)])

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent),
    )
    return {
        "exit_code": proc.returncode,
        "output": proc.stdout,
    }


def watch_skill(skill_dir: str, drop_threshold: int = 10):
    """Watch a skill: scan + bench, compare to baseline, alert on drop."""
    skill_path = Path(skill_dir).resolve()
    if not skill_path.is_dir():
        print(f"错误: 目录不存在 - {skill_dir}", file=sys.stderr)
        sys.exit(2)

    timestamp = datetime.now().isoformat()
    print(f"\n{'='*60}")
    print(f"  SkillWatch 监控报告")
    print(f"  时间: {timestamp}")
    print(f"  Skill: {skill_path.name}")
    print(f"{'='*60}")

    # Gate 1: Security scan
    print(f"\n📋 Gate 1: 安全扫描...")
    scan_result = run_scan(skill_dir)

    if "error" in scan_result:
        print(f"  ❌ 扫描失败: {scan_result['error']}")
        return 1

    current_score = scan_result.get("trust_score", 0)
    grade = scan_result.get("grade", "?")
    print(f"  Trust Score: {current_score}/100 ({grade})")
    print(f"  Critical: {scan_result.get('critical_count', 0)}, High: {scan_result.get('high_count', 0)}")

    # Compare with stored history
    history_path = skill_path / ".skillwatch-history.json"
    history = []
    if history_path.exists():
        history = json.loads(history_path.read_text(encoding="utf-8"))

    prev_score = history[-1]["trust_score"] if history else None
    if prev_score is not None:
        delta = current_score - prev_score
        if delta < -drop_threshold:
            print(f"  🚨 严重退化: {prev_score} → {current_score} ({delta:+.1f})")
            print(f"     跌幅超过阈值 {drop_threshold} 分，需要立即检查！")
        elif delta < 0:
            print(f"  ⚠️  轻微下降: {prev_score} → {current_score} ({delta:+.1f})")
        else:
            print(f"  ✅ 稳定/提升: {prev_score} → {current_score} ({delta:+.1f})")

    # Gate 2: Capability bench
    print(f"\n🧪 Gate 2: 能力评测...")
    bench_result = run_bench(skill_dir)
    if bench_result["exit_code"] == 0:
        print(f"  ✅ 测试全部通过")
    else:
        print(f"  ❌ 有测试失败")
        # Print last few lines of bench output
        lines = bench_result["output"].strip().split("\n")
        for line in lines[-5:]:
            print(f"     {line}")

    # Save history
    history.append({
        "timestamp": timestamp,
        "trust_score": current_score,
        "grade": grade,
        "critical": scan_result.get("critical_count", 0),
        "high": scan_result.get("high_count", 0),
        "bench_pass": bench_result["exit_code"] == 0,
    })
    # Keep last 50 entries
    history = history[-50:]
    history_path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n📊 历史记录已保存: {history_path}")

    # Final verdict
    print(f"\n{'='*60}")
    if scan_result.get("critical_count", 0) > 0 or scan_result.get("high_count", 0) > 0:
        print(f"  ❌ 告警: 发现高风险问题")
        return 1
    elif prev_score and (prev_score - current_score) > drop_threshold:
        print(f"  🚨 告警: Trust Score 暴跌")
        return 1
    else:
        print(f"  ✅ 一切正常")
        return 0


def main():
    ap = argparse.ArgumentParser(description="SkillWatch — Skill 发布后持续监控")
    sub = ap.add_subparsers(dest="command")

    watch_parser = sub.add_parser("watch", help="监控一个 skill")
    watch_parser.add_argument("skill_dir", help="skill 目录路径")
    watch_parser.add_argument("--drop-threshold", type=int, default=10,
                              help="分数跌幅超过此值则告警（默认 10）")

    args = ap.parse_args()

    if args.command == "watch":
        exit_code = watch_skill(args.skill_dir, drop_threshold=args.drop_threshold)
        sys.exit(exit_code)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
