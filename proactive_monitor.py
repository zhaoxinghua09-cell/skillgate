"""
Skill Proactive Monitor — 主动监控模块。
不用用户每次都问，系统自己定期检查，主动告诉我们哪里有问题。
LGD: 有籍（每次检查有记录）、有证（检查有数据）、有门禁（发现问题就提醒）。
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


project_root = Path(__file__).parent
monitor_log = project_root / "proactive-monitor-log.json"


def check_error_queue() -> Dict:
    """检查错误队列——有没有待重试的失败任务。"""
    queue_file = project_root / "error_queue.json"

    if not queue_file.exists():
        return {"status": "ok", "message": "错误队列为空"}

    try:
        queue = json.loads(queue_file.read_text(encoding="utf-8"))
    except:
        return {"status": "ok", "message": "错误队列读取失败"}

    pending = [q for q in queue if q["retries"] < q["max_retries"]]

    if not pending:
        return {"status": "ok", "message": "错误队列为空"}

    return {
        "status": "warning",
        "message": f"⚠️ 有 {len(pending)} 个失败任务待重试",
        "pending_count": len(pending)
    }


def check_success_rate() -> Dict:
    """检查成功率——有没有下降。"""
    traces_file = project_root / "traces.json"

    if not traces_file.exists():
        return {"status": "ok", "message": "暂无 traces 数据"}

    try:
        traces = json.loads(traces_file.read_text(encoding="utf-8"))
    except:
        return {"status": "ok", "message": "traces 读取失败"}

    if len(traces) < 5:
        return {"status": "ok", "message": "数据太少，无法判断趋势"}

    success_count = sum(1 for t in traces if t["success"])
    success_rate = success_count / len(traces) * 100

    if success_rate < 80:
        return {
            "status": "critical",
            "message": f"❌ 成功率只有 {success_rate:.0f}%——太低了！",
            "success_rate": success_rate
        }
    elif success_rate < 95:
        return {
            "status": "warning",
            "message": f"⚠️ 成功率 {success_rate:.0f}%——可以更好",
            "success_rate": success_rate
        }
    else:
        return {
            "status": "ok",
            "message": f"✅ 成功率 {success_rate:.0f}%——很好",
            "success_rate": success_rate
        }


def check_cost() -> Dict:
    """检查成本——有没有超预算。"""
    cost_file = project_root / "cost-tracker.json"

    if not cost_file.exists():
        return {"status": "ok", "message": "暂无成本数据"}

    try:
        data = json.loads(cost_file.read_text(encoding="utf-8"))
    except:
        return {"status": "ok", "message": "成本数据读取失败"}

    today = datetime.now().date().isoformat()
    if today not in data:
        return {"status": "ok", "message": "今日暂无成本数据"}

    used_seconds = data[today]["total_seconds"]
    budget = 3600  # 1 小时
    used_percent = used_seconds / budget * 100

    if used_percent > 100:
        return {
            "status": "critical",
            "message": f"❌ 成本超预算了！已用 {used_percent:.0f}%",
            "used_percent": used_percent
        }
    elif used_percent > 80:
        return {
            "status": "warning",
            "message": f"⚠️ 成本快超了——已用 {used_percent:.0f}%",
            "used_percent": used_percent
        }
    else:
        return {
            "status": "ok",
            "message": f"✅ 成本正常——已用 {used_percent:.0f}%",
            "used_percent": used_percent
        }


def run_all_checks() -> List[Dict]:
    """跑所有检查。"""
    results = []

    results.append(check_error_queue())
    results.append(check_success_rate())
    results.append(check_cost())

    # 记录这次检查
    _log_check(results)

    return results


def get_overall_status(results: List[Dict]) -> str:
    """综合判断整体状态。"""
    statuses = [r["status"] for r in results]

    if "critical" in statuses:
        return "critical"
    elif "warning" in statuses:
        return "warning"
    else:
        return "ok"


def _log_check(results: List[Dict]):
    """记录这次检查。"""
    logs = _load_logs()

    log = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": get_overall_status(results),
        "checks": results
    }

    logs.append(log)

    # 只保留最近 100 次检查
    if len(logs) > 100:
        logs = logs[-100:]

    _save_logs(logs)


def _load_logs() -> List[Dict]:
    """加载检查日志。"""
    if not monitor_log.exists():
        return []
    try:
        return json.loads(monitor_log.read_text(encoding="utf-8"))
    except:
        return []


def _save_logs(logs: List[Dict]):
    """保存检查日志。"""
    monitor_log.write_text(
        json.dumps(logs, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    print("=" * 60)
    print("(")
    print("  👀 Skill Proactive Monitor — 主动监控模块")
    print("=" * 60)

    print("\n  主动检查中...\n")

    results = run_all_checks()
    overall = get_overall_status(results)

    for r in results:
        status_icon = {
            "ok": "✅",
            "warning": "⚠️",
            "critical": "❌"
        }.get(r["status"], "ℹ️")
        print(f"  {status_icon} {r['message']}")

    print(f"\n  整体状态: {overall}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
