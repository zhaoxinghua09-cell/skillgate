"""
SkillGate JS/TS Analyzer — 扫描 JavaScript / TypeScript 文件。
"""
import re
from pathlib import Path
from typing import List, Tuple


JS_DANGEROUS_PATTERNS = [
    (r"\beval\s*\(", "CRITICAL", "eval() 动态代码执行"),
    (r"\bFunction\s*\(", "CRITICAL", "Function() 构造器动态执行"),
    (r"\bnew\s+Function\s*\(", "CRITICAL", "new Function() 动态执行"),
    (r"\bchild_process\.exec\s*\(", "CRITICAL", "child_process.exec shell 执行"),
    (r"\bchild_process\.spawn\s*\([^)]*shell\s*:\s*true", "CRITICAL", "child_process.spawn shell=True"),
    (r"\bexecSync\s*\(", "HIGH", "execSync 同步 shell 执行"),
    (r"\brequire\s*\(\s*['\"]child_process['\"]", "HIGH", "require child_process"),
    (r"\bimport\s+.*\s+from\s+['\"]child_process['\"]", "HIGH", "import child_process"),
    (r"\b__dirname\s*\+\s*.*\.\.\/", "MEDIUM", "路径遍历风险"),
    (r"\bprocess\.env\.", "LOW", "读取环境变量"),
    (r"\bfetch\s*\(", "MEDIUM", "fetch 网络请求"),
    (r"\baxios\b", "MEDIUM", "axios HTTP 客户端"),
    (r"\bXMLHttpRequest\b", "MEDIUM", "XMLHttpRequest 网络请求"),
    (r"\bhttp\.request\b", "MEDIUM", "http.request 网络请求"),
    (r"\bhttps\.request\b", "MEDIUM", "https.request 网络请求"),
]

JS_SECRET_PATTERNS = [
    (re.compile(r"(api[_-]?key|apikey|secret|token|password)\s*[:=]\s*['\"`]([^'\"`]{8,})['\"`]", re.IGNORECASE),
     "CRITICAL", "硬编码凭证"),
]

JS_PROMPT_INJECTION = [
    (r"ignore\s+previous\s+instructions", "CRITICAL", "Prompt injection"),
    (r"disregard\s+all\s+previous", "CRITICAL", "Prompt injection"),
    (r"jailbreak", "CRITICAL", "Jailbreak pattern"),
    (r"reveal\s+your\s+prompt", "HIGH", "Reveal system prompt attempt"),
]


def scan_js_file(filepath: Path) -> List[Tuple]:
    """Scan a JS/TS file, return list of (severity, category, message, line)."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()

    # Dangerous patterns
    for pattern, severity, msg in JS_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "js-dangerous", msg, i))

    # Secret patterns
    for pattern, severity, msg in JS_SECRET_PATTERNS:
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                findings.append((severity, "js-credential", msg, i))

    # Prompt injection
    for pattern, severity, msg in JS_PROMPT_INJECTION:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((severity, "prompt-injection", msg, i))

    return findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python js_analyzer.py <file.js>")
        sys.exit(1)

    findings = scan_js_file(Path(sys.argv[1]))
    for sev, cat, msg, line in findings:
        print(f"[{sev}] line {line}: {msg}")
