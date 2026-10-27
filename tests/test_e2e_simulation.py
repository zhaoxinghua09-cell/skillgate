"""
SkillGate 端到端模拟 — 模拟真实用户的最严工况。
"""
import sys
from pathlib import Path
import tempfile
import shutil

# 把项目根目录加到 path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def simulate_full_workflow():
    """模拟完整用户工作流。"""
    print("=" * 60)
    print("  🎭 SkillGate 端到端模拟 — 最严工况")
    print("=" * 60)

    # === 场景：用户开发了一个新 skill，要发布了 ===
    print("\n  📋 场景：用户开发了一个新 skill，准备发布")

    # 创建一个模拟的 skill
    tmpdir = tempfile.mkdtemp(prefix="skillgate-e2e-")
    skill_dir = Path(tmpdir) / "my-new-skill"
    skill_dir.mkdir()

    # 写 SKILL.md
    (skill_dir / "SKILL.md").write_text("""---
name: my-new-skill
description: 一个新的测试 skill
version: 1.0.0
author: test-user
license: MIT
---

# My New Skill

这是一个测试 skill。
""")

    # 写 scripts/good.py — 安全代码
    (skill_dir / "scripts").mkdir()
    (skill_dir / "scripts" / "good.py").write_text('''
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
''')

    # 写 scripts/bad.py — 有一个漏洞
    (skill_dir / "scripts" / "bad.py").write_text('''
import os

def run_command(cmd):
    os.system(cmd)
''')

    print(f"    ✅ 创建模拟 skill: {skill_dir}")

    # === 步骤 1：用户跑安全扫描 ===
    print("\n  🔍 步骤 1：跑安全扫描")
    from skillgate import scan_skill

    result = scan_skill(str(skill_dir))
    print(f"    Trust Score: {result.trust_score}/100 ({result.grade})")
    print(f"    Critical: {result.critical_count}")
    print(f"    High: {result.high_count}")
    print(f"    Medium: {result.medium_count}")
    print(f"    Low: {result.low_count}")
    print(f"    Findings: {len(result.findings)}")

    # === 步骤 2：用户看报告 ===
    print("\n  📄 步骤 2：生成报告")
    # 简单 markdown 报告
    report = f"""# SkillGate 扫描报告

- **Skill**: {result.skill_name}
- **Trust Score**: {result.trust_score}/100 ({result.grade})
- **扫描文件数**: {result.files_scanned}

## Findings

"""
    for f in result.findings:
        report += f"- [{f.severity}] {f.message} ({f.file}:{f.line})\n"

    report_path = Path(tmpdir) / "report.md"
    report_path.write_text(report)
    print(f"    ✅ 报告生成: {report_path}")

    # === 步骤 3：用户跑 --fail-under 门禁 ===
    print("\n  🚪 步骤 3：CI 门禁检查")
    fail_under = 80
    if result.trust_score >= fail_under:
        print(f"    ✅ Trust Score {result.trust_score} >= {fail_under} — 通过")
        gate_pass = True
    else:
        print(f"    ❌ Trust Score {result.trust_score} < {fail_under} — 不通过")
        gate_pass = False

    # === 步骤 4：用户修了漏洞，再扫一遍 ===
    print("\n  🔧 步骤 4：用户修了漏洞，再扫一遍")
    # 把 bad.py 改成安全的
    (skill_dir / "scripts" / "bad.py").write_text('''
import subprocess

def run_command(cmd_list):
    return subprocess.run(cmd_list, shell=False)
''')

    result2 = scan_skill(str(skill_dir))
    print(f"    修复后 Trust Score: {result2.trust_score}/100 ({result2.grade})")
    print(f"    Critical: {result2.critical_count}")
    print(f"    High: {result2.high_count}")

    # === 步骤 5：生成徽章 ===
    print("\n  🏅 步骤 5：生成徽章")
    from badge_generator import generate_badge
    badge_svg = generate_badge(result2.trust_score, result2.grade)
    badge_path = Path(tmpdir) / "badge.svg"
    badge_path.write_text(badge_svg)
    print(f"    ✅ 徽章生成: {badge_path}")

    # === 步骤 6：SBOM 生成 ===
    print("\n  📦 步骤 6：生成 SBOM")
    from sbom_generator import generate_sbom
    sbom = generate_sbom(skill_dir)
    print(f"    ✅ SBOM 生成: {len(sbom)} bytes")

    # === 总结 ===
    print("\n" + "=" * 60)
    print("  📊 端到端模拟总结")
    print("=" * 60)
    print(f"    初始 Trust Score: {result.trust_score}/100")
    print(f"    修复后 Trust Score: {result2.trust_score}/100")
    print(f"    提升: {result2.trust_score - result.trust_score} 分")
    print(f"    CI 门禁通过: {'✅' if gate_pass else '❌'}")
    print(f"    报告生成: ✅")
    print(f"    徽章生成: ✅")
    print(f"    SBOM 生成: ✅")

    # 清理
    shutil.rmtree(tmpdir)

    print("\n  🎉 端到端模拟完成！")


if __name__ == "__main__":
    simulate_full_workflow()
