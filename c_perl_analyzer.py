"""
SkillGate C/Perl Analyzer — 扫描 C 和 Perl 文件。
"""
import re
from pathlib import Path
from typing import List, Tuple


C_DANGEROUS_PATTERNS = [
    (r"\bsystem\s*\(", "CRITICAL", "system() 执行 shell 命令"),
    (r"\bexec[lp]?[ve]?\s*\(", "CRITICAL", "exec*() 执行系统命令"),
    (r"\bpopen\s*\(", "HIGH", "popen() 管道执行"),
    (r"\bscanf\s*\([^)]*%s", "HIGH", "scanf %s 缓冲区溢出风险"),
    (r"\bgets\s*\(", "CRITICAL", "gets() 已废弃，缓冲区溢出"),
    (r"\bstrcpy\s*\(", "HIGH", "strcpy() 缓冲区溢出风险"),
    (r"\bstrcat\s*\(", "HIGH", "strcat() 缓冲区溢出风险"),
    (r"\bsprintf\s*\(", "HIGH", "sprintf() 缓冲区溢出风险"),
    (r"\bmemcpy\s*\([^)]*sizeof", "MEDIUM", "memcpy 大小检查"),
    (r"\bmalloc\s*\([^)]*getenv", "HIGH", "malloc 用 getenv 大小"),
    (r"\bfree\s*\(", "LOW", "free() 内存释放"),
    (r"\b#include\s*<openssl/", "MEDIUM", "OpenSSL 加密库"),
    (r"\b#include\s*<sqlite3.h>", "MEDIUM", "SQLite 数据库"),
]

PERL_DANGEROUS_PATTERNS = [
    (r"\beval\s*\(", "CRITICAL", "eval() 代码执行"),
    (r"\bexec\s*\(", "CRITICAL", "exec() 执行系统命令"),
    (r"\bsystem\s*\(", "CRITICAL", "system() 执行系统命令"),
    (r"\b`[^`]*\$", "HIGH", "反引号执行 shell 命令"),
    (r"\bopen\s*\([^)]*\|\s*$", "HIGH", "open 管道模式"),
    (r"\bdo\s+\$", "CRITICAL", "do 动态包含"),
    (r"\brequire\s+\$", "HIGH", "require 动态加载"),
    (r"\buse\s+\$", "HIGH", "use 动态模块"),
    (r"\b\$_\s*=\s*<", "MEDIUM", "默认变量读取输入"),
    (r"\bparam\s*\(", "MEDIUM", "CGI param 用户输入"),
]


def scan_c_file(filepath: Path) -> List[Tuple]:
    """Scan a C file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in C_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "c-dangerous", msg, i))

    return findings


def scan_perl_file(filepath: Path) -> List[Tuple]:
    """Scan a Perl file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in PERL_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "perl-dangerous", msg, i))

    return findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python c_perl_analyzer.py <file.c|file.pl>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if path.suffix == ".c":
        findings = scan_c_file(path)
    elif path.suffix == ".pl":
        findings = scan_perl_file(path)
    else:
        print("Unsupported file type")
        sys.exit(1)

    for sev, cat, msg, line in findings:
        print(f"[{sev}] line {line}: {msg}")
