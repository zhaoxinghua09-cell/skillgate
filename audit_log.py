"""
SkillGate Audit Log — 每次扫描都有记录（有籍）。
符合 LGD 三律之"有籍"原则：每个动作都有档案可追溯。
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class AuditEntry:
    timestamp: str
    action: str
    skill_name: str
    skill_dir: str
    trust_score: int
    grade: str
    findings_count: int
    rule_version: str


class AuditLog:
    """Persistent audit log for all SkillGate actions."""

    def __init__(self, log_path: str = ".skillgate-audit.jsonl"):
        self.log_path = Path(log_path)

    def log(self, entry: AuditEntry):
        """Append an entry to the audit log."""
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    def get_history(self, limit: int = 10) -> list[dict]:
        """Get recent scan history."""
        if not self.log_path.exists():
            return []

        entries = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                entries.append(json.loads(line.strip()))

        return entries[-limit:][::-1]  # newest first

    def print_history(self, limit: int = 10):
        """Print scan history nicely."""
        history = self.get_history(limit)

        if not history:
            print("No audit history yet.")
            return

        print("=" * 60)
        print(f"  SkillGate Audit Log (last {len(history)} scans)")
        print("=" * 60)

        for i, entry in enumerate(history, 1):
            print(f"  {i}. {entry['timestamp']}")
            print(f"     Skill: {entry['skill_name']}")
            print(f"     Score: {entry['trust_score']}/100 ({entry['grade']})")
            print(f"     Findings: {entry['findings_count']}")
            print()

        print("=" * 60)


def record_scan(result, skill_dir: str):
    """Record a scan result to the audit log."""
    audit = AuditLog()
    entry = AuditEntry(
        timestamp=datetime.now().isoformat(),
        action="scan",
        skill_name=result.skill_name,
        skill_dir=skill_dir,
        trust_score=result.trust_score,
        grade=result.grade,
        findings_count=len(result.findings),
        rule_version=result.rule_version,
    )
    audit.log(entry)


if __name__ == "__main__":
    audit = AuditLog()
    audit.print_history()
