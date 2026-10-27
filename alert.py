"""
SkillGate Alert — Trust Score 下降时发告警通知。
支持：Webhook (Slack/Discord/飞书) / 本地日志
"""
import json
import urllib.request
from datetime import datetime
from pathlib import Path


def send_webhook_alert(webhook_url: str, skill_name: str, old_score: int, new_score: int, drop: int):
    """Send a webhook alert when Trust Score drops significantly."""
    payload = {
        "text": f"⚠️ SkillGate Alert: {skill_name} Trust Score dropped by {drop} points!\n"
                f"  Before: {old_score}/100\n"
                f"  After: {new_score}/100\n"
                f"  Time: {datetime.now().isoformat()}"
    }

    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return True
    except Exception as e:
        print(f"Webhook 发送失败: {e}")
        return False


def log_alert(skill_name: str, old_score: int, new_score: int, drop: int, log_file: str = ".skillgate-alerts.log"):
    """Log alert to local file."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "skill": skill_name,
        "old_score": old_score,
        "new_score": new_score,
        "drop": drop,
        "level": "critical" if drop >= 20 else "warning"
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"告警已记录: {json.dumps(entry, ensure_ascii=False)}")


def check_and_alert(skill_name: str, old_score: int, new_score: int, threshold: int = 10, webhook_url: str = None):
    """Check if score dropped below threshold, send alert if so."""
    drop = old_score - new_score
    if drop > threshold:
        print(f"⚠️ Trust Score 下降 {drop} 分 ({old_score} → {new_score})")
        log_alert(skill_name, old_score, new_score, drop)

        if webhook_url:
            send_webhook_alert(webhook_url, skill_name, old_score, new_score, drop)

        return True
    return False


if __name__ == "__main__":
    # Demo
    check_and_alert("test-skill", 95, 75, threshold=10)
