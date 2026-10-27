"""
SkillGate Dockerfile Scanner — 扫描 Dockerfile 安全问题。
"""
import re
from pathlib import Path
from typing import List, Tuple


DOCKERFILE_PATTERNS = [
    (r"^FROM\s+alpine:latest", "MEDIUM", "alpine:latest 不是固定版本"),
    (r"^FROM\s+ubuntu:latest", "MEDIUM", "ubuntu:latest 不是固定版本"),
    (r"^FROM\s+python:latest", "MEDIUM", "python:latest 不是固定版本"),
    (r"^USER\s+root", "MEDIUM", "以 root 用户运行"),
    (r"^RUN\s+apt-get\s+install.*--no-install-recommends", "LOW", "缺少 --no-install-recommends"),
    (r"^EXPOSE\s+22", "MEDIUM", "暴露 SSH 端口"),
    (r"^EXPOSE\s+0\.0\.0\.0:", "MEDIUM", "绑定到所有网络接口"),
    (r"^ADD\s+https?://", "MEDIUM", "ADD 远程 URL（应该用 curl/wget + 删除）"),
    (r"^COPY\s+--from=.*latest", "MEDIUM", "多阶段构建用了 latest tag"),
    (r"^RUN\s+pip\s+install.*--trusted-host", "HIGH", "pip 禁用 HTTPS 验证"),
    (r"^RUN\s+curl\s+.*\|\s*sh", "CRITICAL", "curl | sh 管道执行"),
    (r"^RUN\s+wget\s+.*\|\s*bash", "CRITICAL", "wget | bash 管道执行"),
]


def scan_dockerfile(filepath: Path) -> List[Tuple]:
    """Scan a Dockerfile for security issues."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    for pattern, severity, msg in DOCKERFILE_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((severity, "dockerfile", msg, i))

    return findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python dockerfile_scanner.py <Dockerfile>")
        sys.exit(1)

    findings = scan_dockerfile(Path(sys.argv[1]))
    for sev, cat, msg, line in findings:
        print(f"[{sev}] line {line}: {msg}")
