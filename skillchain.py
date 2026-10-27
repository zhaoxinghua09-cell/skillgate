"""
医械法规技能链编排器。
把三个 skill 串起来：规范化引用 → 术语质检 → 风险评估 → 安全扫描。
"""
import subprocess
import sys
from pathlib import Path


# 三个 skill 的路径
SKILLS = {
    "reg-citation-normalizer": r"C:\Users\Administrator\.agents\skills\skills-reg-citation-normalizer-master-809eea69d1597f344da648041dfec729078b1103",
    "medxpert-termbase": r"C:\Users\Administrator\.agents\skills\skills-medxpert-termbase-master-a1b96dcc19f833337027b4cf23c50bfddef8f8f0",
    "iso14971-risk-matrix": r"C:\Users\Administrator\.agents\skills\skills-iso14971-risk-matrix-master-956b23753b38c681010bc1f1bf41c801b273780f",
}


def step1_normalize_citations(doc_path: str):
    """第一步：规范化法规引用。"""
    print("\n" + "=" * 60)
    print("  第 1 步：规范化法规引用 (reg-citation-normalizer)")
    print("=" * 60)

    script = Path(SKILLS["reg-citation-normalizer"]) / "scripts" / "cite_normalize.py"
    result = subprocess.run(
        [sys.executable, str(script), "check", doc_path],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("  ✅ 引用规范化通过")
    else:
        print("  ⚠️ 发现引用书写问题")
        print(result.stdout)

    return result.returncode


def step2_terminology_check(doc_path: str):
    """第二步：术语质检。"""
    print("\n" + "=" * 60)
    print("  第 2 步：术语质检 (medxpert-termbase)")
    print("=" * 60)

    script = Path(SKILLS["medxpert-termbase"]) / "scripts" / "term_check.py"
    result = subprocess.run(
        [sys.executable, str(script), "check", doc_path],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("  ✅ 术语质检通过")
    else:
        print("  ⚠️ 发现术语问题")
        print(result.stdout)

    return result.returncode


def step3_risk_assessment():
    """第三步：风险评估（示例）。"""
    print("\n" + "=" * 60)
    print("  第 3 步：风险评估 (iso14971-risk-matrix)")
    print("=" * 60)

    script = Path(SKILLS["iso14971-risk-matrix"]) / "scripts" / "risk_matrix.py"
    result = subprocess.run(
        [sys.executable, str(script), "assess", "-s", "4", "-p", "2"],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    return result.returncode


def step4_security_scan():
    """第四步：安全扫描 (SkillGate)。"""
    print("\n" + "=" * 60)
    print("  第 4 步：安全扫描 (SkillGate)")
    print("=" * 60)

    project_root = Path(__file__).parent
    result = subprocess.run(
        [sys.executable, "skillgate.py", "scan", "."],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    # 提取 Trust Score
    for line in result.stdout.split("\n"):
        if "Trust Score" in line:
            print(f"  {line.strip()}")

    return result.returncode


def main():
    print("=" * 60)
    print("  🔗 医械法规技能链")
    print("=" * 60)
    print("  流程：规范化引用 → 术语质检 → 风险评估 → 安全扫描")
    print("=" * 60)

    # 示例文档
    doc_path = r"C:\Users\Administrator\.agents\skills\skills-reg-citation-normalizer-master-809eea69d1597f344da648041dfec729078b1103\SKILL.md"

    # 跑四步
    step1_normalize_citations(doc_path)
    step2_terminology_check(doc_path)
    step3_risk_assessment()
    step4_security_scan()

    print("\n" + "=" * 60)
    print("  ✅ 技能链执行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
