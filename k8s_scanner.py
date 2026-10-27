"""
Kubernetes manifest scanner for SkillGate.
Detects common security misconfigurations in K8s YAML files.
"""

from pathlib import Path
from typing import List
import re
from skillgate import Finding


K8S_DANGEROUS_PATTERNS = [
    # Privileged container
    (r"privileged:\s*true", "Privileged container (root on host)"),
    # Run as root
    (r"runAsUser:\s*0", "Container runs as root"),
    # Host network
    (r"hostNetwork:\s*true", "Host network namespace"),
    # Host PID
    (r"hostPID:\s*true", "Host PID namespace"),
    # Host IPC
    (r"hostIPC:\s*true", "Host IPC namespace"),
    # All capabilities
    (r"add:\s*\[\s*\"ADD\"", "All Linux capabilities added"),
    # No resource limits
    (r"resources:\s*\{\s*\}", "No CPU/memory limits"),
    # Pull policy always (latest tag)
    (r":\s*latest\s*$", "Using latest tag (unpinned)"),
    # Host path mount
    (r"hostPath:", "HostPath volume mount"),
    # AllowPrivilegeEscalation
    (r"allowPrivilegeEscalation:\s*true", "Privilege escalation allowed"),
]


def scan_k8s_manifest(file_path: Path) -> List[Finding]:
    """Scan a Kubernetes YAML manifest for security issues."""
    findings = []

    if not file_path.suffix in (".yaml", ".yml"):
        return findings

    content = file_path.read_text(encoding="utf-8", errors="ignore")

    # Quick check: is it a K8s manifest?
    if not re.search(r"apiVersion:\s*", content) or not re.search(r"kind:\s*", content):
        return findings

    for pattern, message in K8S_DANGEROUS_PATTERNS:
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            findings.append(Finding(
                severity="HIGH" if "privileged" in message.lower() or "root" in message.lower() else "MEDIUM",
                category="kubernetes",
                message=f"K8s: {message}",
                file=str(file_path),
                line=line_num,
            ))

    return findings


if __name__ == "__main__":
    print("Kubernetes scanner loaded successfully")
