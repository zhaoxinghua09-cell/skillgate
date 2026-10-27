"""
Terraform / IaC scanner for SkillGate.
Detects common security misconfigurations in Terraform HCL files.
"""

from pathlib import Path
from typing import List
import re
from skillgate import Finding


TERRAFORM_DANGEROUS_PATTERNS = [
    # Open to world
    (r"0\.0\.0\.0/0", "Security group open to 0.0.0.0/0 (world)"),
    # No encryption
    (r"encrypted\s*=\s*false", "Storage not encrypted"),
    # Public S3 bucket
    (r"acl\s*=\s*\"public-read", "S3 bucket publicly readable"),
    # No versioning
    (r"versioning\s*=\s*\{\s*enabled\s*=\s*false", "S3 versioning disabled"),
    # Root access enabled
    (r"permit_root_login\s*=\s*\"ENABLED", "SSH root login enabled"),
    # Unencrypted RDS
    (r"storage_encrypted\s*=\s*false", "RDS storage not encrypted"),
    # Publicly accessible DB
    (r"publicly_accessible\s*=\s*true", "Database publicly accessible"),
]


def scan_terraform_file(file_path: Path) -> List[Finding]:
    """Scan a Terraform .tf file for security issues."""
    findings = []

    if file_path.suffix != ".tf":
        return findings

    content = file_path.read_text(encoding="utf-8", errors="ignore")

    for pattern, message in TERRAFORM_DANGEROUS_PATTERNS:
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            findings.append(Finding(
                severity="HIGH" if "0.0.0.0/0" in message or "public" in message.lower() else "MEDIUM",
                category="iac",
                message=f"Terraform: {message}",
                file=str(file_path),
                line=line_num,
            ))

    return findings


if __name__ == "__main__":
    print("Terraform scanner loaded successfully")
