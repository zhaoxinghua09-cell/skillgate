"""
Skill Synthesizer — 合成器。
合并多个 skill 的输出，生成最终结果。
"""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class SkillOutput:
    """一个 skill 的输出。"""
    skill_name: str
    output: str
    confidence: float  # 置信度 0-1


def synthesize(outputs: List[SkillOutput]) -> str:
    """合并多个 skill 的输出，生成最终结果。"""
    if not outputs:
        return ""

    if len(outputs) == 1:
        return outputs[0].output

    # 按置信度排序
    sorted_outputs = sorted(outputs, key=lambda x: x.confidence, reverse=True)

    # 合成：先列每个 skill 的输出，然后总结
    result_parts = []
    result_parts.append("## 多 Skill 合成结果\n")

    for i, output in enumerate(sorted_outputs, 1):
        result_parts.append(f"### {i}. {output.skill_name}（置信度 {output.confidence:.0%}）")
        result_parts.append(output.output)
        result_parts.append("")

    # 总结
    result_parts.append("### 总结")
    result_parts.append(f"共 {len(outputs)} 个 skill 参与合成：")
    for output in sorted_outputs:
        result_parts.append(f"- {output.skill_name}")

    return "\n".join(result_parts)


def main():
    print("=" * 60)
    print("  🔀 Skill Synthesizer — 合成器")
    print("=" * 60)

    # 示例：合成两个 skill 的输出
    outputs = [
        SkillOutput(
            skill_name="reg-citation-normalizer",
            output="✅ 引用规范化通过：0 个错误",
            confidence=0.95
        ),
        SkillOutput(
            skill_name="medxpert-termbase",
            output="⚠️ 术语质检发现 1 个错误：ISO13485 → ISO 13485",
            confidence=0.90
        ),
    ]

    result = synthesize(outputs)
    print(result)

    print("=" * 60)
    print("  ✅ 合成完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
