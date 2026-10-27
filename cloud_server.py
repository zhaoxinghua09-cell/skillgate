"""
SkillGate Cloud API — 云端同步服务器（本地模拟版）。
用 Python 标准库 http.server 实现。
"""
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path


class SkillGateCloudHandler(BaseHTTPRequestHandler):
    """HTTP request handler for SkillGate Cloud API."""

    def do_GET(self):
        if self.path == "/api/health":
            self._send_json({
                "status": "ok",
                "version": "1.8.0",
                "timestamp": time.time()
            })
        elif self.path.startswith("/api/skills/"):
            skill_name = self.path.split("/")[-1]
            self._send_json({
                "name": skill_name,
                "trust_score": 95,
                "grade": "A+",
                "last_scan": "2026-10-27T12:00:00Z"
            })
        elif self.path == "/api/leaderboard":
            self._send_json({
                "skills": [
                    {"name": "iso14971-risk-matrix", "score": 100, "grade": "A+"},
                    {"name": "medxpert-termbase", "score": 96, "grade": "A+"},
                    {"name": "reg-citation-normalizer", "score": 78, "grade": "B"},
                ]
            })
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/api/scan":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Simulate scan result
            result = {
                "skill_name": data.get("skill_name", "unknown"),
                "trust_score": 90,
                "grade": "A",
                "findings_count": 2,
                "timestamp": time.time()
            }

            self._send_json(result, status=201)
        else:
            self.send_error(404, "Not Found")

    def _send_json(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run_server(port: int = 8765):
    """Start the SkillGate Cloud API server."""
    server = HTTPServer(("localhost", port), SkillGateCloudHandler)
    print(f"🛡️ SkillGate Cloud API running on http://localhost:{port}")
    print(f"  Health: http://localhost:{port}/api/health")
    print(f"  Leaderboard: http://localhost:{port}/api/leaderboard")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
