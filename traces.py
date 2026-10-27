"""
Skill Traces — 调用日志。
记录每次调用的详细信息，有籍（registered）。
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


project_root = Path(__file__).parent
traces_file = project_root / "traces.json"


def log_trace(skill_name: str, input_data: str, output_data: str, success: bool, duration: float, error: str = None):
    """记录一次调用 trace。"""
    traces = _load()

    trace = {
        "timestamp": datetime.now().isoformat(),
        "skill_name": skill_name,
        "input": input_data,
        "output": output_data,
        "success": success,
        "duration_seconds": duration,
        "error": error
    }

    traces.append(trace)

    # 只保留最近 1000 条
    if len(traces) > 1000:
        traces = traces[-1000:]

    _save(traces)


def get_traces(skill_name: str = None, limit: int = 50) -> List[Dict]:
    """获取调用 traces。"""
    traces = _load()

    if skill_name:
        traces = [t for t in traces if t["skill_name"] == skill_name]

    return traces[-limit:]


def _load() -> List[Dict]:
    """加载 traces。"""
    if not traces_file.exists():
        return []
    try:
        return json.loads(traces_file.read_text(encoding="utf-8"))
    except:
        return []


def _save(traces: List[Dict]):
    """保存 traces。"""
    traces_file.write_text(
        json.dumps(traces, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    print("=" * 60)
    print("  🔍 Skill Traces — 调用日志")
    print("=" * 60)

    traces = get_traces(limit=10)

    if not traces:
        print("\n  暂无调用日志")
        return

    print(f"\n  最近 {len(traces)} 次调用：")
    for i, t in enumerate(traces, 1):
        status = "✅" if t["success"] else "❌"
        print(f"    {i}. {status} {t['skill_name']} ({t['duration_seconds']:.2f}s)")
        print(f"       时间: {t['timestamp']}")
        if t["error"]:
            print(f"       错误: {t['error']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
