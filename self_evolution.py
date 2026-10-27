"""
Skill Self-Evolution — 自我进化模块。
自动分析 traces / analytics / error_queue，给出改进建议。
LGD: 有籍（用 traces 学）、有证（用 analytics 验证）、有门禁（从 error_queue 改进）。
"""
import json
from pathlib import Path
from typing import Dict, List


project_root = Path(__file__).parent


def analyze_usage() -> Dict:
    """从 analytics 里学习：哪个 skill 最常用，哪个最不常用。"""
    analytics_file = project_root / "analytics.json"

    if not analytics_file.exists():
        return {"total_skills": 0, "most_used": None, "least_used": None}

    try:
        data = json.loads(analytics_file.read_text(encoding="utf-8"))
    except:
        return {"total_skills": 0, "most_used": None, "least_used": None}

    if not data:
        return {"total_skills": 0, "most_used": None, "least_used": None}

    skills_by_runs = sorted(
        data.items(),
        key=lambda x: x[1]["total_runs"],
        reverse=True
    )

    return {
        "total_skills": len(data),
        "most_used": skills_by_runs[0][0] if skills_by_runs else None,
        "most_used_runs": skills_by_runs[0][1]["total_runs"] if skills_by_runs else 0,
        "least_used": skills_by_runs[-1][0] if skills_by_runs else None,
        "least_used_runs": skills_by_runs[-1][1]["total_runs"] if skills_by_runs else 0,
    }


def analyze_errors() -> Dict:
    """从 error_queue 里学习：哪里最容易出错。"""
    queue_file = project_root / "error_queue.json"

    if not queue_file.exists():
        return {"total_errors": 0, "error_by_skill": {}, "most_error_prone": None}

    try:
        queue = json.loads(queue_file.read_text(encoding="utf-8"))
    except:
        return {"total_errors": 0, "error_by_skill": {}, "most_error_prone": None}

    error_by_skill = {}
    for item in queue:
        skill = item["skill_name"]
        if skill not in error_by_skill:
            error_by_skill[skill] = 0
        error_by_skill[skill] += 1

    return {
        "total_errors": len(queue),
        "error_by_skill": error_by_skill,
        "most_error_prone": max(error_by_skill, key=error_by_skill.get) if error_by_skill else None
    }


def analyze_traces() -> Dict:
    """从 traces 里学习：什么输入最容易成功，什么输入最容易失败。"""
    traces_file = project_root / "traces.json"

    if not traces_file.exists():
        return {"total_traces": 0, "success_rate": 0}

    try:
        traces = json.loads(traces_file.read_text(encoding="utf-8"))
    except:
        return {"total_traces": 0, "success_rate": 0}

    if not traces:
        return {"total_traces": 0, "success_rate": 0}

    success_count = sum(1 for t in traces if t["success"])
    success_rate = success_count / len(traces) * 100

    return {
        "total_traces": len(traces),
        "success_rate": success_rate,
        "success_count": success_count,
        "failed_count": len(traces) - success_count
    }


def get_improvement_suggestions() -> List[str]:
    """综合分析，给出改进建议。"""
    suggestions = []

    # 从使用情况学
    usage = analyze_usage()
    if usage["most_used"] and usage["most_used_runs"] > 10:
        suggestions.append(
            f"📈 {usage['most_used']} 是最常用的 skill（{usage['most_used_runs']} 次）"
            f"——优先优化这个 skill 的性能和稳定性"
        )

    if usage["least_used"] and usage["least_used_runs"] < 3:
        suggestions.append(
            f"📉 {usage['least_used']} 用得很少（{usage['least_used_runs']} 次）"
            f"——考虑改进它的易用性，或者看看是不是需求不大"
        )

    # 从错误学
    errors = analyze_errors()
    if errors["most_error_prone"]:
        suggestions.append(
            f"⚠️ {errors['most_error_prone']} 最容易出错"
            f"——优先修复这个 skill 的 bug"
        )

    # 从成功率学
    traces = analyze_traces()
    if traces["total_traces"] > 0:
        if traces["success_rate"] < 80:
            suggestions.append(
                f"❌ 成功率只有 {traces['success_rate']:.0f}%"
                f"——需要整体提升运行时的稳定性"
            )
        elif traces["success_rate"] > 95:
            suggestions.append(
                f"✅ 成功率 {traces['success_rate']:.0f}%——很稳定，保持现状"
            )

    return suggestions


def main():
    print("=" * 60)
    print("(")
    print("  🧬 Skill Self-Evolution — 自我进化模块")
    print("=" * 60)

    print("\n  📊 从使用中学（Analytics）：")
    usage = analyze_usage()
    print(f"    总 skill 数: {usage['total_skills']}")
    if usage["most_used"]:
        print(f"    最常用: {usage['most_used']} ({usage['most_used_runs']} 次)")
    if usage["least_used"]:
        print(f"    最不常用: {usage['least_used']} ({usage['least_used_runs']} 次)")

    print("\n  🔴 从错误中学（Error Queue）：")
    errors = analyze_errors()
    print(f"    总错误数: {errors['total_errors']}")
    if errors["most_error_prone"]:
        print(f"    最容易出错: {errors['most_error_prone']}")

    print("\n  📈 从 traces 中学（Traces）：")
    traces = analyze_traces()
    print(f"    总调用数: {traces['total_traces']}")
    if traces["total_traces"] > 0:
        print(f"    成功率: {traces['success_rate']:.1f}%")

    print("\n  💡 改进建议：")
    suggestions = get_improvement_suggestions()
    if suggestions:
        for i, s in enumerate(suggestions, 1):
            print(f"    {i}. {s}")
    else:
        print("    暂无数据，跑几次再来看")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
