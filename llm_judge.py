"""
SkillGate LLM-as-Judge — 用大模型评测 skill 输出质量。
比简单的字符串匹配更接近真实用户体验。

支持：
- OpenAI 兼容 API
- Anthropic API
- 任何兼容 OpenAI 格式的本地模型
"""
import json
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class JudgeResult:
    skill_name: str
    test_case: str
    expected_behavior: str
    actual_output: str
    judge_score: int  # 1-10
    judge_comment: str
    passed: bool


def call_llm(prompt: str, api_key: str, model: str = "gpt-4o-mini", base_url: str = "https://api.openai.com/v1") -> str:
    """Call an LLM API (OpenAI-compatible)."""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert judge evaluating AI skill outputs. Be strict but fair."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }).encode()

    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM call failed: {e}"


def judge_output(skill_name: str, test_prompt: str, expected_behavior: str, actual_output: str,
                 api_key: str, model: str = "gpt-4o-mini", base_url: str = None) -> JudgeResult:
    """Use LLM to judge if the skill output is good enough."""

    judge_prompt = f"""You are evaluating an AI skill called "{skill_name}".

**Test prompt given to the skill:**
{test_prompt}

**Expected behavior:**
{expected_behavior}

**Actual output from the skill:**
{actual_output}

Rate the output on a scale of 1-10:
- 10: Perfect, exactly what was expected
- 7-9: Good, minor issues
- 4-6: Acceptable but with notable problems
- 1-3: Poor, major issues or wrong

First explain your reasoning briefly, then give a score.
Format your response as:
REASONING: <your explanation>
SCORE: <number 1-10>
"""

    response = call_llm(judge_prompt, api_key, model, base_url or "https://api.openai.com/v1")

    # Parse score from response
    score = 5
    comment = response
    for line in response.splitlines():
        if line.startswith("SCORE:"):
            try:
                score = int(line.split(":")[1].strip())
            except:
                pass
        if line.startswith("REASONING:"):
            comment = line.split(":", 1)[1].strip()

    passed = score >= 7

    return JudgeResult(
        skill_name=skill_name,
        test_case=test_prompt[:50],
        expected_behavior=expected_behavior[:50],
        actual_output=actual_output[:100],
        judge_score=score,
        judge_comment=comment,
        passed=passed
    )


def run_judge_suite(skill_name: str, test_cases: list[dict], api_key: str,
                    model: str = "gpt-4o-mini", base_url: str = None) -> list[JudgeResult]:
    """Run LLM-as-judge on a suite of test cases."""
    results = []
    for tc in test_cases:
        result = judge_output(
            skill_name=skill_name,
            test_prompt=tc["prompt"],
            expected_behavior=tc["expected"],
            actual_output=tc.get("actual", "(no output yet)"),
            api_key=api_key,
            model=model,
            base_url=base_url
        )
        results.append(result)
    return results


if __name__ == "__main__":
    # Demo (needs API key)
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY to run demo")
        exit(0)

    test = {
        "prompt": "What is ISO 14971?",
        "expected": "Explain that ISO 14971 is the medical device risk management standard",
        "actual": "ISO 14971 is the international standard for medical device risk management."
    }

    result = judge_output("iso14971-risk-matrix", test["prompt"], test["expected"], test["actual"], api_key)
    print(f"Score: {result.judge_score}/10")
    print(f"Passed: {result.passed}")
    print(f"Comment: {result.judge_comment}")
