"""
SkillGate Docker Image Scanner — 扫描 Docker 镜像配置。
"""
import re
from pathlib import Path


DOCKER_IMAGE_PATTERNS = [
    (r":latest$", "MEDIUM", "使用 latest 标签（不可复现构建）"),
    (r":alpine$", "LOW", "使用 alpine 基础镜像（可能缺少 glibc）"),
    (r":slim$", "LOW", "使用 slim 基础镜像"),
    (r"^ubuntu:1[6-8]\.", "HIGH", "过旧的 Ubuntu 版本（已 EOL）"),
    (r"^debian:(jessie|stretch)$", "HIGH", "过旧的 Debian 版本（已 EOL）"),
    (r"^node:(8|10|12|14)\.", "HIGH", "过旧的 Node.js 版本（已 EOL）"),
    (r"^python:(2\.|3\.[0-6])", "HIGH", "过旧的 Python 版本（已 EOL）"),
]


def scan_docker_image(image_name: str) -> list[dict]:
    """Scan a Docker image name for issues."""
    findings = []

    for pattern, severity, msg in DOCKER_IMAGE_PATTERNS:
        if re.search(pattern, image_name, re.IGNORECASE):
            findings.append({
                "severity": severity,
                "message": msg,
                "image": image_name
            })

    return findings


def scan_dockerfile_images(dockerfile_path: Path) -> list[dict]:
    """Extract and scan all FROM images in a Dockerfile."""
    findings = []

    try:
        content = dockerfile_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("FROM "):
            image = line[5:].strip()
            # Remove "AS builder" suffix
            if " AS " in image:
                image = image.split(" AS ")[0]

            image_findings = scan_docker_image(image)
            for f in image_findings:
                findings.append(f)

    return findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python docker_image_scanner.py <Dockerfile>")
        sys.exit(1)

    findings = scan_dockerfile_images(Path(sys.argv[1]))
    for f in findings:
        print(f"[{f['severity']}] {f['image']}: {f['message']}")
