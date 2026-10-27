"""
SkillGate 最严测试方案 — 精确率 + 召回率 + F1-score。
按照 LGD 方法论：有籍、有证、有门禁。
"""
import sys
from pathlib import Path
import tempfile
import shutil

# 把项目根目录加到 path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# ============================================================
# 测试集：每个用例都有明确预期（有籍）
# ============================================================

# 真阳性（True Positive）：真的有漏洞，应该被报出来
TRUE_POSITIVES = {
    "eval() call": "eval(user_input)",
    "exec() call": "exec(user_code)",
    "os.system()": "os.system('ls -la')",
    "shell=True": "subprocess.run('ls', shell=True)",
    "pickle.loads": "pickle.loads(data)",
    "hardcoded api_key": 'api_key = "sk-1234567890abcdef"',
}

# 真阴性（True Negative）：真的没漏洞，不应该被报出来
TRUE_NEGATIVES = {
    "normal function": "def add(a, b): return a + b",
    "variable assignment": "x = 42",
    "print statement": "print('hello world')",
    "import requests (safe)": "import requests",
    "from env var (safe)": 'api_key = os.getenv("API_KEY")',
    "list comprehension": "[x for x in range(10)]",
    "try/except": "try:\n    1/0\nexcept:\n    pass",
    "class definition": "class MyClass:\n    def method(self): pass",
}


def run_test_suite():
    """跑测试集，算精确率和召回率。"""
    from skillgate import scan_python_file
    from skillgate import ScanResult

    print("=" * 60)
    print("  🧪 最严测试方案：精确率 + 召回率")
    print("=" * 60)

    # === 真阳性测试 ===
    print("\n  📊 真阳性测试（应该被报出来）")
    tp_total = 0
    tp_detected = 0

    for name, code in TRUE_POSITIVES.items():
        tmpdir = tempfile.mkdtemp()
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text(code)

        result = ScanResult(skill_dir=tmpdir)
        scan_python_file(test_file, result)

        # 有没有报出 MEDIUM 及以上的 finding？
        medium_or_higher = [f for f in result.findings if f.severity in ["CRITICAL", "HIGH", "MEDIUM"]]
        found = len(medium_or_higher) > 0
        if found:
            tp_detected += 1
            status = "✅"
        else:
            status = "❌"
        tp_total += 1
        print(f"    {status} {name}: {len(medium_or_higher)} findings (MEDIUM+)")

        shutil.rmtree(tmpdir)

    recall = tp_detected / tp_total if tp_total > 0 else 0
    print(f"\n    召回率 (Recall): {recall*100:.1f}% ({tp_detected}/{tp_total})")

    # === 真阴性测试 ===
    print("\n  📊 真阴性测试（不应该被报出来）")
    tn_total = 0
    tn_correct = 0

    for name, code in TRUE_NEGATIVES.items():
        tmpdir = tempfile.mkdtemp()
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text(code)

        result = ScanResult(skill_dir=tmpdir)
        scan_python_file(test_file, result)

        # 有没有误报 MEDIUM 及以上的？
        false_positives = [f for f in result.findings if f.severity in ["CRITICAL", "HIGH", "MEDIUM"]]
        if len(false_positives) == 0:
            tn_correct += 1
            status = "✅"
        else:
            status = "❌"
        tn_total += 1
        print(f"    {status} {name}: {len(false_positives)} false positives (MEDIUM+)")

        shutil.rmtree(tmpdir)

    specificity = tn_correct / tn_total if tn_total > 0 else 0
    fpr = 1 - specificity  # 误报率
    print(f"\n    特异度 (Specificity): {specificity*100:.1f}% ({tn_correct}/{tn_total})")
    print(f"    误报率 (FPR): {fpr*100:.1f}%")

    # === 综合评分 ===
    precision = tp_detected / (tp_detected + (tn_total - tn_correct)) if (tp_detected + (tn_total - tn_correct)) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n" + "=" * 60)
    print("  📈 综合评分")
    print("=" * 60)
    print(f"    精确率 (Precision): {precision*100:.1f}%")
    print(f"    召回率 (Recall): {recall*100:.1f}%")
    print(f"    误报率 (FPR): {fpr*100:.1f}%")
    print(f"    F1-score: {f1*100:.1f}%")

    # === 门禁 ===
    print("\n" + "=" * 60)
    print("  🚪 门禁检查")
    print("=" * 60)
    gate_pass = True
    if fpr > 10:
        print(f"    ❌ 误报率 {fpr*100:.1f}% > 10% — 不通过")
        gate_pass = False
    else:
        print(f"    ✅ 误报率 {fpr*100:.1f}% < 10% — 通过")

    if recall < 80:
        print(f"    ❌ 召回率 {recall*100:.1f}% < 80% — 不通过")
        gate_pass = False
    else:
        print(f"    ✅ 召回率 {recall*100:.1f}% >= 80% — 通过")

    if gate_pass:
        print("\n  🎉 门禁全过！可以发布！")
    else:
        print("\n  ⚠️  门禁没全过，还要继续优化！")

    return {
        "precision": precision,
        "recall": recall,
        "fpr": fpr,
        "f1": f1,
        "gate_pass": gate_pass
    }


if __name__ == "__main__":
    run_test_suite()
