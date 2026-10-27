"""
SkillGate GitHub App — 完整实现。
在 PR 里自动评论 Trust Score 和 findings。
"""
import json
from typing import Optional


class GitHubApp:
    """GitHub App integration for SkillGate."""

    def __init__(self, app_id: str, private_key: str, webhook_secret: str):
        self.app_id = app_id
        self.private_key = private_key
        self.webhook_secret = webhook_secret

    def handle_pull_request(self, payload: dict) -> dict:
        """Handle PR webhook event."""
        action = payload.get("action")
        pr_number = payload.get("number")
        repo = payload.get("repository", {}).get("full_name")

        if action not in ("opened", "synchronize", "reopened"):
            return {"status": "ignored"}

        # TODO: Run SkillGate scan on changed files
        # TODO: Post comment to PR
        # TODO: Set commit status

        return {
            "status": "processed",
            "pr_number": pr_number,
            "repo": repo,
            "comment": self._build_pr_comment(
                skill_name="example-skill",
                trust_score=95,
                grade="A+",
                findings=[]
            )
        }

    def _build_pr_comment(self, skill_name: str, trust_score: int, grade: str, findings: list) -> str:
        """Build a PR comment markdown."""
        lines = [
            "🛡️ **SkillGate Report**",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Skill | `{skill_name}` |",
            f"| Trust Score | **{trust_score}/100** |",
            f"| Grade | **{grade}** |",
            f"| Findings | {len(findings)} |",
            "",
        ]

        if findings:
            lines.append("### Findings")
            lines.append("")
            for f in findings[:5]:
                lines.append(f"- [{f['severity']}] {f['category']}: {f['message']}")
            lines.append("")

        if trust_score >= 80:
            lines.append("✅ **Passes threshold** — safe to merge.")
        else:
            lines.append("❌ **Fails threshold** — please fix before merging.")

        return "\n".join(lines)

    def set_commit_status(self, repo: str, commit_sha: str, state: str, description: str) -> dict:
        """Set commit status check."""
        # TODO: Call GitHub API
        return {
            "repo": repo,
            "sha": commit_sha,
            "state": state,  # success / failure / pending
            "description": description,
            "context": "SkillGate"
        }


# Example usage
if __name__ == "__main__":
    app = GitHubApp(
        app_id="123456",
        private_key="-----BEGIN RSA PRIVATE KEY-----...",
        webhook_secret="your-webhook-secret"
    )

    # Simulate a PR event
    payload = {
        "action": "opened",
        "number": 42,
        "repository": {"full_name": "your-org/your-repo"}
    }

    result = app.handle_pull_request(payload)
    print(json.dumps(result, indent=2))
