"""
Skill Evaluator — 评测者。
评测 skill 的输出质量。
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class EvaluationResult:
    """评测结果。"""
    skill_name: str
    accuracy: float  # 准确率 0-1
    completeness: float  # 完整性 0-1
    usefulness: float  # 有用性 0-1
    overall: float  # 综合分 0-1


def evaluate_skill(skill_name: str, test_cases: list) -> EvaluationResult:
    """评测一个 skill 的输出质量。

    test_cases: [(input, expected_output, actual_output), ...]
    """
    if not test_cases:
        return EvaluationResult(skill_name, 0, 0, 0, 0)

    # 准确率：输出和预期一致的比例
    correct = 0
    for input_text, expected, actual in test_cases:
        if expected == actual:
            correct += 1
    accuracy = correct / len(test_cases)

    # 完整性：输出非空的比例
    non_empty = sum(1 for _, _, actual in test_cases if actual and len(str(actual)) > 0)
    completeness = non_empty / len(test_cases)

    # 有用性：输出包含预期关键词的比例
    useful = 0
    for input_text, expected, actual in test_cases:
        if expected and str(expected) in str(actual):
            useful += 1
    usefulness = useful / len(test_cases)

    # 综合分：加权平均
    overall = accuracy * 0.5 + completeness * 0.3 + usefulness * 0.2

    return EvaluationResult(
        skill_name=skill_name,
        accuracy=accuracy,
        completeness=completeness,
        usefulness=usefulness,
        overall=overall
    )


def main():
    print("=" * 60)
    print("(")
    print("  📊 Skill Evaluator — 评测者")
    print("=" * 60)

    # 示例：评测 reg-citation-normalizer
    test_cases = [
        ("ISO13485", "ISO 13485", "ISO 13485"),  # 正确
        ("iso 13485", "ISO 13485", "ISO 13485"),  # 正确
        ("YY/T0287", "YY/T 0287", "YY/T 0287"),  # 正确
    ]

    result = evaluate_skill("reg-citation-normalizer", test_cases)

    print(f"\n  评测对象: {result.skill_name}")
    print(f"  准确率: {result.accuracy:.1%}")
    print(f"  完整性: {result.completeness:.1%}")
    print(f"  有用性: {result.usefulness:.1%}")
    print(f"  综合分: {result.overall:.1%}")

    print("\n" + "=" * 60)
    if result.overall >= 0.9:
        print("  ✅ 评测通过：优秀")
    elif result.overall >= 0.7:
        print("  ⚠️ 评测通过：良好")
    else:
        print("  ❌ 评测不通过：需要改进")
    print("=" * 60)


if __name__ == "__main__":
    main()
