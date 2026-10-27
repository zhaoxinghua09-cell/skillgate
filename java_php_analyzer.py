"""
SkillGate Java/PHP Analyzer — 扫描 Java 和 PHP 文件。
"""
import re
from pathlib import Path
from typing import List, Tuple


JAVA_DANGEROUS_PATTERNS = [
    (r"\bRuntime\.getRuntime\(\)\.exec\s*\(", "CRITICAL", "Runtime.exec() 执行系统命令"),
    (r"\bProcessBuilder\s*\(", "HIGH", "ProcessBuilder 子进程"),
    (r"\bSystem\.getenv\s*\(", "LOW", "System.getenv 读取环境变量"),
    (r"\bClass\.forName\s*\(", "MEDIUM", "Class.forName 动态加载类"),
    (r"\bMethod\.invoke\s*\(", "MEDIUM", "反射 Method.invoke"),
    (r"\bObjectInputStream\.readObject\b", "HIGH", "Java 反序列化"),
    (r"\bCipher\.getInstance\s*\(\s*['\"]DES", "MEDIUM", "DES 加密已不安全"),
    (r"\bMessageDigest\.getInstance\s*\(\s*['\"]MD5", "MEDIUM", "MD5 哈希已不安全"),
    (r"\bSSLContext\.getInstance\s*\(\s*['\"]TLSv1", "MEDIUM", "TLSv1 已过时"),
    (r"\bopenConnection\s*\(", "MEDIUM", "URL.openConnection 网络连接"),
]

PHP_DANGEROUS_PATTERNS = [
    (r"\beval\s*\(", "CRITICAL", "eval() 代码执行"),
    (r"\bexec\s*\(", "CRITICAL", "exec() 执行系统命令"),
    (r"\bsystem\s*\(", "CRITICAL", "system() 执行系统命令"),
    (r"\bshell_exec\s*\(", "CRITICAL", "shell_exec() 执行系统命令"),
    (r"\bpassthru\s*\(", "CRITICAL", "passthru() 执行系统命令"),
    (r"\b`\s*\$", "HIGH", "反引号执行 shell 命令"),
    (r"\bunserialize\s*\(", "HIGH", "unserialize() 反序列化漏洞"),
    (r"\bextract\s*\(\s*\$_", "HIGH", "extract() 变量覆盖"),
    (r"\b\$_GET\[", "MEDIUM", "直接使用 $_GET 用户输入"),
    (r"\b\$_POST\[", "MEDIUM", "直接使用 $_POST 用户输入"),
    (r"\b\$_REQUEST\[", "HIGH", "直接使用 $_REQUEST 用户输入"),
    (r"\bmysql_query\s*\(", "HIGH", "mysql_query SQL 注入风险"),
    (r"\bmssql_query\s*\(", "HIGH", "mssql_query SQL 注入风险"),
]


def scan_java_file(filepath: Path) -> List[Tuple]:
    """Scan a Java file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in JAVA_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "java-dangerous", msg, i))

    return findings


def scan_php_file(filepath: Path) -> List[Tuple]:
    """Scan a PHP file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in PHP_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "php-dangerous", msg, i))

    return findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python java_php_analyzer.py <file.java|file.php>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if path.suffix == ".java":
        findings = scan_java_file(path)
    elif path.suffix == ".php":
        findings = scan_php_file(path)
    else:
        print("Unsupported file type")
        sys.exit(1)

    for sev, cat, msg, line in findings:
        print(f"[{sev}] line {line}: {msg}")
