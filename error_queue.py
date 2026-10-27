"""
Skill Error Queue — 错误队列。
失败的任务放到队列里，能重试，有门禁（gated）。
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


project_root = Path(__file__).parent
queue_file = project_root / "error_queue.json"


def add_to_queue(skill_name: str, input_data: str, error: str, retries: int = 0):
    """把失败的任务加到错误队列。"""
    queue = _load()

    item = {
        "id": len(queue) + 1,
        "timestamp": datetime.now().isoformat(),
        "skill_name": skill_name,
        "input": input_data,
        "error": error,
        "retries": retries,
        "max_retries": 3
    }

    queue.append(item)
    _save(queue)


def get_pending() -> List[Dict]:
    """获取待重试的任务。"""
    queue = _load()
    return [q for q in queue if q["retries"] < q["max_retries"]]


def mark_success(item_id: int):
    """标记任务成功，从队列里移除。"""
    queue = _load()
    queue = [q for q in queue if q["id"] != item_id]
    _save(queue)


def mark_retry(item_id: int):
    """标记任务重试一次。"""
    queue = _load()
    for q in queue:
        if q["id"] == item_id:
            q["retries"] += 1
    _save(queue)


def _load() -> List[Dict]:
    """加载队列。"""
    if not queue_file.exists():
        return []
    try:
        return json.loads(queue_file.read_text(encoding="utf-8"))
    except:
        return []


def _save(queue: List[Dict]):
    """保存队列。"""
    queue_file.write_text(
        json.dumps(queue, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    print("=" * 60)
    print("  ⚠️ Skill Error Queue — 错误队列")
    print("=" * 60)

    pending = get_pending()

    if not pending:
        print("\n  ✅ 队列为空，没有待重试的任务")
        return

    print(f"\n  待重试任务: {len(pending)} 个")
    for item in pending:
        print(f"    #{item['id']} {item['skill_name']} (已重试 {item['retries']}/{item['max_retries']} 次)")
        print(f"       错误: {item['error'][:50]}...")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
