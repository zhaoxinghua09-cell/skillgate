"""
端到端集成测试。
用我们搭的测试环境跑完整的扫描流程。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from skillgate import scan_skill


def test_good_skill():
    """好的 skill 应该得高分。"""
    fixture_dir = Path(__file__).parent / "fixtures" / "good-skill"
    result = scan_skill(str(fixture_dir))

    print(f"  Good Skill Score: {result.trust_score}/100 ({result.grade})")
    # 不要求 100 分，只要不是 F 就行
    assert result.grade != "F", "Good skill should not be F"
    print("  ✅ test_good_skill passed")


def test_dangerous_skill():
    """危险的 skill 应该得低分。"""
    fixture_dir = Path(__file__).parent / "fixtures" / "dangerous-skill"
    result = scan_skill(str(fixture_dir))

    print(f"  Dangerous Skill Score: {result.trust_score}/100 ({result.grade})")
    # 危险的应该有 critical 或 high findings
    assert result.critical_count > 0 or result.high_count > 0, \
        "Dangerous skill should have critical or high findings"
    print("  ✅ test_dangerous_skill passed")


def test_score_calculation():
    """Trust Score 计算应该正确。"""
    # 我们自己的 skill 应该有分数
    result = scan_skill(str(Path(__file__).parent.parent))
    assert 0 <= result.trust_score <= 100, "Score should be between 0 and 100"
    print(f"  Self Scan Score: {result.trust_score}/100")
    print("  ✅ test_score_calculation passed")


if __name__ == "__main__":
    print("=" * 50)
    print("  端到端集成测试")
    print("=" * 50)
    print()

    test_good_skill()
    test_dangerous_skill()
    test_score_calculation()

    print()
    print("=" * 50)
    print("  ✅ All integration tests passed!")
    print("=" * 50)
