"""
SkillGate Go/Rust Analyzer — 扫描 Go 和 Rust 文件。
"""
import re
from pathlib import Path
from typing import List, Tuple


GO_DANGEROUS_PATTERNS = [
    (r"\bexec\.Command\s*\([^)]*sh\s+-c", "CRITICAL", "exec.Command shell 执行"),
    (r"\bexec\.Command\s*\([^)]*bash\s+-c", "CRITICAL", "exec.Command shell 执行"),
    (r"\bos\.Setenv\s*\(", "LOW", "os.Setenv 设置环境变量"),
    (r"\bioutil\.ReadFile\b", "MEDIUM", "ioutil.ReadFile 已废弃"),
    (r"\bunsafe\.", "HIGH", "unsafe 包绕过内存安全"),
    (r"\bcrypto/md5\b", "MEDIUM", "MD5 已不安全"),
    (r"\bcrypto/sha1\b", "MEDIUM", "SHA1 已不安全"),
    (r"\bnet/http\b", "MEDIUM", "net/http 网络库"),
    (r"\bnet\.Dial\b", "HIGH", "net.Dial 原始网络连接"),
    (r"\bos\.RemoveAll\s*\(", "HIGH", "os.RemoveAll 递归删除"),
    (r"\bioutil\.WriteFile\b", "LOW", "ioutil.WriteFile 已废弃"),
]

RUST_DANGEROUS_PATTERNS = [
    (r"\bunsafe\s*\{\s*", "HIGH", "unsafe 块绕过 Rust 安全检查"),
    (r"\bstd::env::var\s*\(", "LOW", "std::env::var 读取环境变量"),
    (r"\bstd::process::Command\s*\(", "MEDIUM", "std::process::Command 子进程调用"),
    (r"\bstd::fs::remove_dir_all\s*\(", "HIGH", "remove_dir_all 递归删除"),
    (r"\breqwest\b", "MEDIUM", "reqwest HTTP 客户端"),
    (r"\bhyper\b", "MEDIUM", "hyper HTTP 库"),
    (r"\bsqlite3\b", "MEDIUM", "sqlite3 数据库"),
    (r"\bopenssl\b", "MEDIUM", "openssl 加密库"),
]


def scan_go_file(filepath: Path) -> List[Tuple]:
    """Scan a Go file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in GO_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "go-dangerous", msg, i))

    return findings


def scan_rust_file(filepath: Path) -> List[Tuple]:
    """Scan a Rust file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in RUST_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "rust-dangerous", msg, i))

    return findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python go_rust_analyzer.py <file.go|file.rs>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if path.suffix == ".go":
        findings = scan_go_file(path)
    elif path.suffix == ".rs":
        findings = scan_rust_file(path)
    else:
        print("Unsupported file type")
        sys.exit(1)

    for sev, cat, msg, line in findings:
        print(f"[{sev}] line {line}: {msg}")
