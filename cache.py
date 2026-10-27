"""
Skill Cache — 上下文缓存。
缓存常用 skill 的结果，省时间。
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta


project_root = Path(__file__).parent
cache_file = project_root / "cache.json"


def get_cache_key(skill_name: str, input_data: str) -> str:
    """生成缓存 key。"""
    raw = f"{skill_name}:{input_data}"
    return hashlib.md5(raw.encode(), usedforsecurity=False).hexdigest()


def get(skill_name: str, input_data: str, ttl_seconds: int = 3600):
    """从缓存里取结果。TTL 默认 1 小时。"""
    data = _load()
    key = get_cache_key(skill_name, input_data)

    if key not in data:
        return None

    entry = data[key]

    # 检查是否过期
    cached_at = datetime.fromisoformat(entry["cached_at"])
    if datetime.now() - cached_at > timedelta(seconds=ttl_seconds):
        # 过期了，删掉
        del data[key]
        _save(data)
        return None

    return entry["output"]


def set(skill_name: str, input_data: str, output: str):
    """把结果存到缓存里。"""
    data = _load()
    key = get_cache_key(skill_name, input_data)

    data[key] = {
        "skill_name": skill_name,
        "input": input_data,
        "output": output,
        "cached_at": datetime.now().isoformat()
    }

    _save(data)


def clear():
    """清空缓存。"""
    _save({})


def get_stats() -> dict:
    """获取缓存统计。"""
    data = _load()
    return {
        "total_entries": len(data),
        "size_bytes": len(json.dumps(data))
    }


def _load() -> dict:
    """加载缓存。"""
    if not cache_file.exists():
        return {}
    try:
        return json.loads(cache_file.read_text(encoding="utf-8"))
    except:
        return {}


def _save(data: dict):
    """保存缓存。"""
    cache_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    print("=" * 60)
    print("(")
    print("  💾 Skill Cache — 上下文缓存")
    print("=" * 60)

    stats = get_stats()
    print(f"\n  缓存条目数: {stats['total_entries']}")
    print(f"  缓存大小: {stats['size_bytes'] / 1024:.1f} KB")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
