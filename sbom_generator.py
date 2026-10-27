#!/usr/bin/env python3
"""
SBOM (Software Bill of Materials) generator for skills.
Generates SPDX-compatible SBOM.
"""

import json
from pathlib import Path
from datetime import datetime


def generate_sbom(skill_dir: str) -> str:
    """Generate SPDX SBOM for a skill directory."""
    skill_path = Path(skill_dir)

    # Collect dependencies
    dependencies = []

    # Check requirements.txt
    req_file = skill_path / "requirements.txt"
    if req_file.exists():
        for line in req_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                dependencies.append({
                    "name": line.split("==")[0].split(">=")[0].split("<=")[0].strip(),
                    "version": line,
                    "type": "pip",
                })

    # Check package.json
    pkg_file = skill_path / "package.json"
    if pkg_file.exists():
        try:
            pkg = json.loads(pkg_file.read_text(encoding="utf-8"))
            for dep in pkg.get("dependencies", {}).keys():
                dependencies.append({"name": dep, "version": pkg["dependencies"][dep], "type": "npm"})
        except:
            pass

    # Generate SPDX SBOM
    sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": skill_path.name,
        "documentNamespace": f"https://skillgate.dev/sbom/{skill_path.name}",
        "creationInfo": {
            "created": datetime.now().isoformat(),
            "creators": ["Tool: SkillGate-SBOM-Generator-1.0"],
        },
        "packages": [
            {
                "SPDXID": f"SPDXRef-Package-{i}",
                "name": dep["name"],
                "versionInfo": dep["version"],
                "supplier": "NOASSERTION",
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
            }
            for i, dep in enumerate(dependencies)
        ],
    }

    return json.dumps(sbom, indent=2)


def get_slsa_level(skill_dir: str) -> int:
    """Estimate SLSA supply chain level for a skill."""
    skill_path = Path(skill_dir)
    level = 0

    # Level 1: has source code
    if any(skill_path.glob("**/*.py")) or any(skill_path.glob("**/*.js")):
        level = max(level, 1)

    # Level 2: has build script / CI
    if (skill_path / "ci-templates").exists() or (skill_path / ".github").exists():
        level = max(level, 2)

    # Level 3: has provenance (SLSA attestation)
    if (skill_path / "attestation.json").exists():
        level = max(level, 3)

    return level


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python sbom_generator.py <skill_dir>")
        sys.exit(1)

    print(generate_sbom(sys.argv[1]))
    print(f"\nSLSA Level: {get_slsa_level(sys.argv[1])}")
