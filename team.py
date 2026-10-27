"""
SkillGate Team — 团队协作功能。
多人扫描结果对比、历史趋势、共享报告。
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class TeamReport:
    """Generate team-wide scan reports."""

    def __init__(self, team_name: str, data_dir: str = ".skillgate-team"):
        self.team_name = team_name
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def save_scan_result(self, username: str, skill_name: str, result_dict: dict):
        """Save a scan result for a team member."""
        user_dir = self.data_dir / username
        user_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{skill_name}-{timestamp}.json"

        data = {
            "username": username,
            "skill_name": skill_name,
            "timestamp": datetime.now().isoformat(),
            "result": result_dict
        }

        (user_dir / filename).write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def get_team_summary(self) -> dict:
        """Get team-wide summary."""
        all_results = []

        for user_dir in self.data_dir.iterdir():
            if not user_dir.is_dir():
                continue
            for f in user_dir.glob("*.json"):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    all_results.append(data)
                except Exception:
                    pass

        if not all_results:
            return {"total": 0, "avg_score": 0, "members": []}

        # Calculate stats
        scores = [r["result"]["trust_score"] for r in all_results]
        avg_score = sum(scores) / len(scores)

        # Per member stats
        members = {}
        for r in all_results:
            user = r["username"]
            if user not in members:
                members[user] = {"scans": 0, "total_score": 0}
            members[user]["scans"] += 1
            members[user]["total_score"] += r["result"]["trust_score"]

        for user in members:
            members[user]["avg_score"] = members[user]["total_score"] / members[user]["scans"]

        return {
            "total_scans": len(all_results),
            "avg_score": round(avg_score, 1),
            "team_size": len(members),
            "members": members
        }

    def compare_skills(self, skill1: str, skill2: str) -> dict:
        """Compare two skills side by side."""
        # This would load the latest scan for each skill and compare
        return {
            "skill1": skill1,
            "skill2": skill2,
            "note": "Feature coming soon"
        }

    def generate_team_html(self) -> str:
        """Generate an HTML team report."""
        summary = self.get_team_summary()

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SkillGate Team — {self.team_name}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #0d1117; color: #e6edf3; padding: 40px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
        .stat {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; text-align: center; }}
        .number {{ font-size: 2rem; font-weight: bold; color: #58a6ff; }}
        .label {{ color: #8b949e; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ {self.team_name} — Team Trust Report</h1>
        </div>
        <div class="stats">
            <div class="stat">
                <div class="number">{summary["total_scans"]}</div>
                <div class="label">Total Scans</div>
            </div>
            <div class="stat">
                <div class="number">{summary["avg_score"]}</div>
                <div class="label">Avg Trust Score</div>
            </div>
            <div class="stat">
                <div class="number">{summary["team_size"]}</div>
                <div class="label">Team Members</div>
            </div>
        </div>
    </div>
</body>
</html>'''

        return html


if __name__ == "__main__":
    team = TeamReport("My Team")
    summary = team.get_team_summary()
    print(json.dumps(summary, indent=2))
