"""
SkillGate Parallel Scanner — 并行扫描多个文件，提升性能。
"""
import concurrent.futures
from pathlib import Path
from typing import List


def scan_files_parallel(filepaths: List[Path], scan_fn, max_workers: int = 4) -> list:
    """Scan multiple files in parallel."""
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(scan_fn, f): f for f in filepaths}

        for future in concurrent.futures.as_completed(future_to_file):
            filepath = future_to_file[future]
            try:
                result = future.result()
                if result:
                    results.extend(result)
            except Exception as e:
                print(f"Error scanning {filepath}: {e}")

    return results


def get_all_files_to_scan(skill_path: Path) -> List[Path]:
    """Get all files that should be scanned."""
    files = []

    # Python files
    files.extend(skill_path.rglob("*.py"))

    # JS/TS files
    files.extend(skill_path.rglob("*.js"))
    files.extend(skill_path.rglob("*.ts"))

    # Shell files
    files.extend(skill_path.rglob("*.sh"))

    # Markdown files
    files.extend(skill_path.rglob("*.md"))

    # Go files
    files.extend(skill_path.rglob("*.go"))

    # Rust files
    files.extend(skill_path.rglob("*.rs"))

    # Java files
    files.extend(skill_path.rglob("*.java"))

    # PHP files
    files.extend(skill_path.rglob("*.php"))

    # Dockerfile
    if (skill_path / "Dockerfile").exists():
        files.append(skill_path / "Dockerfile")

    # Filter out cache and build directories
    filtered = []
    for f in files:
        if ".git" in str(f):
            continue
        if "__pycache__" in str(f):
            continue
        if "node_modules" in str(f):
            continue
        if "dist" in str(f) and "dist-info" not in str(f):
            continue
        filtered.append(f)

    return filtered


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parallel_scan.py <skill_dir>")
        sys.exit(1)

    files = get_all_files_to_scan(Path(sys.argv[1]))
    print(f"Found {len(files)} files to scan")
