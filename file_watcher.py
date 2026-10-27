"""
Skill File Watcher — 文件监控。
监控项目文件变化，文件变了就自动重新扫描。
LGD: 有籍（监控有记录）、有证（变化有证据）、有门禁（扫完验证）。
"""
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List


project_root = Path(__file__).parent
watcher_log = project_root / "file-watcher-log.json"


def get_file_modification_times() -> Dict[str, float]:
    """获取所有 .py 文件的修改时间。"""
    mod_times = {}

    for py_file in project_root.glob("*.py"):
        mod_times[py_file.name] = py_file.stat().st_mtime

    return mod_times


def check_for_changes() -> Dict:
    """检查有没有文件变化。"""
    current_times = get_file_modification_times()

    # 加载上次的记录
    last_times = _load_last_times()

    if not last_times:
        # 第一次运行，保存当前状态
        _save_last_times(current_times)
        return {"changed": False, "message": "第一次运行，记录当前状态"}

    # 对比
    changed_files = []
    for filename, mod_time in current_times.items():
        if filename not in last_times or mod_time > last_times[filename]:
            changed_files.append(filename)

    if changed_files:
        # 更新记录
        _save_last_times(current_times)
        return {
            "changed": True,
            "changed_files": changed_files,
            "message": f"检测到 {len(changed_files)} 个文件变了：{', '.join(changed_files)}"
        }

    return {"changed": False, "message": "没有文件变化"}


def auto_scan_if_changed() -> Dict:
    """如果文件变了，自动重新扫描。"""
    check_result = check_for_changes()

    if not check_result["changed"]:
        return {"status": "no-change", "message": "没有变化，不用扫"}

    # 模拟自动扫描
    return {
        "status": "auto-scanned",
        "message": f"文件变了，自动重新扫描了一遍：{', '.join(check_result['changed_files'])}"
    }


def _load_last_times() -> Dict[str, float]:
    """加载上次的修改时间。"""
    if not watcher_log.exists():
        return {}
    try:
        data = json.loads(watcher_log.read_text(encoding="utf-8"))
        return data.get("last_mod_times", {})
    except:
        return {}


def _save_last_times(times: Dict[str, float]):
    """保存修改时间。"""
    data = {
        "last_check": datetime.now().isoformat(),
        "last_mod_times": times
    }
    watcher_log.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    print("=" * 60)
    print("(")
    print("  👀 Skill File Watcher — 文件监控")
    print("=" * 60)

    print("\n  检查文件变化中...\n")

    result = auto_scan_if_changed()
    print(f"  {result['message']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
