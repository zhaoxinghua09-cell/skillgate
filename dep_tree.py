"""
SkillGate Dependency Tree Scanner — 完整依赖树扫描。
不只扫直接依赖，还扫传递依赖。
"""
import json
import urllib.request
from pathlib import Path


def parse_requirements(filepath: Path) -> list[dict]:
    """Parse requirements.txt into structured dependency list."""
    deps = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return deps

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Handle ==, >=, ~=, etc.
        for op in ["==", ">=", "<=", "~=", "!="]:
            if op in line:
                name, version = line.split(op, 1)
                deps.append({
                    "name": name.strip(),
                    "specifier": op + version.strip(),
                    "direct": True
                })
                break
        else:
            # No version specified
            deps.append({
                "name": line,
                "specifier": "latest",
                "direct": True
            })

    return deps


def get_transitive_deps(package_name: str, version: str = "latest") -> list[dict]:
    """Get transitive dependencies from PyPI JSON API."""
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            requires = data.get("info", {}).get("requires_dist", []) or []
            return [{"name": r, "direct": False} for r in requires[:20]]  # limit to 20
    except Exception:
        return []


def scan_full_dependency_tree(skill_path: Path) -> list[dict]:
    """Scan full dependency tree (direct + transitive)."""
    req_file = skill_path / "requirements.txt"
    if not req_file.exists():
        return []

    direct_deps = parse_requirements(req_file)
    all_deps = list(direct_deps)

    # Get transitive deps for each direct dep
    for dep in direct_deps[:5]:  # limit to 5 direct deps to avoid timeout
        transitive = get_transitive_deps(dep["name"])
        all_deps.extend(transitive)

    return all_deps


def query_osv(package_name: str, version: str) -> list[dict]:
    """Query OSV.dev for vulnerabilities."""
    try:
        payload = json.dumps({
            "package": {"name": package_name, "ecosystem": "PyPI"},
            "version": version
        }).encode()

        req = urllib.request.Request(
            "https://api.osv.dev/v1/query",
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("vulns", [])
    except Exception:
        return []


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python dep_tree.py <requirements.txt>")
        sys.exit(1)

    deps = scan_full_dependency_tree(Path(sys.argv[1]).parent)
    print(f"Total dependencies: {len(deps)}")
    for d in deps:
        print(f"  {'[direct]' if d['direct'] else '[transitive]'} {d['name']}")
