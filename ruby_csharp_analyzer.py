"""
SkillGate Ruby/C# Analyzer — 扫描 Ruby 和 C# 文件。
"""
import re
from pathlib import Path
from typing import List, Tuple


RUBY_DANGEROUS_PATTERNS = [
    (r"\beval\s*\(", "CRITICAL", "eval() 代码执行"),
    (r"\bsystem\s*\(", "CRITICAL", "system() 执行系统命令"),
    (r"\bexec\s*\(", "CRITICAL", "exec() 执行系统命令"),
    (r"\b`\s*\$", "HIGH", "反引号执行 shell 命令"),
    (r"\bIO\.popen\s*\(", "HIGH", "IO.popen 管道执行"),
    (r"\bMarshal\.load\s*\(", "HIGH", "Marshal.load 反序列化"),
    (r"\bYAML\.load\s*\([^)]*\)(?![^#]*permitted_classes)", "MEDIUM", "YAML.load 不安全加载"),
    (r"\brequire\s+['\"]open-uri['\"]", "MEDIUM", "open-uri 网络库"),
    (r"\bNet::HTTP\b", "MEDIUM", "Net::HTTP 网络请求"),
    (r"\bFile\.delete\s*\(", "MEDIUM", "File.delete 删除文件"),
    (r"\bFileUtils\.rm_rf\s*\(", "HIGH", "FileUtils.rm_rf 递归删除"),
]

C_SHARP_DANGEROUS_PATTERNS = [
    (r"\bProcess\.Start\s*\(", "CRITICAL", "Process.Start 执行系统命令"),
    (r"\bProcessStartInfo\b", "HIGH", "ProcessStartInfo 子进程"),
    (r"\bAssembly\.Load\s*\(", "HIGH", "Assembly.Load 动态加载程序集"),
    (r"\bActivator\.CreateInstance\s*\(", "MEDIUM", "Activator.CreateInstance 动态实例化"),
    (r"\bBinaryFormatter\.Deserialize\b", "HIGH", "BinaryFormatter 反序列化漏洞"),
    (r"\bDESCryptoServiceProvider\b", "MEDIUM", "DES 加密已不安全"),
    (r"\bMD5\.Create\b", "MEDIUM", "MD5 哈希已不安全"),
    (r"\bSHA1\.Create\b", "MEDIUM", "SHA1 哈希已不安全"),
    (r"\bWebClient\b", "MEDIUM", "WebClient 网络下载"),
    (r"\bHttpClient\b", "MEDIUM", "HttpClient 网络请求"),
    (r"\bFile\.Delete\s*\(", "MEDIUM", "File.Delete 删除文件"),
    (r"\bDirectory\.Delete\s*\([^)]*true", "HIGH", "Directory.Delete 递归删除"),
]


def scan_ruby_file(filepath: Path) -> List[Tuple]:
    """Scan a Ruby file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in RUBY_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "ruby-dangerous", msg, i))

    return findings


def scan_csharp_file(filepath: Path) -> List[Tuple]:
    """Scan a C# file."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in C_SHARP_DANGEROUS_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                findings.append((severity, "csharp-dangerous", msg, i))

    return findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ruby_csharp_analyzer.py <file.rb|file.cs>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if path.suffix == ".rb":
        findings = scan_ruby_file(path)
    elif path.suffix == ".cs":
        findings = scan_csharp_file(path)
    else:
        print("Unsupported file type")
        sys.exit(1)

    for sev, cat, msg, line in findings:
        print(f"[{sev}] line {line}: {msg}")
