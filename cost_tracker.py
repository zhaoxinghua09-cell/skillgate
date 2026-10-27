"""
Skill Cost Tracker — 成本追踪。
记录每个 skill 跑了多少次，花了多少时间。
LGD: 有籍（每次运行有记录）、有证（数据有实跑）、有门禁（成本超了有提醒）。
"""
import json
from pathlib import Path
from datetime import datetime


project_root = Path(__file__).parent
cost_file = project_root / "cost-tracker.json"


# 成本阈值（本地工具，主要是时间成本）
DAILY_TIME_BUDGET_SECONDS = 3600  # 每天最多跑 1 小时


def record_run(skill_name: str, duration_seconds: float):
    """记录一次运行的成本。"""
    data = _load()
    today = datetime.now().date().isoformat()

    if today not in data:
        data[today] = {
            "total_seconds": 0,
            "runs": {}
        }

    data[today]["total_seconds"] += duration_seconds

    if skill_name not in data[today]["runs"]:
        data[today]["runs"][skill_name] = {
            "count": 0,
            "total_seconds": 0
        }

    data[today]["runs"][skill_name]["count"] += 1
    data[today]["runs"][skill_name]["total_seconds"] += duration_seconds

    _save(data)


def get_daily_cost(date: str = None) -> dict:
    """获取某天的成本。"""
    data = _load()
    if not date:
        date = datetime.now().date().isoformat()

    if date not in data:
        return {"total_seconds": 0, "runs": {}}

    return data[date]


def check_budget() -> tuple[bool, float]:
    """检查是否超了预算。返回 (是否超了, 已用百分比)。"""
    today_cost = get_daily_cost()
    used_seconds = today_cost["total_seconds"]
    used_percent = used_seconds / DAILY_TIME_BUDGET_SECONDS * 100

    return used_percent > 100, used_percent


def _load() -> dict:
    """加载成本数据。"""
    if not cost_file.exists():
        return {}
    try:
        return json.loads(cost_file.read_text(encoding="utf-8"))
    except:
        return {}


def _save(data: dict):
    """保存成本数据。"""
    cost_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    print("=" * 60)
    print("  💰 Skill Cost Tracker — 成本追踪")
    print("=" * 60)

    today_cost = get_daily_cost()
    used_percent = today_cost["total_seconds"] / DAILY_TIME_BUDGET_SECONDS * 100

    print(f"\n  今日已用时间: {today_cost['total_seconds']:.1f} 秒")
    print(f"  今日预算: {DAILY_TIME_BUDGET_SECONDS} 秒（1 小时）")
    print(f"  已用预算: {used_percent:.1f}%")

    if used_percent > 100:
        print(f"  ⚠️ 已超预算！")
    elif used_percent > 80:
        print(f"  ⚠️ 快超预算了！")
    else:
        print(f"  ✅ 预算充足")

    if today_cost["runs"]:
        print(f"\n  按 skill 统计：")
        for skill_name, data in today_cost["runs"].items():
            print(f"    {skill_name}: {data['count']} 次, {data['total_seconds']:.1f} 秒")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
