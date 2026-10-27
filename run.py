#!/usr/bin/env python3
"""
Quick start script for SkillGate.
Run: python run.py quickstart
"""

import sys
import subprocess


def run_cmd(cmd: str):
    print(f"\n$ {cmd}")
    subprocess.run(cmd, shell=True)


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <command>")
        print()
        print("Commands:")
        print("  scan <dir>    - Scan a skill directory")
        print("  test          - Run all unit tests")
        print("  quickstart    - Show quickstart guide")
        print("  scorecard     - Run OpenSSF-inspired scorecard")
        print("  sbom          - Generate SBOM")
        return

    cmd = sys.argv[1]

    if cmd == "scan":
        if len(sys.argv) < 3:
            print("Usage: python run.py scan <skill_dir>")
            return
        run_cmd(f"python skillgate.py scan {sys.argv[2]}")

    elif cmd == "test":
        run_cmd("python tests/test_skillgate.py")

    elif cmd == "quickstart":
        run_cmd("python skillgate.py quickstart")

    elif cmd == "scorecard":
        run_cmd("python scorecard.py .")

    elif cmd == "sbom":
        run_cmd("python sbom_generator.py .")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
