"""
Skill Analytics — 使用记录。
记录每个 skill 被用了多少次，有证（evidenced）。
"""
import json
from pathlib import Path
from datetime import datetime


project_root = Path(__file__).parent
analytics_file = project_root / "analytics.json"


def log_usage(skill_name: str, action: str = "run"):
    """记录一次使用。"""
    data = _load()

    if skill_name not in data:
        data[skill_name] = {
            "total_runs": 0,
            "success_runs": 0,
            "failed_runs": 0,
            "history": []
        }

    data[skill_name]["total_runs"] += 1
    data[skill_name]["history"].append({
        "timestamp": datetime.now().isoformat(),
        "action": action
    })

    # 只保留最近 100 条历史
    if len(data[skill_name]["history"]) > 100:
        data[skill_name]["history"] = data[skill_name]["history"][-100:]

    _save(data)


def log_success(skill_name: str):
    """记录一次成功。"""
    data = _load()
    if skill_name in data:
        data[skill_name]["success_runs"] += 1
        _save(data)


def log_failure(skill_name: str):
    """记录一次失败。"""
    data = _load()
    if skill_name in data:
        data[skill_name]["failed_runs"] += 1
        _save(data)


def get_stats() -> dict:
    """获取使用统计。"""
    return _load()


def _load() -> dict:
    """加载数据。"""
    if not analytics_file.exists():
        return {}
    try:
        return json.loads(analytics_file.read_text(encoding="utf-8"))
    except:
        return {}


def _save(data: dict):
    """保存数据。"""
    analytics_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    print("=" * 60)
    print("  📊 Skill Analytics — 使用记录")
    print("=" * 60)

    stats = get_stats()

    if not stats:
        print("\n  暂无使用记录")
        return

    print(f"\n  总 skill 数: {len(stats)}")
    print(f"\n  使用统计：")
    for skill_name, data in stats.items():
        success_rate = (data["success_runs"] / data["total_runs"] * 100) if data["total_runs"] > 0 else 0
        print(f"    {skill_name}:")
        print(f"      总运行: {data['total_runs']} 次")
        print(f"      成功: {data['success_runs']} 次 ({success_rate:.0f}%)")
        print(f"      失败: {data['failed_runs']} 次")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
