"""
Skill Version Manager — 版本管理。
记录 skill 的版本、升级历史。
"""
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime


@dataclass
class VersionHistory:
    """一个 skill 的版本历史。"""
    name: str
    versions: List[Dict]  # [{"version": "1.0.0", "date": "2026-10-20", "changes": "..."}]


# 我们的 skill 版本历史
VERSION_HISTORY: List[VersionHistory] = [
    VersionHistory(
        name="skillgate",
        versions=[
            {"version": "v1.0.0", "date": "2026-10-25", "changes": "最小可用版——基础安全扫描"},
            {"version": "v2.0.0", "date": "2026-10-26", "changes": "加规则、加语言、加输出格式"},
            {"version": "v3.0.0", "date": "2026-10-26", "changes": "加评测、加红队测试"},
            {"version": "v4.0.0", "date": "2026-10-27", "changes": "加 SBOM、SLSA、Scorecard"},
            {"version": "v5.0.0", "date": "2026-10-27", "changes": "加 K8s/Terraform 扫描"},
            {"version": "v6.0.0", "date": "2026-10-27", "changes": "加 CI 模拟器、加压力测试"},
            {"version": "v7.0.0", "date": "2026-10-27", "changes": "优化误报率、加 E2E 测试"},
            {"version": "v7.3.0", "date": "2026-10-27", "changes": "加 Web 版、加运行时"},
        ]
    ),
    VersionHistory(
        name="lgd-gate-methodology",
        versions=[
            {"version": "v1.0.0", "date": "2026-10-27", "changes": "初始版本——从 SkillGate 沉淀出来"},
        ]
    ),
    VersionHistory(
        name="reg-citation-normalizer",
        versions=[
            {"version": "v1.0.0", "date": "2026-09-20", "changes": "初始版本——医械法规引用规范化"},
        ]
    ),
]


def get_version_history(skill_name: str) -> List[Dict]:
    """获取一个 skill 的版本历史。"""
    for history in VERSION_HISTORY:
        if history.name == skill_name:
            return history.versions
    return []


def get_latest_version(skill_name: str) -> str:
    """获取一个 skill 的最新版本。"""
    versions = get_version_history(skill_name)
    if not versions:
        return "unknown"
    return versions[-1]["version"]


def main():
    print("=" * 60)
    print("  📦 Skill Version Manager — 版本管理")
    print("=" * 60)

    print(f"\n  总 skill 数: {len(VERSION_HISTORY)}")

    for history in VERSION_HISTORY:
        latest = history.versions[-1]
        print(f"\n  {history.name}:")
        print(f"    最新版本: {latest['version']} ({latest['date']})")
        print(f"    总版本数: {len(history.versions)}")
        print(f"    最近更新: {latest['changes'][:50]}...")

    print("\n" + "=" * 60)
    print("  ✅ 版本管理就绪")
    print("=" * 60)


if __name__ == "__main__":
    main()
