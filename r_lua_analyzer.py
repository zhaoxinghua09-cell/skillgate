"""
R and Lua scanners for SkillGate.
"""

from pathlib import Path
from typing import List
from skillgate import Finding


# ── R language ──────────────────────────────────────────────────────────────

R_DANGEROUS_PATTERNS = [
    ("system\\(", "Command execution via system() call"),
    ("shell\\(", "Command execution via shell() call"),
    ("source\\(", "Source arbitrary file"),
    ("eval\\(", "Evaluate arbitrary expression"),
    ("parse\\(", "Parse and evaluate R code"),
    ("install\\.packages\\(", "Install packages from CRAN"),
    ("download\\.file\\(", "Download files from network"),
    ("unlink\\(", "Delete files"),
    ("write\\.table\\(", "Write files"),
    ("readRDS\\(", "Read serialized R objects"),
]


def scan_r_file(file_path: Path) -> List[Finding]:
    findings = []
    content = file_path.read_text(encoding="utf-8", errors="ignore")

    for pattern, message in R_DANGEROUS_PATTERNS:
        import re
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            findings.append(Finding(
                severity="HIGH" if "eval" in pattern or "system" in pattern or "shell" in pattern else "MEDIUM",
                category="dangerous-code",
                message=f"R: {message}",
                file=str(file_path),
                line=line_num,
            ))

    return findings


# ── Lua language ────────────────────────────────────────────────────────────

LUA_DANGEROUS_PATTERNS = [
    ("os\\.execute", "Command execution via os.execute()"),
    ("io\\.popen", "Command execution via io.popen()"),
    ("loadstring", "Evaluate arbitrary Lua code"),
    ("dofile", "Execute arbitrary Lua file"),
    ("loadfile", "Load arbitrary Lua file"),
    ("require", "Require arbitrary module"),
    ("os\\.remove", "Delete files"),
    ("io\\.open", "File I/O operation"),
]


def scan_lua_file(file_path: Path) -> List[Finding]:
    findings = []
    content = file_path.read_text(encoding="utf-8", errors="ignore")

    for pattern, message in LUA_DANGEROUS_PATTERNS:
        import re
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            findings.append(Finding(
                severity="HIGH" if "execute" in pattern or "popen" in pattern or "loadstring" in pattern else "MEDIUM",
                category="dangerous-code",
                message=f"Lua: {message}",
                file=str(file_path),
                line=line_num,
            ))

    return findings


if __name__ == "__main__":
    print("R and Lua scanners loaded successfully")
