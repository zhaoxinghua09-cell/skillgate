#!/usr/bin/env python3
"""skillgate-mcp — MCP Server for SkillGate

Exposes SkillGate as MCP tools so AI agents can call it directly.

Usage (in your MCP config):
    "skillgate": {
      "command": "python",
      "args": ["/path/to/skillgate-mcp.py"]
    }
"""
from __future__ import annotations

import json
import sys
import subprocess
from pathlib import Path


def send_message(msg: dict):
    """Send a JSON-RPC message over stdout."""
    print(json.dumps(msg), flush=True)


def handle_initialize(params: dict) -> dict:
    """Handle initialize request."""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "skillgate",
            "version": "0.1.0"
        }
    }


def handle_tools_list(params: dict) -> dict:
    """Handle tools/list request."""
    return {
        "tools": [
            {
                "name": "scan_skill",
                "description": "Scan an AI agent skill for security issues and get a Trust Score. "
                               "Use this BEFORE installing or publishing any skill. "
                               "Returns a 0-100 trust score, grade, and list of findings.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "skill_dir": {
                            "type": "string",
                            "description": "Path to the skill directory to scan"
                        },
                        "fail_under": {
                            "type": "integer",
                            "description": "Optional: fail if trust score is below this threshold (e.g. 90)",
                            "default": None
                        }
                    },
                    "required": ["skill_dir"]
                }
            },
            {
                "name": "bench_skill",
                "description": "Run capability benchmarks on a skill to verify it actually works. "
                               "Use this after security scan to confirm the skill functions correctly.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "skill_dir": {
                            "type": "string",
                            "description": "Path to the skill directory to benchmark"
                        }
                    },
                    "required": ["skill_dir"]
                }
            }
        ]
    }


def handle_tools_call(params: dict) -> dict:
    """Handle tools/call request."""
    tool_name = params.get("name")
    args = params.get("arguments", {})

    if tool_name == "scan_skill":
        skill_dir = args.get("skill_dir", "")
        fail_under = args.get("fail_under")

        cmd = [sys.executable, str(Path(__file__).parent / "skillgate.py"),
               "scan", skill_dir, "--format", "json"]

        if fail_under:
            cmd.extend(["--fail-under", str(fail_under)])

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        try:
            result = json.loads(proc.stdout)
        except json.JSONDecodeError:
            result = {"error": proc.stderr}

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2, ensure_ascii=False)
                }
            ]
        }

    elif tool_name == "bench_skill":
        skill_dir = args.get("skill_dir", "")

        cmd = [sys.executable, str(Path(__file__).parent / "skillbench.py"),
               "run", skill_dir]

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        return {
            "content": [
                {
                    "type": "text",
                    "text": proc.stdout + proc.stderr
                }
            ]
        }

    else:
        return {
            "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
            "isError": True
        }


def main():
    """Main MCP server loop: read JSON-RPC from stdin, write responses to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = msg.get("method", "")
        msg_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            result = handle_initialize(params)
        elif method == "tools/list":
            result = handle_tools_list(params)
        elif method == "tools/call":
            result = handle_tools_call(params)
        elif method == "notifications/initialized":
            # Just acknowledge, no response needed
            continue
        else:
            result = {"error": f"Unknown method: {method}"}

        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": result
        }
        send_message(response)


if __name__ == "__main__":
    main()
