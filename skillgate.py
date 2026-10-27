#!/usr/bin/env python3
"""skillgate — Skill 安全与质量扫描门禁

Usage:
    python skillgate scan <skill_dir>
    python skillgate scan <skill_dir> --format json
    python skillgate scan <skill_dir> --format markdown --output report.md

Exit codes:
    0 = pass (all checks green)
    1 = fail (critical/high findings)
    2 = usage error
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# Import AST analyzer
try:
    from ast_analyzer import analyze_python_file as ast_analyze
except ImportError:
    ast_analyze = None

# Import JS analyzer
try:
    from js_analyzer import scan_js_file
except ImportError:
    scan_js_file = None


# ── Check patterns ──────────────────────────────────────────────────────────

# 1. Dangerous code execution
DANGEROUS_CODE_PATTERNS = [
    (r"\beval\s*\(", "MEDIUM", "eval() 动态代码执行（工具常用，需人工判断）"),
    (r"\bexec\s*\(", "MEDIUM", "exec() 动态代码执行（工具常用，需人工判断）"),
    (r"\bos\.system\s*\(", "HIGH", "os.system() shell 调用"),
    (r"\bsubprocess\.(run|call|Popen|check_output)\s*\([^)]*shell\s*=\s*True", "HIGH", "subprocess shell=True"),
    (r"\bos\.popen\s*\(", "HIGH", "os.popen() shell 调用"),
    (r"\b__import__\s*\(", "MEDIUM", "动态 import"),
    (r"\bpickle\.load(s)?\s*\(", "HIGH", "pickle 反序列化"),
    (r"\byaml\.load\s*\([^)]*\)(?![^#]*Loader\s*=\s*SafeLoader)", "MEDIUM", "yaml.load 非安全加载"),
    (r"\bcompile\s*\([^)]*\)", "INFO", "compile() 动态代码编译（低风险）"),
    (r"\bgetattr\s*\([^)]*os\.", "MEDIUM", "getattr 动态调用 os 模块"),
    (r"\bglobals\(\)", "INFO", "globals() 访问全局命名空间（低风险）"),
    (r"\blocals\(\)", "INFO", "locals() 访问局部命名空间（低风险）"),
    (r"\binput\s*\(\)", "INFO", "input() 接受用户输入（CLI 工具常见）"),
    (r"\binput\s*\([^)]*\)", "INFO", "input() 接受用户输入（CLI 工具常见）"),
    (r"\b__builtins__\b", "INFO", "访问 __builtins__（低风险）"),
    (r"\bglobals\(\)\[", "MEDIUM", "globals() 动态修改"),
    (r"\bsetattr\s*\(", "INFO", "setattr 动态属性设置（低风险）"),
    (r"\bdelattr\s*\(", "INFO", "delattr 动态属性删除（低风险）"),
    # === 新增规则 ===
    (r"\bmarshal\.load(s)?\s*\(", "HIGH", "marshal 反序列化"),
    (r"\bshelve\.open\s*\(", "MEDIUM", "shelve 反序列化"),
    (r"\bjsonpickle\.decode\s*\(", "HIGH", "jsonpickle 反序列化"),
    (r"\byaml\.unsafe_load\s*\(", "CRITICAL", "yaml.unsafe_load 任意代码执行"),
    (r"\b__reduce__\s*\(", "MEDIUM", "__reduce__ 反序列化钩子"),
    (r"\bbuiltins\.__import__\s*\(", "MEDIUM", "builtins.__import__ 动态导入"),
    (r"\bimportlib\.import_module\s*\(", "LOW", "importlib 动态导入"),
    (r"\bctypes\.CDLL\s*\(", "HIGH", "ctypes 加载动态库"),
    (r"\bctypes\.windll\s*\(", "HIGH", "ctypes 加载 Windows DLL"),
    (r"\bctypes\.oledll\s*\(", "HIGH", "ctypes 加载 OLE DLL"),
    (r"\bdl\.open\s*\(", "HIGH", "dlopen 加载动态库"),
    (r"\bctypes\.pythonapi\b", "MEDIUM", "ctypes.pythonapi 直接调用 C API"),
]

# 2. Network calls / data exfiltration
NETWORK_PATTERNS = [
    (r"\bimport\s+requests\b", "INFO", "requests 网络库（常见）"),
    (r"\bfrom\s+requests\s+import\b", "INFO", "requests 网络库（常见）"),
    (r"\bimport\s+urllib\b", "INFO", "urllib 网络库（常见）"),
    (r"\bimport\s+http\.client\b", "INFO", "http.client 网络库"),
    (r"\bimport\s+socket\b", "LOW", "socket 原始网络连接"),
    (r"\bimport\s+ftplib\b", "LOW", "FTP 库"),
    (r"\bimport\s+smtplib\b", "LOW", "SMTP 邮件库"),
    (r"\burlopen\s*\(", "LOW", "urlopen 网络请求"),
    (r"\bpost\s*\([^)]*https?://", "MEDIUM", "POST 数据到外部 URL"),
    (r"\bhttpx\b", "INFO", "httpx HTTP 客户端（常见）"),
    (r"\baiohttp\b", "INFO", "aiohttp 异步 HTTP（常见）"),
    (r"\bcurl\b", "LOW", "curl 命令行网络工具"),
    (r"\bwget\b", "LOW", "wget 命令行网络工具"),
    (r"\bnc\s+-[el]\b", "HIGH", "netcat 反向 shell 风险"),
    (r"\bncat\b", "LOW", "ncat 网络工具"),
    (r"\btelnetlib\b", "HIGH", "telnetlib 明文传输"),
    (r"\bparamiko\b", "LOW", "paramiko SSH 库"),
    (r"\bscp\b", "LOW", "scp 文件传输"),
]

# 3. Credential / secret access
CREDENTIAL_PATTERNS = [
    (re.compile(r"(api[_-]?key|apikey|secret|token|password|passwd|credential)\s*[:=]\s*['\"]([^'\"]{8,})['\"]", re.IGNORECASE),
     "CRITICAL", "硬编码凭证"),
    (re.compile(r"os\.environ\[['\"](.*TOKEN|.*KEY|.*SECRET|.*PASSWORD)['\"]\]", re.IGNORECASE),
     "INFO", "从环境变量读凭证（安全做法）"),
    (re.compile(r"os\.getenv\s*\(\s*['\"](.*TOKEN|.*KEY|.*SECRET|.*PASSWORD)", re.IGNORECASE),
     "INFO", "从环境变量读凭证（安全做法）"),
    (re.compile(r"~\.ssh/", re.IGNORECASE),
     "HIGH", "访问 SSH 密钥目录"),
    (re.compile(r"\.aws/credentials", re.IGNORECASE),
     "HIGH", "访问 AWS 凭证文件"),
    (re.compile(r"\.git-credentials", re.IGNORECASE),
     "HIGH", "访问 Git 凭证文件"),
    (re.compile(r"\.netrc", re.IGNORECASE),
     "MEDIUM", "访问 .netrc 凭证文件"),
    (re.compile(r"\.npmrc", re.IGNORECASE),
     "MEDIUM", "访问 .npmrc 凭证文件"),
    (re.compile(r"\.pypirc", re.IGNORECASE),
     "MEDIUM", "访问 .pypirc 凭证文件"),
    (re.compile(r"id_rsa", re.IGNORECASE),
     "HIGH", "访问 SSH 私钥"),
    (re.compile(r"id_ed25519", re.IGNORECASE),
     "HIGH", "访问 SSH 私钥"),
]

# 4. File system danger
FILESYSTEM_PATTERNS = [
    (r"\bshutil\.rmtree\s*\(", "MEDIUM", "shutil.rmtree 递归删除"),
    (r"\bos\.remove\s*\(", "INFO", "os.remove 删除文件（常见）"),
    (r"\bos\.rmdir\s*\(", "INFO", "os.rmdir 删除目录（常见）"),
    (r"\bos\.unlink\s*\(", "MEDIUM", "os.unlink 删除文件"),
    (r"\bopen\s*\([^)]*['\"]/etc/", "HIGH", "写入 /etc/ 系统目录"),
    (r"\bopen\s*\([^)]*['\"]C:\\\\Windows\\\\", "HIGH", "写入 Windows 系统目录"),
    (r"\bopen\s*\([^)]*['\"]/System/", "HIGH", "写入 macOS 系统目录"),
    (r"\bos\.rename\s*\([^)]*/etc/", "MEDIUM", "重命名 /etc/ 下文件"),
    (r"\bshutil\.move\s*\([^)]*/etc/", "MEDIUM", "移动文件到 /etc/"),
    (r"\btempfile\.mkdtemp\b", "LOW", "创建临时目录"),
    (r"\btempfile\.mktemp\b", "MEDIUM", "mktemp 临时文件竞争风险"),
]

# 5. Prompt injection / LLM-specific risks
PROMPT_INJECTION_PATTERNS = [
    (r"ignore\s+previous\s+instructions", "CRITICAL", "Prompt injection: ignore previous"),
    (r"disregard\s+all\s+previous", "CRITICAL", "Prompt injection: disregard previous"),
    (r"you\s+are\s+now\s+a?n?\s+\w+", "MEDIUM", "Prompt injection: persona override"),
    (r"system\s+prompt\s+leak", "HIGH", "System prompt leak attempt"),
    (r"jailbreak", "CRITICAL", "Jailbreak pattern"),
    (r"reveal\s+your\s+instructions", "HIGH", "Reveal system instructions attempt"),
    (r"reveal\s+your\s+prompt", "HIGH", "Reveal system prompt attempt"),
    (r"bypass\s+safety", "HIGH", "Bypass safety guardrails"),
    (r"do\s+not\s+tell\s+the\s+user", "MEDIUM", "Hide actions from user"),
    (r"do\s+not\s+mention", "LOW", "Instructed to omit information"),
    (r"pretend\s+you\s+are", "MEDIUM", "Pretend persona override"),
    (r"act\s+as\s+if\s+you\s+are", "MEDIUM", "Act as persona override"),
    (r"forget\s+your\s+rules", "CRITICAL", "Forget your rules"),
    (r"override\s+your\s+guidelines", "CRITICAL", "Override guidelines"),
    (r"ignore\s+your\s+training", "CRITICAL", "Ignore training"),
]

# 6. Excessive agency / MCP risks
EXCESSIVE_AGENCY_PATTERNS = [
    (r"delete\s+all\s+files", "CRITICAL", "Excessive agency: delete all files"),
    (r"send\s+all\s+data", "HIGH", "Excessive agency: exfiltrate all data"),
    (r"run\s+arbitrary\s+commands", "HIGH", "Arbitrary command execution"),
    (r"access\s+all\s+files", "MEDIUM", "Overly broad file access"),
    (r"read\s+every\s+file", "HIGH", "Read every file"),
    (r"modify\s+all\s+configs", "HIGH", "Modify all configs"),
    (r"install\s+any\s+package", "MEDIUM", "Install any package"),
    (r"unrestricted\s+internet\s+access", "MEDIUM", "Unrestricted internet access"),
    (r"bypass\s+all\s+safety\s+checks", "CRITICAL", "Bypass all safety checks"),
    (r"disable\s+all\s+filters", "HIGH", "Disable all filters"),
    (r"grant\s+yourself\s+admin", "CRITICAL", "Grant yourself admin access"),
    (r"add\s+new\s+user\s+accounts", "HIGH", "Add new user accounts"),
]

# 7. License compliance
LICENSE_PATTERNS = [
    (r"\bGPL\b", "MEDIUM", "GPL 许可证（传染性）"),
    (r"\bAGPL\b", "HIGH", "AGPL 许可证（网络传染性）"),
    (r"\bSSPL\b", "HIGH", "SSPL 许可证（服务端传染性）"),
    (r"\bUnlicense\b", "LOW", "Unlicense（公有领域）"),
]

# 8. Code quality
QUALITY_PATTERNS = [
    (r"\bTODO\b", "LOW", "TODO 注释未完成"),
    (r"\bFIXME\b", "LOW", "FIXME 注释未修复"),
    (r"\bHACK\b", "LOW", "HACK 临时方案"),
    (r"\bXXX\b", "LOW", "XXX 标记的问题"),
    (r"\bprint\s*\(", "LOW", "print 调试语句"),
    (r"\bconsole\.log\(", "LOW", "console.log 调试语句"),
    (r"\bdebugger\b", "MEDIUM", "debugger 语句"),
]

# 9. Authentication & Authorization
AUTH_PATTERNS = [
    (r"\bauth\s*=\s*None\b", "MEDIUM", "认证被禁用"),
    (r"\bverify\s*=\s*False\b", "HIGH", "SSL 验证被禁用"),
    (r"\bALLOW_ALL\b", "HIGH", "允许所有访问"),
    (r"\bCORS.*\*\b", "MEDIUM", "CORS 允许所有来源"),
    (r"\bpassword\s*=\s*['\"][^'\"]+['\"]", "CRITICAL", "硬编码密码"),
    (r"\btoken\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]", "CRITICAL", "硬编码 token"),
]

# 10. Input Validation
VALIDATION_PATTERNS = [
    (r"\brequest\.args\.get\(", "LOW", "直接读取请求参数"),
    (r"\binput\s*\(", "MEDIUM", "读取用户输入"),
    (r"\bsys\.argv\b", "LOW", "读取命令行参数"),
    (r"\bos\.environ\[", "MEDIUM", "读取环境变量"),
]

# 11. Data Exfiltration Risk
EXFIL_PATTERNS = [
    (r"\brequests\.post\([^)]*https?://", "MEDIUM", "向外发 POST 请求"),
    (r"\burllib\.request\.urlopen\(", "MEDIUM", "向外发请求"),
    (r"\bsmtplib\.SMTP\(", "MEDIUM", "发送邮件"),
    (r"\bsocket\.socket\(", "MEDIUM", "原始 socket 网络连接"),
]

FRONTMATTER_REQUIRED_FIELDS = ["name", "description"]
FRONTMATTER_OPTIONAL_FIELDS = ["version", "license", "author", "tags"]

STDLIB_MODULES = {
    "argparse", "ast", "base64", "collections", "copy", "csv", "datetime",
    "functools", "hashlib", "itertools", "json", "logging", "math",
    "os", "pathlib", "pickle", "platform", "random", "re", "shutil",
    "sqlite3", "string", "sys", "tempfile", "time", "typing", "urllib",
    "xml", "zipfile", "__future__", "abc", "asyncio", "dataclasses",
    "enum", "io", "socket", "subprocess", "threading", "unittest",
    "warnings", "weakref",
}


# ── Data classes ──────────────────────────────────────────────────────────

# Category explanations (有证：每个结论有解释)
CATEGORY_EXPLANATIONS = {
    "dangerous-code": "检测到危险代码模式，可能导致代码执行或系统破坏",
    "credential-leak": "检测到硬编码凭证或敏感信息泄露",
    "prompt-injection": "检测到 prompt 注入风险，可能被绕过安全限制",
    "excessive-agency": "检测到过度权限，可能超出预期的操作范围",
    "network": "检测到网络请求，注意数据外带风险",
    "filesystem": "检测到文件系统操作，注意删除和写入风险",
    "deserialization": "检测到不安全的反序列化，可能导致 RCE",
    "dependency": "检测到有风险的依赖包",
    "license": "检测到许可证合规问题",
    "code-quality": "代码质量问题，不影响安全但影响可维护性",
    "auth": "认证授权相关问题",
    "input-validation": "输入验证相关问题",
    "exfiltration": "数据外带风险",
    "ast-analysis": "AST 语法树分析发现的问题",
    "structure": "项目结构问题",
    "file-read": "文件读取问题",
}


@dataclass
class Finding:
    severity: str  # CRITICAL / HIGH / MEDIUM / LOW
    category: str
    message: str
    file: str
    line: Optional[int] = None
    rule_id: str = ""  # 规则唯一 ID
    explanation: str = ""  # 为什么报这个


@dataclass
class ScanResult:
    skill_name: str = ""
    skill_dir: str = ""
    findings: list[Finding] = field(default_factory=list)
    files_scanned: int = 0
    frontmatter: dict = field(default_factory=dict)
    trust_score: int = 0
    grade: str = ""
    rule_version: str = "v3.0.0"  # 规则版本号（有籍）

    @property
    def critical_count(self): return len([f for f in self.findings if f.severity == "CRITICAL"])
    @property
    def high_count(self): return len([f for f in self.findings if f.severity == "HIGH"])
    @property
    def medium_count(self): return len([f for f in self.findings if f.severity == "MEDIUM"])
    @property
    def low_count(self): return len([f for f in self.findings if f.severity == "LOW"])


# ── Scanners ──────────────────────────────────────────────────────────────

def scan_python_file(filepath: Path, result: ScanResult):
    """Scan a single Python file for dangerous patterns."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result.findings.append(Finding(
            severity="LOW", category="file-read",
            message=f"无法读取文件: {e}", file=str(filepath)
        ))
        return

    # === 第一步：AST 分析（更准，误报低） ===
    ast_lines = set()  # 记录 AST 已经报过的行，正则就不要重复报了
    try:
        from ast_analyzer import analyze_python_file
        ast_findings = analyze_python_file(filepath)
        for af in ast_findings:
            result.findings.append(Finding(
                severity=af.severity,
                category="ast-analysis",
                message=f"[AST] {af.message}",
                file=str(filepath),
                line=af.line
            ))
            ast_lines.add(af.line)  # 记录这一行已经报过了
    except Exception:
        pass  # AST 分析失败不影响正则扫描

    lines = content.splitlines()

    # Helper: check if line is a comment
    def is_comment_line(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''")

    # Helper: check if match is inside a string (simple heuristic)
    def is_inside_string(line: str, match_start: int) -> bool:
        """Simple heuristic: check if the match position is inside a string literal."""
        # Count quotes before the match
        before = line[:match_start]
        # Count unescaped quotes
        single_quotes = before.count("'") - before.count("\\'")
        double_quotes = before.count('"') - before.count('\\"')
        # If odd number of either, we're inside a string
        return (single_quotes % 2 == 1) or (double_quotes % 2 == 1)

    # Helper: check if line has skillgate: ignore suppression
    def is_suppressed(line_idx: int) -> bool:
        """Check if the current line or previous line has # skillgate: ignore"""
        # Check current line
        if 0 < line_idx <= len(lines):
            if "skillgate: ignore" in lines[line_idx - 1]:
                return True
        # Check previous line
        if line_idx > 1:
            if "skillgate: ignore" in lines[line_idx - 2]:
                return True
        return False

    # 1. Dangerous code patterns
    for pattern, severity, msg in DANGEROUS_CODE_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if is_suppressed(i):
                continue
            if i in ast_lines:  # AST 已经报过了，不要重复报
                continue
            if re.search(pattern, line):
                result.findings.append(Finding(
                    severity=severity, category="dangerous-code",
                    message=msg, file=str(filepath), line=i
                ))

    # 2. Network patterns
    for pattern, severity, msg in NETWORK_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if is_suppressed(i):
                continue
            if re.search(pattern, line):
                result.findings.append(Finding(
                    severity=severity, category="network",
                    message=msg, file=str(filepath), line=i
                ))

    # 3. Credential / secret patterns
    for pattern, severity, msg in CREDENTIAL_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if pattern.search(line):
                result.findings.append(Finding(
                    severity=severity, category="credential-leak",
                    message=msg, file=str(filepath), line=i
                ))

    # 4. Filesystem danger patterns
    for pattern, severity, msg in FILESYSTEM_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if re.search(pattern, line):
                result.findings.append(Finding(
                    severity=severity, category="filesystem",
                    message=msg, file=str(filepath), line=i
                ))

    # 5. Excessive agency patterns
    for pattern, severity, msg in EXCESSIVE_AGENCY_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if re.search(pattern, line, re.IGNORECASE):
                result.findings.append(Finding(
                    severity=severity, category="excessive-agency",
                    message=msg, file=str(filepath), line=i
                ))

    # 6. AST analysis (higher precision, lower false positive)
    if ast_analyze:
        try:
            ast_findings = ast_analyze(filepath)
            for af in ast_findings:
                result.findings.append(Finding(
                    severity=af.severity, category="ast-analysis",
                    message=af.message, file=str(filepath), line=af.line
                ))
        except Exception:
            pass


def scan_md_file(filepath: Path, result: ScanResult):
    """Scan a Markdown file for prompt injection patterns."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    lines = content.splitlines()
    for pattern, severity, msg in PROMPT_INJECTION_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                result.findings.append(Finding(
                    severity=severity, category="prompt-injection",
                    message=msg, file=str(filepath), line=i
                ))


def scan_dependencies(skill_path: Path, result: ScanResult):
    """Scan dependencies for known vulnerabilities via OSV.dev."""
    # Find requirements.txt
    req_file = skill_path / "requirements.txt"
    if not req_file.exists():
        return

    try:
        content = req_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    deps = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Parse package name and version
        if "==" in line:
            name, version = line.split("==", 1)
            deps.append((name.strip(), version.strip()))
        elif ">=" in line:
            name = line.split(">=", 1)[0].strip()
            deps.append((name, "latest"))

    if not deps:
        return

    # Query OSV.dev for each dependency
    for name, version in deps[:10]:  # limit to 10 deps to avoid timeout
        try:
            payload = json.dumps({
                "package": {"name": name, "ecosystem": "PyPI"},
                "version": version
            }).encode()

            req = urllib.request.Request(
                "https://api.osv.dev/v1/query",
                data=payload,
                headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=5) as resp:  # nosec B310 - URL is fixed GitHub API, not user input
                data = json.loads(resp.read())
                vulns = data.get("vulns", [])
                if vulns:
                    for v in vulns[:3]:  # top 3 vulns per dep
                        result.findings.append(Finding(
                            severity="HIGH", category="dependency-vuln",
                            message=f"{name}=={version}: {v.get('summary', 'known vulnerability')}",
                            file=str(req_file)
                        ))
        except Exception:
            # Offline fallback: just note that we couldn't check
            result.findings.append(Finding(
                severity="LOW", category="dependency-scan",
                message=f"无法联网检查 {name} 的已知漏洞",
                file=str(req_file)
            ))


def scan_shell_file(filepath: Path, result: ScanResult):
    """Scan a shell script for dangerous patterns."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    lines = content.splitlines()
    dangerous_sh_patterns = [
        (r"\brm\s+-rf?\s+/", "CRITICAL", "rm -rf / 危险删除"),
        (r"\bcurl\s+.*\|\s*sh", "HIGH", "curl | sh 管道执行远程脚本"),
        (r"\bwget\s+.*\|\s*bash", "HIGH", "wget | bash 管道执行远程脚本"),
        (r"\bchmod\s+777", "MEDIUM", "chmod 777 权限过松"),
        (r"\bsudo\s+", "MEDIUM", "sudo 权限提升"),
    ]

    for pattern, severity, msg in dangerous_sh_patterns:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                result.findings.append(Finding(
                    severity=severity, category="dangerous-shell",
                    message=msg, file=str(filepath), line=i
                ))


def parse_frontmatter(filepath: Path, result: ScanResult):
    """Parse YAML frontmatter from SKILL.md."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    if not content.startswith("---"):
        result.findings.append(Finding(
            severity="MEDIUM", category="frontmatter",
            message="SKILL.md 缺少 YAML frontmatter", file=str(filepath)
        ))
        return

    end = content.find("---", 3)
    if end == -1:
        result.findings.append(Finding(
            severity="MEDIUM", category="frontmatter",
            message="SKILL.md frontmatter 未闭合", file=str(filepath)
        ))
        return

    fm_text = content[3:end].strip()
    # Simple YAML parsing (enough for frontmatter)
    current_key = None
    for line in fm_text.splitlines():
        if line.startswith("- "):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            result.frontmatter[key] = value

    # Check required fields
    for field_name in FRONTMATTER_REQUIRED_FIELDS:
        if field_name not in result.frontmatter:
            result.findings.append(Finding(
                severity="LOW", category="frontmatter",
                message=f"缺少必填字段: {field_name}", file=str(filepath)
            ))

    result.skill_name = result.frontmatter.get("name", filepath.parent.name)


def compute_trust_score(result: ScanResult) -> int:
    """Weighted Trust Score calculation.

    Weights:
    - CRITICAL: -15 each
    - HIGH: -8 each
    - MEDIUM: -4 each
    - LOW: -1 each
    - Missing frontmatter required fields: -10
    """
    score = 100

    # Weighted deductions by severity
    score -= result.critical_count * 15
    score -= result.high_count * 8
    score -= result.medium_count * 4
    score -= result.low_count * 1

    # Frontmatter completeness penalty
    fm = result.frontmatter
    if not fm:
        score -= 20
    else:
        required_present = sum(1 for f in FRONTMATTER_REQUIRED_FIELDS if fm.get(f))
        if required_present < len(FRONTMATTER_REQUIRED_FIELDS):
            score -= 10

    # Clamp to 0-100
    return max(0, min(100, score))

    # Zero dependencies bonus
    has_network = any(f.category == "network" for f in result.findings)
    if not has_network:
        score += 2

    return max(0, min(100, score))


def grade_from_score(score: int) -> str:
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 40: return "D"
    return "F"


def generate_badge(result: ScanResult) -> str:
    """Generate a shields.io-style SVG badge for Trust Score."""
    score = result.trust_score
    grade = result.grade

    # Color based on score
    if score >= 90:
        color = "brightgreen"
    elif score >= 75:
        color = "green"
    elif score >= 60:
        color = "yellow"
    elif score >= 40:
        color = "orange"
    else:
        color = "red"

    label = "trust score"
    value = f"{score}/100 {grade}"

    # Simple SVG badge (shields.io style)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="120" height="20">
  <linearGradient id="smooth" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="round">
    <rect width="120" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#round)">
    <rect width="60" height="20" fill="#555"/>
    <rect width="60" height="20" x="60" fill="{color}"/>
    <rect width="120" height="20" fill="url(#smooth)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="30" y="14" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="30" y="13">{label}</text>
    <text x="90" y="14" fill="#010101" fill-opacity=".3">{value}</text>
    <text x="90" y="13">{value}</text>
  </g>
</svg>'''
    return svg


# ── Main ───────────────────────────────────────────────────────────────────

def find_skill_documents(skill_path: Path) -> list[Path]:
    """Find skill definition files in any supported format.

    Supports:
    - SKILL.md (Claude Code / standard)
    - AGENTS.md (Codex / OpenCode)
    - .cursorrules / .cursor/rules/*.md (Cursor)
    - *.md in root (generic fallback)
    """
    docs = []

    # Standard SKILL.md
    if (skill_path / "SKILL.md").exists():
        docs.append(skill_path / "SKILL.md")

    # AGENTS.md (Codex/OpenCode)
    if (skill_path / "AGENTS.md").exists():
        docs.append(skill_path / "AGENTS.md")

    # .cursorrules (Cursor)
    if (skill_path / ".cursorrules").exists():
        docs.append(skill_path / ".cursorrules")

    # .cursor/rules/*.md (Cursor modern format)
    cursor_rules = skill_path / ".cursor" / "rules"
    if cursor_rules.is_dir():
        docs.extend(cursor_rules.glob("*.md"))

    # .claude/skills/*.md (Claude Code plugin format)
    claude_skills = skill_path / ".claude" / "skills"
    if claude_skills.is_dir():
        docs.extend(claude_skills.glob("*/SKILL.md"))

    # .agents/skills/*.md (OpenCode format)
    agents_skills = skill_path / ".agents" / "skills"
    if agents_skills.is_dir():
        docs.extend(agents_skills.glob("*/SKILL.md"))

    # Fallback: any top-level .md file (but not README)
    if not docs:
        for md in skill_path.glob("*.md"):
            if md.name.lower() != "readme.md":
                docs.append(md)

    return docs


def scan_skill(skill_dir: str) -> ScanResult:
    skill_path = Path(skill_dir).resolve()
    if not skill_path.is_dir():
        print(f"错误: 目录不存在 - {skill_dir}", file=sys.stderr)
        sys.exit(2)

    # 安全检查：不允许扫描系统敏感目录（防路径遍历攻击）
    SENSITIVE_DIRS = ["/etc", "/proc", "/sys", "C:\\Windows", "C:\\Program Files"]
    for sensitive in SENSITIVE_DIRS:
        if str(skill_path).lower().startswith(sensitive.lower()):
            print(f"安全限制: 不允许扫描系统敏感目录 ({sensitive})", file=sys.stderr)
            sys.exit(3)

    result = ScanResult(skill_dir=str(skill_path))

    # Default excluded directories
    DEFAULT_EXCLUDES = {"tests", "test", "docs", "doc", ".git", "__pycache__", "node_modules"}

    def should_exclude(filepath: Path) -> bool:
        """Check if a file should be excluded from scanning."""
        parts = filepath.relative_to(skill_path).parts
        for part in parts:
            if part in DEFAULT_EXCLUDES:
                return True
        return False

    # Find skill definition files in any supported format
    skill_docs = find_skill_documents(skill_path)

    if not skill_docs:
        result.findings.append(Finding(
            severity="HIGH", category="structure",
            message="未找到任何 skill 定义文件（SKILL.md / AGENTS.md / .cursorrules）",
            file=str(skill_path)
        ))
    else:
        for doc in skill_docs:
            # Try to parse frontmatter (only if it starts with ---)
            try:
                content = doc.read_text(encoding="utf-8", errors="replace")
                if content.startswith("---"):
                    parse_frontmatter(doc, result)
            except Exception:
                pass
            scan_md_file(doc, result)
            result.files_scanned += 1

    # Scan all Python files
    for py_file in skill_path.rglob("*.py"):
        if should_exclude(py_file):
            continue
        scan_python_file(py_file, result)
        result.files_scanned += 1

    # Scan all shell scripts
    for sh_file in skill_path.rglob("*.sh"):
        if should_exclude(sh_file):
            continue
        scan_shell_file(sh_file, result)
        result.files_scanned += 1

    # Scan all JS/TS files
    if scan_js_file:
        for js_file in list(skill_path.rglob("*.js")) + list(skill_path.rglob("*.ts")):
            if should_exclude(js_file):
                continue
            try:
                js_findings = scan_js_file(js_file)
                for sev, cat, msg, line in js_findings:
                    result.findings.append(Finding(
                        severity=sev, category=cat,
                        message=msg, file=str(js_file), line=line
                    ))
            except Exception:
                pass
            result.files_scanned += 1

    # Scan all Markdown files (excluding already-scanned skill docs)
    for md_file in skill_path.rglob("*.md"):
        if md_file in skill_docs:
            continue
        if should_exclude(md_file):
            continue
        scan_md_file(md_file, result)
        result.files_scanned += 1

    # Scan dependencies for known vulnerabilities
    scan_dependencies(skill_path, result)

    # Compute score
    result.trust_score = compute_trust_score(result)
    result.grade = grade_from_score(result.trust_score)

    return result


def print_terminal_report(result: ScanResult, fail_under: int = None):
    print(f"\n{'='*60}")
    print(f"  SkillGate 扫描报告")
    print(f"{'='*60}")
    print(f"  Skill: {result.skill_name}")
    print(f"  目录: {result.skill_dir}")
    print(f"  扫描文件数: {result.files_scanned}")
    print(f"{'='*60}")
    print(f"  Trust Score: {result.trust_score}/100  ({result.grade})")
    print(f"{'='*60}")

    if not result.findings:
        print("  ✅ 全部检查通过，无发现")
    else:
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_findings = sorted(result.findings, key=lambda f: severity_order.get(f.severity, 99))
        for f in sorted_findings:
            icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(f.severity, "⚪")
            loc = f"{f.file}:{f.line}" if f.line else f.file
            print(f"  {icon} [{f.severity}] {f.category}: {f.message}")
            print(f"      {loc}")

    print(f"{'='*60}")

    # Determine exit code
    exit_code = 0
    if result.critical_count > 0 or result.high_count > 0:
        print(f"  ❌ 阻断发布: {result.critical_count} CRITICAL, {result.high_count} HIGH")
        exit_code = 1
    elif fail_under is not None and result.trust_score < fail_under:
        print(f"  ❌ 阻断发布: Trust Score {result.trust_score} < 阈值 {fail_under}")
        exit_code = 1
    else:
        print(f"  ✅ 通过: {result.medium_count} MEDIUM, {result.low_count} LOW")

    return exit_code


def generate_sarif(result: ScanResult) -> str:
    """Generate SARIF 2.1.0 output for GitHub Code Scanning."""
    # Map our severities to SARIF levels
    severity_map = {
        "CRITICAL": "error",
        "HIGH": "error",
        "MEDIUM": "warning",
        "LOW": "note",
    }

    rules = {}
    sarif_results = []

    for f in result.findings:
        rule_id = f"skillgate/{f.category}"
        if rule_id not in rules:
            rules[rule_id] = {
                "id": rule_id,
                "name": f.category,
                "shortDescription": {"text": f.message},
                "fullDescription": {"text": f.message},
                "defaultConfiguration": {"level": severity_map.get(f.severity, "warning")},
            }

        sarif_results.append({
            "ruleId": rule_id,
            "level": severity_map.get(f.severity, "warning"),
            "message": {"text": f.message},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": f.file},
                    "region": {"startLine": f.line or 1}
                }
            }]
        })

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "SkillGate",
                    "version": "0.2.0",
                    "informationUri": "https://github.com/your-org/skillgate",
                    "rules": list(rules.values())
                }
            },
            "results": sarif_results
        }]
    }

    return json.dumps(sarif, indent=2, ensure_ascii=False)


def generate_junit_xml(result: ScanResult) -> str:
    """Generate JUnit XML output for CI test reporting."""
    import xml.etree.ElementTree as ET
    from xml.dom import minidom

    testsuites = ET.Element("testsuites")
    testsuite = ET.SubElement(testsuites, "testsuite", {
        "name": "SkillGate",
        "tests": str(len(result.findings) + 1),  # +1 for overall score
        "failures": str(result.critical_count + result.high_count),
        "errors": "0",
        "time": "0.1"
    })

    # Overall score test
    overall_test = ET.SubElement(testsuite, "testcase", {
        "name": f"Trust Score: {result.trust_score}/100",
        "classname": "skillgate.overall"
    })
    if result.trust_score < 80:
        failure = ET.SubElement(overall_test, "failure", {
            "message": f"Score {result.trust_score} below threshold 80"
        })

    # Individual findings as test cases
    for i, f in enumerate(result.findings):
        testcase = ET.SubElement(testsuite, "testcase", {
            "name": f"{f.category}: {f.message[:50]}",
            "classname": f"skillgate.{f.category}"
        })
        if f.severity in ("CRITICAL", "HIGH"):
            failure = ET.SubElement(testcase, "failure", {
                "message": f"[{f.severity}] {f.message}"
            })

    # Pretty print
    rough = ET.tostring(testsuites, encoding="unicode")
    pretty = minidom.parseString(rough).toprettyxml(indent="  ")  # nosec B318 - XML is self-generated, not untrusted input
    return pretty


def generate_agent_summary(result: ScanResult) -> str:
    """Generate a short, agent-friendly summary that can be relayed to the user."""
    score = result.trust_score
    grade = result.grade
    name = result.skill_name

    if score >= 90:
        verdict = "SAFE: ok to use."
        detail = f"Trust Score {score}/100 ({grade}), no critical issues."
    elif score >= 75:
        verdict = "MOSTLY SAFE: usable, minor issues."
        detail = f"Trust Score {score}/100 ({grade}), {result.medium_count} medium findings."
    elif score >= 60:
        verdict = "CAUTION: review findings before use."
        detail = f"Trust Score {score}/100 ({grade}), {result.high_count} high findings."
    else:
        verdict = "UNSAFE: do not install."
        detail = f"Trust Score {score}/100 ({grade}), {result.critical_count} critical findings."

    lines = [
        f"SKILLGATE_RESULT",
        f"SKILL: {name}",
        f"SCORE: {score}/100",
        f"GRADE: {grade}",
        f"VERDICT: {verdict}",
        f"DETAIL: {detail}",
    ]

    if result.findings:
        lines.append(f"TOP_FINDINGS:")
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_findings = sorted(result.findings, key=lambda f: severity_order.get(f.severity, 99))[:5]
        for f in sorted_findings:
            lines.append(f"  - [{f.severity}] {f.category}: {f.message}")

    # Add fix suggestions
    fix_suggestions = generate_fix_suggestions(result)
    if fix_suggestions:
        lines.append(f"\n修复建议：")
        for s in fix_suggestions:
            lines.append(f"  → {s}")

    return "\n".join(lines)


def generate_fix_suggestions(result: ScanResult) -> list[str]:
    """Generate actionable fix suggestions based on findings."""
    suggestions = []
    categories = {f.category for f in result.findings}

    if "dangerous-code" in categories:
        suggestions.append("替换 eval/exec 为安全的替代方案（ast.literal_eval / 直接类型转换）")
        suggestions.append("避免 shell=True，用列表参数传 subprocess")

    if "network" in categories:
        suggestions.append("如果 skill 不需要联网，移除 requests/urllib 等网络依赖")
        suggestions.append("如果必须联网，在 SKILL.md 里声明需要网络权限")

    if "credential-leak" in categories:
        suggestions.append("硬编码凭证改用环境变量：os.getenv('API_KEY')")
        suggestions.append("不要把 .env 文件提交到 git")

    if "prompt-injection" in categories:
        suggestions.append("移除任何试图绕过 system prompt 的指令")
        suggestions.append("不要在 skill 里写 'ignore previous instructions' 这类内容")

    if "filesystem" in categories:
        suggestions.append("避免递归删除操作，或者加白名单检查路径")
        suggestions.append("不要写入系统目录（/etc/, C:\\Windows\\）")

    if "frontmatter" in categories:
        suggestions.append("在 SKILL.md 头部补全 frontmatter：name, description, version, license, author")

    return suggestions


def main():
    ap = argparse.ArgumentParser(description="SkillGate — Skill 安全与质量扫描门禁")
    sub = ap.add_subparsers(dest="command")

    scan_parser = sub.add_parser("scan", help="扫描一个 skill 目录")
    scan_parser.add_argument("skill_dir", help="skill 目录路径")
    scan_parser.add_argument("--format", choices=["terminal", "json", "markdown", "agent", "sarif", "junit"], default="terminal")
    scan_parser.add_argument("--output", help="输出文件路径（默认 stdout）")
    scan_parser.add_argument("--fail-under", type=int, default=None,
                             help="CI 模式：Trust Score 低于此值则 exit 1")
    scan_parser.add_argument("--badge", help="生成 SVG badge 到指定路径")
    scan_parser.add_argument("--batch", action="store_true",
                             help="批量扫描：扫描目录下所有子目录")
    scan_parser.add_argument("--lenient", action="store_true",
                             help="宽松模式：所有规则降一级别（减少误报）")

    # Quickstart subcommand
    quickstart_parser = sub.add_parser("quickstart", help="快速演示 SkillGate 怎么用")

    args = ap.parse_args()

    if args.command == "quickstart":
        print("=" * 60)
        print("  🛡️  SkillGate Quickstart")
        print("=" * 60)
        print()
        print("1. Scan a skill:")
        print("   python skillgate.py scan ./my-skill/")
        print()
        print("2. Get AI-friendly output:")
        print("   python skillgate.py scan ./my-skill/ --format agent")
        print()
        print("3. CI integration:")
        print("   python skillgate.py scan ./my-skill/ --fail-under 80")
        print()
        print("4. Generate badge for your README:")
        print("   python skillgate.py scan ./my-skill/ --badge badge.svg")
        print()
        print("5. Save report to file:")
        print("   python skillgate.py scan ./my-skill/ --format json --output report.json")
        print()
        print("📚 Full docs: https://github.com/your-org/skillgate")
        print("=" * 60)
        sys.exit(0)

    if args.command == "scan":
        # Batch mode: scan all subdirectories
        if args.batch:
            base_path = Path(args.skill_dir).resolve()
            if not base_path.is_dir():
                print(f"错误: 目录不存在 - {args.skill_dir}", file=sys.stderr)
                sys.exit(2)

            all_results = []
            skill_dirs = [d for d in base_path.iterdir() if d.is_dir()]
            print(f"批量扫描: 发现 {len(skill_dirs)} 个子目录")

            for d in skill_dirs:
                try:
                    r = scan_skill(str(d))
                    all_results.append(r)
                    status = "✅" if r.critical_count == 0 and r.high_count == 0 else "❌"
                    print(f"  {status} {r.skill_name}: {r.trust_score}/100 ({r.grade})")
                except Exception as e:
                    print(f"  ⚠️  {d.name}: 扫描失败 - {e}")

            # Summary
            print(f"\n{'='*60}")
            print(f"  批量扫描汇总")
            print(f"{'='*60}")
            print(f"  总计: {len(all_results)} 个 skill")
            avg_score = sum(r.trust_score for r in all_results) / len(all_results) if all_results else 0
            print(f"  平均 Trust Score: {avg_score:.1f}/100")
            passed = len([r for r in all_results if r.critical_count == 0 and r.high_count == 0])
            print(f"  通过: {passed}/{len(all_results)}")

            # Exit code
            if passed < len(all_results):
                sys.exit(1)
            else:
                sys.exit(0)

        result = scan_skill(args.skill_dir)

        # Lenient mode: downgrade all findings by one level
        if args.lenient:
            severity_downgrade = {
                "CRITICAL": "HIGH",
                "HIGH": "MEDIUM",
                "MEDIUM": "LOW",
                "LOW": "INFO",
                "INFO": "INFO",
            }
            for f in result.findings:
                f.severity = severity_downgrade.get(f.severity, f.severity)
            print("  (宽松模式：所有规则降一级别)")

        # 自动记录到审计日志（有籍）
        try:
            from audit_log import record_scan
            record_scan(result, args.skill_dir)
        except Exception:
            pass  # 审计日志失败不影响主流程

        # Generate badge if requested
        if args.badge:
            badge_svg = generate_badge(result)
            Path(args.badge).write_text(badge_svg, encoding="utf-8")
            print(f"Badge 已生成: {args.badge}")

        if args.format == "agent":
            output = generate_agent_summary(result)
            if args.output:
                Path(args.output).write_text(output, encoding="utf-8")
                print(f"Agent summary written to: {args.output}")
            else:
                print(output)
            # Exit code for CI usage
            if result.critical_count > 0 or result.high_count > 0:
                sys.exit(1)
        elif args.format == "sarif":
            output = generate_sarif(result)
            if args.output:
                Path(args.output).write_text(output, encoding="utf-8")
                print(f"SARIF 报告已写入: {args.output}")
            else:
                print(output)
        elif args.format == "junit":
            output = generate_junit_xml(result)
            if args.output:
                Path(args.output).write_text(output, encoding="utf-8")
                print(f"JUnit XML 报告已写入: {args.output}")
            else:
                print(output)
        elif args.format == "json":
            output = json.dumps(asdict(result), indent=2, ensure_ascii=False)
            if args.output:
                Path(args.output).write_text(output, encoding="utf-8")
                print(f"JSON 报告已写入: {args.output}")
            else:
                print(output)
        elif args.format == "markdown":
            lines = [
                f"# SkillGate 扫描报告",
                f"",
                f"- **Skill**: {result.skill_name}",
                f"- **Trust Score**: {result.trust_score}/100 ({result.grade})",
                f"- **扫描文件数**: {result.files_scanned}",
                f"",
                f"## Findings",
                f"",
            ]
            if result.findings:
                for f in result.findings:
                    lines.append(f"- [{f.severity}] {f.category}: {f.message} (`{f.file}:{f.line}`)")
            else:
                lines.append("✅ 无发现")
            output = "\n".join(lines)
            if args.output:
                Path(args.output).write_text(output, encoding="utf-8")
                print(f"Markdown 报告已写入: {args.output}")
            else:
                print(output)
        else:
            exit_code = print_terminal_report(result, fail_under=args.fail_under)
            sys.exit(exit_code)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
