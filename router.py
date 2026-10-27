"""
Skill Router — 路由器。
用户输入一句话，自动选合适的 skill。
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Skill:
    """一个 skill 的元数据。"""
    name: str
    description: str
    keywords: List[str]
    path: str


# 我们的 skill 列表
SKILLS = [
    Skill(
        name="reg-citation-normalizer",
        description="医疗器械法规引用编号的识别、解析与规范化",
        keywords=["法规", "引用", "citation", "21 CFR", "ISO", "GB", "NMPA", "FDA"],
        path=r"C:\Users\Administrator\.agents\skills\skills-reg-citation-normalizer-master-809eea69d1597f344da648041dfec729078b1103"
    ),
    Skill(
        name="medxpert-termbase",
        description="医械法规术语库与译稿质检",
        keywords=["术语", "翻译", "translation", "terminology", "mistranslation", "双语"],
        path=r"C:\Users\Administrator\.agents\skills\skills-medxpert-termbase-master-a1b96dcc19f833337027b4cf23c50bfddef8f8f0"
    ),
    Skill(
        name="iso14971-risk-matrix",
        description="ISO 14971 风险矩阵计算与风险管理文件自查",
        keywords=["风险", "risk", "ISO 14971", "severity", "probability", "风险矩阵"],
        path=r"C:\Users\Administrator\.agents\skills\skills-iso14971-risk-matrix-master-956b23753b38c681010bc1f1bf41c801b273780f"
    ),
    Skill(
        name="skillgate",
        description="Skill 安全扫描与信任门禁",
        keywords=["安全", "扫描", "security", "scan", "trust", "gate", "漏洞", "vulnerability"],
        path="."
    ),
    Skill(
        name="lgd-gate-methodology",
        description="LGD-Gate 开源方法论",
        keywords=["方法论", "methodology", "开发", "dev", "开源", "open source"],
        path=r"C:\Users\Administrator\.agents\skills\skills-lgd-gate-methodology-master"
    ),
]


def route(query: str) -> List[Skill]:
    """根据用户输入，返回最匹配的 skill 列表（按匹配度排序）。"""
    query_lower = query.lower()
    scored = []

    for skill in SKILLS:
        score = 0
        # 关键词匹配
        for keyword in skill.keywords:
            if keyword.lower() in query_lower:
                score += 1
        # 描述匹配
        if skill.description.lower() in query_lower:
            score += 2

        if score > 0:
            scored.append((score, skill))

    # 按分数降序排列
    scored.sort(key=lambda x: x[0], reverse=True)
    return [skill for score, skill in scored]


def main():
    print("=" * 60)
    print("  🚦 Skill Router — 路由器")
    print("=" * 60)
    print("  输入一句话，自动选合适的 skill")
    print("  输入 'quit' 退出")
    print("=" * 60)

    while True:
        print()
        query = input("  你想做什么？> ").strip()
        if query.lower() == "quit":
            break

        if not query:
            continue

        results = route(query)

        if not results:
            print("  ⚠️ 没有找到匹配的 skill")
        else:
            print(f"  ✅ 找到 {len(results)} 个匹配的 skill：")
            for i, skill in enumerate(results, 1):
                print(f"    {i}. {skill.name} — {skill.description}")


if __name__ == "__main__":
    main()
