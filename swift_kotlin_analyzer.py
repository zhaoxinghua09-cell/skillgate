"""
SkillGate Swift/Kotlin Analyzer — 扫描 Swift 和 Kotlin 文件。
"""
import re
from pathlib import Path
from typing import List, Tuple


SWIFT_DANGEROUS_PATTERNS = [
    (r"\bNSTask\b", "HIGH", "NSTask 子进程执行"),
    (r"\bProcess\(\)\.launch", "HIGH", "Process.launch() 子进程"),
    (r"\bURLSession\b", "MEDIUM", "URLSession 网络请求"),
    (r"\bURL\(string:", "MEDIUM", "URL 网络请求"),
    (r"\bUserDefaults\.standard\b", "LOW", "UserDefaults 本地存储"),
    (r"\bFileManager\.default\b", "LOW", "FileManager 文件操作"),
    (r"\btry!\b", "MEDIUM", "try! 强制解包错误"),
    (r"\bas!\b", "MEDIUM", "as! 强制类型转换"),
    (r"\bfatalError\(", "HIGH", "fatalError() 强制崩溃"),
    (r"\bprint\(", "LOW", "print 调试语句"),
]

KOTLIN_DANGEROUS_PATTERNS = [
    (r"\bRuntime\.getRuntime\(\)\.exec\b", "CRITICAL", "Runtime.exec() 执行系统命令"),
    (r"\bProcessBuilder\b", "HIGH", "ProcessBuilder 子进程"),
    (r"\bSystem\.getenv\b", "LOW", "System.getenv 读取环境变量"),
    (r"\bClass\.forName\b", "MEDIUM", "Class.forName 动态加载"),
    (r"\bClassLoader\b", "MEDIUM", "ClassLoader 动态类加载"),
    (r"\bObjectInputStream\b", "HIGH", "Java 反序列化"),
    (r"\bHttpURLConnection\b", "MEDIUM", "HttpURLConnection 网络请求"),
    (r"\bOkHttpClient\b", "MEDIUM", "OkHttp 网络库"),
    (r"\bFile\(\)\.deleteRecursively\b", "HIGH", "deleteRecursively 递归删除"),
    (r"\bprintln\(", "LOW", "println 调试语句"),
]


def scan_swift_file(filepath: Path) -> List[Tuple]:
    """Scan a Swift file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in SWIFT_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "swift-dangerous", msg, i))

    return findings


def scan_kotlin_file(filepath: Path) -> List[Tuple]:
    """Scan a Kotlin file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in KOTLIN_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "kotlin-dangerous", msg, i))

    return findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python swift_kotlin_analyzer.py <file.swift|file.kt>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if path.suffix == ".swift":
        findings = scan_swift_file(path)
    elif path.suffix == ".kt":
        findings = scan_kotlin_file(path)
    else:
        print("Unsupported file type")
        sys.exit(1)

    for sev, cat, msg, line in findings:
        print(f"[{sev}] line {line}: {msg}")
