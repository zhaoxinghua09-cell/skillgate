"""
Skill Proactive Recommender — 主动推荐。
从使用历史推断用户需求，主动推荐可能需要的 skill。
LGD: 有籍（推荐有记录）、有证（从 analytics 学）、有门禁（推荐要准确）。
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


project_root = Path(__file__).parent


def get_recommendations() -> List[str]:
    """从使用历史推断需求，主动推荐。"""
    recommendations = []

    # 从 analytics 学：用户常用什么
    analytics_file = project_root / "analytics.json"
    if not analytics_file.exists():
        return ["💡 开始用一些 skill 吧，我会记住你常用的，然后主动推荐"]

    try:
        analytics = json.loads(analytics_file.read_text(encoding="utf-8"))
    except:
        return []

    if not analytics:
        return ["💡 开始用一些 skill 吧，我会记住你常用的，然后主动推荐"]

    # 找到最常用的 skill
    most_used = max(analytics.items(), key=lambda x: x[1]["total_runs"])
    skill_name = most_used[0]
    runs = most_used[1]["total_runs"]

    if runs > 5:
        recommendations.append(
            f"💡 你常用 {skill_name}（{runs} 次了）——要不要我帮你跑一遍？"
        )

    # 找到很久没用的 skill
    for skill_name, data in analytics.items():
        if data["total_runs"] < 2:
            recommendations.append(
                f"💡 {skill_name} 你只用过 {data['total_runs']} 次——要不要试试？"
            )

    return recommendations


def get_anticipation() -> List[str]:
    """预测用户可能需要什么，提前做。"""
    anticipation = []

    # 如果用户最近用过 reg-citation-normalizer，可能接下来要检查文档
    analytics_file = project_root / "analytics.json"
    if not analytics_file.exists():
        return []

    try:
        analytics = json.loads(analytics_file.read_text(encoding="utf-8"))
    except:
        return []

    if "reg-citation-normalizer" in analytics:
        anticipation.append(
            f"🔮 你刚用过 reg-citation-normalizer——是不是要检查文档里的引用格式？"
        )

    if "iso14971-risk-matrix" in analytics:
        anticipation.append(
            f"🔮 你刚用过 iso14971-risk-matrix——是不是要做风险管理评估？"
        )

    return anticipation


def main():
    print("=" * 60)
    print("(")
    print("  💡 Skill Proactive Recommender — 主动推荐")
    print("=" * 60)

    print("\n  🎯 主动推荐：")
    recs = get_recommendations()
    for r in recs:
        print(f"    {r}")

    print("\n  🔮 预测你可能需要：")
    anticipations = get_anticipation()
    if anticipations:
        for a in anticipations:
            print(f"    {a}")
    else:
        print("    暂无预测")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
