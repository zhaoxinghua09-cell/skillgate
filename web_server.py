"""
SkillGate Web — 本地 Web 版（简化版）。
浏览器打开就能用：扫描、看 Dashboard、看排行榜。
"""
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import sys

# 把项目根目录加到 path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class SkillGateWebHandler(BaseHTTPRequestHandler):
    """HTTP request handler for SkillGate Web."""

    def do_GET(self):
        path = self.path.split("?")[0]  # 去掉查询字符串

        # API 路由
        if path.startswith("/api/health"):
            self._send_json({
                "status": "ok",
                "version": "7.3.0",
                "timestamp": time.time()
            })
        elif path.startswith("/api/leaderboard"):
            self._send_json({
                "skills": [
                    {"name": "iso14971-risk-matrix", "score": 100, "grade": "A+"},
                    {"name": "medxpert-termbase", "score": 100, "grade": "A+"},
                    {"name": "reg-citation-normalizer", "score": 100, "grade": "A+"},
                ]
            })
        elif path.startswith("/api/registry"):
            # 注册中心 API
            from registry import REGISTRY
            skills = [
                {
                    "name": s.name,
                    "description": s.description,
                    "version": s.version,
                    "author": s.author,
                    "category": s.category,
                    "tags": s.tags,
                    "trust_score": s.trust_score
                }
                for s in REGISTRY
            ]
            self._send_json({"skills": skills, "total": len(skills)})

        elif path.startswith("/api/scan"):
            # 在线扫描 API
            skill_path = self.path.split("path=")[1] if "path=" in self.path else ""
            try:
                from skillgate import scan_skill
                result = scan_skill(skill_path)
                self._send_json({
                    "name": result.skill_name,
                    "trust_score": result.trust_score,
                    "grade": result.grade,
                    "critical": result.critical_count,
                    "high": result.high_count,
                    "medium": result.medium_count,
                    "low": result.low_count,
                })
            except Exception as e:
                self._send_json({"error": str(e)}, status=500)

        # 静态文件路由
        elif path == "/" or path == "/index.html":
            self._send_html_file("index.html")
        elif path == "/dashboard":
            self._send_html_file("dashboard.html")
        elif path == "/enterprise":
            self._send_html_file("enterprise-dashboard.html")
        elif path == "/registry":
            self._send_html_file("registry.html")
        elif path == "/proactive":
            self._send_html_file("proactive-dashboard.html")
        elif path == "/methodology":
            self._send_html_file("methodology.html")
        else:
            self._send_json({"error": "Not found"}, status=404)

    def _send_html_file(self, filename: str):
        """Send an HTML file."""
        filepath = project_root / filename
        if not filepath.exists():
            self._send_json({"error": f"{filename} not found"}, status=404)
            return

        content = filepath.read_text(encoding="utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        """Suppress request logging."""
        pass


def main():
    port = 8080
    print("=" * 60)
    print("  🌐 SkillGate Web 版")
    print("=" * 60)
    print(f"  地址: http://localhost:{port}")
    print(f"  排行榜: http://localhost:{port}/")
    print(f"  Dashboard: http://localhost:{port}/dashboard")
    print(f"  企业版: http://localhost:{port}/enterprise")
    print(f"  健康检查: http://localhost:{port}/api/health")
    print("=" * 60)
    print("  按 Ctrl+C 停止")
    print("=" * 60)

    server = HTTPServer(("localhost", port), SkillGateWebHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋 服务器已停止")


if __name__ == "__main__":
    main()
