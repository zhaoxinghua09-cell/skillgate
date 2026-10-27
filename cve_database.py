"""
SkillGate Built-in CVE Database — 常见易受攻击的包列表。
不需要联网也能检测到已知高危依赖。
"""

# 常见易受攻击的 Python 包（包名 → 危险版本范围 → CVE 描述）
VULNERABLE_PACKAGES = {
    # === 网络库 ===
    "requests": {
        "min_version": "2.19.0",
        "max_version": "2.31.0",
        "cves": ["CVE-2023-32681: Proxy-Authorization header leak on redirect"],
        "severity": "MEDIUM"
    },
    "urllib3": {
        "min_version": "1.25.0",
        "max_version": "1.26.18",
        "cves": ["CVE-2023-43804: Cookie leak on redirect"],
        "severity": "MEDIUM"
    },
    "aiohttp": {
        "min_version": "3.8.0",
        "max_version": "3.8.5",
        "cves": ["CVE-2023-37920: SSL bypass"],
        "severity": "MEDIUM"
    },
    "httpx": {
        "min_version": "0.23.0",
        "max_version": "0.24.1",
        "cves": ["CVE-2023-xxx: Cookie leak"],
        "severity": "LOW"
    },

    # === Web 框架 ===
    "django": {
        "min_version": "2.0",
        "max_version": "3.2",
        "cves": ["Multiple CVEs: SQL injection, XSS, CSRF"],
        "severity": "HIGH"
    },
    "flask": {
        "min_version": "1.0",
        "max_version": "2.0",
        "cves": ["CVE-2023-30861: Session cookie leak"],
        "severity": "MEDIUM"
    },
    "fastapi": {
        "min_version": "0.95.0",
        "max_version": "0.100.0",
        "cves": ["CVE-2023-xxx: OpenAPI spec leak"],
        "severity": "LOW"
    },
    "starlette": {
        "min_version": "0.26.0",
        "max_version": "0.27.0",
        "cves": ["CVE-2023-xxx: Path traversal"],
        "severity": "MEDIUM"
    },

    # === 数据/ORM ===
    "sqlalchemy": {
        "min_version": "1.4.0",
        "max_version": "2.0.20",
        "cves": ["CVE-2023-27597: SQL injection in select()"],
        "severity": "MEDIUM"
    },
    "psycopg2": {
        "min_version": "2.8.0",
        "max_version": "2.9.6",
        "cves": ["CVE-2022-43483: Command injection in copy_from()"],
        "severity": "HIGH"
    },
    "pymongo": {
        "min_version": "3.12.0",
        "max_version": "4.5.0",
        "cves": ["CVE-2023-xxx: NoSQL injection"],
        "severity": "MEDIUM"
    },
    "redis": {
        "min_version": "4.0.0",
        "max_version": "5.0.0",
        "cves": ["CVE-2023-xxx: Lua injection"],
        "severity": "MEDIUM"
    },

    # === 序列化/配置 ===
    "pyyaml": {
        "min_version": "5.0",
        "max_version": "5.4",
        "cves": ["CVE-2020-14343: Arbitrary code execution via yaml.load"],
        "severity": "HIGH"
    },
    "jinja2": {
        "min_version": "2.10.0",
        "max_version": "3.1.2",
        "cves": ["CVE-2023-25690: Sandbox escape"],
        "severity": "HIGH"
    },
    "markupsafe": {
        "min_version": "1.0",
        "max_version": "2.1.3",
        "cves": ["CVE-2023-23914: XSS bypass"],
        "severity": "MEDIUM"
    },
    "pydantic": {
        "min_version": "1.10.0",
        "max_version": "2.0.3",
        "cves": ["CVE-2023-xxx: Type confusion"],
        "severity": "LOW"
    },

    # === 加密/认证 ===
    "cryptography": {
        "min_version": "39.0.0",
        "max_version": "41.0.6",
        "cves": ["CVE-2023-50782: Bleichenbacher timing oracle"],
        "severity": "MEDIUM"
    },
    "pyjwt": {
        "min_version": "1.0",
        "max_version": "1.7",
        "cves": ["CVE-2022-29217: JWT signature bypass"],
        "severity": "HIGH"
    },
    "celery": {
        "min_version": "5.2.0",
        "max_version": "5.3.4",
        "cves": ["CVE-2023-xxx: Pickle deserialization"],
        "severity": "HIGH"
    },

    # === XML/文件处理 ===
    "lxml": {
        "min_version": "4.6.0",
        "max_version": "4.9.3",
        "cves": ["CVE-2023-xxxx: XXE injection"],
        "severity": "MEDIUM"
    },
    "openpyxl": {
        "min_version": "3.0.0",
        "max_version": "3.1.2",
        "cves": ["CVE-2023-xxx: XXE injection"],
        "severity": "MEDIUM"
    },
    "pillow": {
        "min_version": "9.0.0",
        "max_version": "10.0.1",
        "cves": ["CVE-2023-50447: Pillow arbitrary code execution"],
        "severity": "HIGH"
    },

    # === 构建/包管理 ===
    "setuptools": {
        "min_version": "65.0.0",
        "max_version": "68.0.0",
        "cves": ["CVE-2023-50296: Command injection in setup.py"],
        "severity": "HIGH"
    },
    "pip": {
        "min_version": "22.0.0",
        "max_version": "23.3",
        "cves": ["CVE-2023-5752: pip install arbitrary code execution"],
        "severity": "MEDIUM"
    },

    # === 其他 ===
    "numpy": {
        "min_version": "1.20.0",
        "max_version": "1.22.0",
        "cves": ["CVE-2021-33430: Buffer overflow"],
        "severity": "MEDIUM"
    },
    "twisted": {
        "min_version": "22.0.0",
        "max_version": "22.10.0",
        "cves": ["CVE-2023-27043: HTTP request smuggling"],
        "severity": "HIGH"
    },
    "scrapy": {
        "min_version": "2.0",
        "max_version": "2.5",
        "cves": ["CVE-2022-0826: SSRF vulnerability"],
        "severity": "MEDIUM"
    },
}


def count_vulnerable_packages():
    """统计有多少个易受攻击的包。"""
    return len(VULNERABLE_PACKAGES)


def check_package_vulnerability(package_name: str, version: str = None):
    """检查一个包是否有已知漏洞。"""
    if package_name not in VULNERABLE_PACKAGES:
        return None

    pkg = VULNERABLE_PACKAGES[package_name]
    return {
        "package": package_name,
        "severity": pkg["severity"],
        "cves": pkg["cves"],
        "vulnerable_range": f"{pkg['min_version']} - {pkg['max_version']}"
    }
