"""
Skill Registry — 本地技能注册中心。
本地搜索、浏览、管理 skill。
"""
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path


@dataclass
class Skill:
    """一个 skill 的元数据。"""
    name: str
    description: str
    version: str
    author: str
    category: str
    tags: List[str]
    path: str
    trust_score: int


# 我们的 skill 列表
REGISTRY: List[Skill] = [
    Skill(
        name="reg-citation-normalizer",
        description="医疗器械法规引用编号的识别、解析与规范化",
        version="1.0.0",
        author="StevenZhao26",
        category="medical-device",
        tags=["medical-device", "regulatory", "citation"],
        path=r"C:\Users\Administrator\.agents\skills\skills-reg-citation-normalizer-master-809eea69d1597f344da648041dfec729078b1103",
        trust_score=100
    ),
    Skill(
        name="medxpert-termbase",
        description="医械法规术语库与译稿质检",
        version="1.0.0",
        author="medxpert",
        category="medical-device",
        tags=["medical-device", "regulatory", "terminology", "translation"],
        path=r"C:\Users\Administrator\.agents\skills\skills-medxpert-termbase-master-a1b96dcc19f833337027b4cf23c50bfddef8f8f0",
        trust_score=100
    ),
    Skill(
        name="iso14971-risk-matrix",
        description="ISO 14971 风险矩阵计算与风险管理文件自查",
        version="1.0.0",
        author="medxpert",
        category="medical-device",
        tags=["medical-device", "risk-management", "iso-14971"],
        path=r"C:\Users\Administrator\.agents\skills\skills-iso14971-risk-matrix-master-956b23753b38c681010bc1f1bf41c801b273780f",
        trust_score=100
    ),
    Skill(
        name="skillgate",
        description="Skill 安全扫描与信任门禁",
        version="7.3.0",
        author="StevenZhao26",
        category="developer-tools",
        tags=["security", "scan", "trust", "gate"],
        path=".",
        trust_score=95
    ),
    Skill(
        name="lgd-gate-methodology",
        description="LGD-Gate 开源方法论",
        version="1.0.0",
        author="StevenZhao26",
        category="methodology",
        tags=["methodology", "open-source", "l-g-d"],
        path=r"C:\Users\Administrator\.agents\skills\skills-lgd-gate-methodology-master",
        trust_score=100
    ),
    # 我们新写的医械法规 skill
    Skill(
        name="iec62366-usability-check",
        description="IEC 62366 可用性工程文件检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-device",
        tags=["medical-device", "usability", "iec-62366"],
        path="skills/iec62366-usability-check.py",
        trust_score=90
    ),
    Skill(
        name="iec62304-sdlc-check",
        description="IEC 62304 软件生命周期检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-device",
        tags=["medical-device", "software", "iec-62304"],
        path="skills/iec62304-sdlc-check.py",
        trust_score=90
    ),
    Skill(
        name="iso10993-biocompatibility-check",
        description="ISO 10993 生物相容性报告检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-device",
        tags=["medical-device", "biocompatibility", "iso-10993"],
        path="skills/iso10993-biocompatibility-check.py",
        trust_score=90
    ),
    Skill(
        name="cer-clinical-evaluation-check",
        description="CER 临床评价报告检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-device",
        tags=["medical-device", "clinical", "cer"],
        path="skills/cer-clinical-evaluation-check.py",
        trust_score=90
    ),
    Skill(
        name="iso13485-qms-check",
        description="ISO 13485 质量管理体系文件检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-device",
        tags=["medical-device", "qms", "iso-13485"],
        path="skills/iso13485-qms-check.py",
        trust_score=90
    ),
    Skill(
        name="ifu-labeling-check",
        description="标签和说明书（IFU）检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-device",
        tags=["medical-device", "labeling", "ifu"],
        path="skills/ifu-labeling-check.py",
        trust_score=90
    ),
    Skill(
        name="pms-post-market-check",
        description="上市后监督（PMS）检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-device",
        tags=["medical-device", "pms", "post-market"],
        path="skills/pms-post-market-check.py",
        trust_score=90
    ),
    Skill(
        name="change-control-check",
        description="变更控制程序检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-device",
        tags=["medical-device", "change-control", "qms"],
        path="skills/change-control-check.py",
        trust_score=90
    ),
    Skill(
        name="ai-medical-algorithm-check",
        description="医疗 AI 算法验证检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-ai",
        tags=["medical-device", "ai", "algorithm"],
        path="skills/ai-medical-algorithm-check.py",
        trust_score=85
    ),
    Skill(
        name="ai-dataset-quality-check",
        description="医疗 AI 数据集质量检查",
        version="1.0.0",
        author="SkillGate",
        category="medical-ai",
        tags=["medical-device", "ai", "dataset"],
        path="skills/ai-dataset-quality-check.py",
        trust_score=85
    ),
]


def search(query: str) -> List[Skill]:
    """搜索 skill。"""
    query_lower = query.lower()
    results = []

    for skill in REGISTRY:
        score = 0
        # 名称匹配
        if query_lower in skill.name.lower():
            score += 3
        # 描述匹配
        if query_lower in skill.description.lower():
            score += 2
        # 标签匹配
        for tag in skill.tags:
            if query_lower in tag.lower():
                score += 1
        # 分类匹配
        if query_lower in skill.category.lower():
            score += 1

        if score > 0:
            results.append((score, skill))

    results.sort(key=lambda x: x[0], reverse=True)
    return [skill for score, skill in results]


def list_all() -> List[Skill]:
    """列出所有 skill。"""
    return REGISTRY


def by_category() -> Dict[str, List[Skill]]:
    """按分类分组。"""
    categories = {}
    for skill in REGISTRY:
        if skill.category not in categories:
            categories[skill.category] = []
        categories[skill.category].append(skill)
    return categories


def scan_all_skills() -> List[Dict]:
    """一键扫描所有 skill，更新信任分。"""
    import subprocess
    import sys
    from pathlib import Path

    project_root = Path(__file__).parent
    results = []

    print("=" * 60)
    print("  🔍 一键扫描所有 skill")
    print("=" * 60)

    for skill in REGISTRY:
        try:
            # 跑 SkillGate 扫描
            result = subprocess.run(
                [sys.executable, "skillgate.py", "scan", skill.path],
                cwd=str(project_root),
                capture_output=True,
                text=True
            )

            # 提取 Trust Score
            trust_score = 0
            for line in result.stdout.split("\n"):
                if "Trust Score" in line:
                    # 提取数字
                    import re
                    match = re.search(r"(\d+)/100", line)
                    if match:
                        trust_score = int(match.group(1))
                    break

            # 更新注册中心里的信任分
            skill.trust_score = trust_score

            results.append({
                "name": skill.name,
                "trust_score": trust_score,
                "status": "✅" if trust_score >= 80 else "⚠️"
            })

            print(f"  {skill.name}: {trust_score}/100")

        except Exception as e:
            results.append({
                "name": skill.name,
                "trust_score": 0,
                "status": f"❌ 错误: {e}"
            })
            print(f"  {skill.name}: ❌ 错误")

    print("=" * 60)
    return results


def main():
    print("=" * 60)
    print("  📚 Skill Registry — 本地技能注册中心")
    print("=" * 60)

    print(f"\n  总 skill 数: {len(REGISTRY)}")

    # 按分类分组
    categories = by_category()
    print(f"\n  按分类：")
    for category, skills in categories.items():
        print(f"    {category}: {len(skills)} 个")

    # 列出所有 skill
    print(f"\n  所有 skill：")
    for i, skill in enumerate(REGISTRY, 1):
        print(f"    {i}. {skill.name} v{skill.version} — Trust Score {skill.trust_score}/100")

    # 搜索示例
    print(f"\n  搜索示例：输入 'medical'")
    results = search("medical")
    print(f"    找到 {len(results)} 个结果：")
    for skill in results:
        print(f"      - {skill.name}")

    print("\n" + "=" * 60)
    print("  ✅ 注册中心就绪")
    print("=" * 60)


if __name__ == "__main__":
    main()
