"""
Skill Governance — 企业级治理（本地版）。
本地策略、权限控制、访问审计。
"""
import json
from pathlib import Path
from datetime import datetime


project_root = Path(__file__).parent
policy_file = project_root / "governance-policy.json"


# 默认策略
DEFAULT_POLICY = {
    "allowed_skills": "*",  # 允许所有 skill
    "blocked_skills": [],  # 禁止的 skill
    "allowed_paths": ["*"],  # 允许访问的路径
    "blocked_paths": [
        "C:\\Windows",
        "C:\\Program Files",
        "/etc",
        "/root"
    ],
    "max_scan_depth": 10,  # 最大扫描深度
    "require_approval_for": [],  # 需要审批的操作
}


def load_policy() -> dict:
    """加载治理策略。"""
    if not policy_file.exists():
        return DEFAULT_POLICY.copy()
    try:
        return json.loads(policy_file.read_text(encoding="utf-8"))
    except:
        return DEFAULT_POLICY.copy()


def save_policy(policy: dict):
    """保存治理策略。"""
    policy_file.write_text(
        json.dumps(policy, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def check_skill_allowed(skill_name: str) -> bool:
    """检查 skill 是否被允许。"""
    policy = load_policy()

    if policy["blocked_skills"] and skill_name in policy["blocked_skills"]:
        return False

    if policy["allowed_skills"] == "*":
        return True

    return skill_name in policy["allowed_skills"]


def check_path_allowed(path: str) -> bool:
    """检查路径是否被允许。"""
    policy = load_policy()

    # 检查黑名单
    for blocked in policy["blocked_paths"]:
        if blocked in path:
            return False

    # 检查白名单
    if policy["allowed_paths"] == ["*"]:
        return True

    for allowed in policy["allowed_paths"]:
        if allowed in path:
            return True

    return False


def audit_access(skill_name: str, action: str, success: bool):
    """审计访问记录。"""
    audit_file = project_root / "governance-audit.log"
    timestamp = datetime.now().isoformat()
    status = "ALLOWED" if success else "DENIED"
    log_line = f"{timestamp} | {status} | {skill_name} | {action}\n"

    with open(audit_file, "a", encoding="utf-8") as f:
        f.write(log_line)


def main():
    print("=" * 60)
    print("(")
    print("  🏛️ Skill Governance — 企业级治理（本地版）")
    print("=" * 60)

    policy = load_policy()

    print(f"\n  允许的 skill: {policy['allowed_skills']}")
    print(f"  禁止的 skill: {policy['blocked_skills'] if policy['blocked_skills'] else '无'}")
    print(f"  禁止的路径: {len(policy['blocked_paths'])} 个")
    print(f"  最大扫描深度: {policy['max_scan_depth']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
