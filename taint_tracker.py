"""
SkillGate Taint Tracker — 简化版污点追踪。
检测：用户输入 → 危险函数 的数据流。
"""
import ast
from pathlib import Path
from typing import List


# 污点源（用户输入）
TAINT_SOURCES = {
    "input",          # input()
    "sys.argv",       # 命令行参数
    "os.environ",     # 环境变量
    "request.args",   # Web 请求参数
    "request.form",
    "request.json",
}

# 污点汇（危险函数）
TAINT_SINKS = {
    "eval",
    "exec",
    "os.system",
    "subprocess.run",
    "subprocess.call",
    "subprocess.Popen",
    "pickle.load",
    "yaml.load",
}


class TaintTrackingVisitor(ast.NodeVisitor):
    """Track taint flow from sources to sinks."""

    def __init__(self):
        self.tainted_vars = set()
        self.findings = []

    def visit_Assign(self, node):
        # Check if right side is a taint source
        if isinstance(node.value, ast.Call):
            func_name = self._get_func_name(node.value.func)
            if func_name in TAINT_SOURCES:
                # This variable is now tainted
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.tainted_vars.add(target.id)

        self.generic_visit(node)

    def visit_Call(self, node):
        # Check if calling a dangerous sink with tainted input
        func_name = self._get_func_name(node.func)
        if func_name in TAINT_SINKS:
            # Check if any argument is tainted
            for arg in node.args:
                if isinstance(arg, ast.Name) and arg.id in self.tainted_vars:
                    self.findings.append({
                        "line": node.lineno,
                        "sink": func_name,
                        "tainted_var": arg.id,
                        "severity": "CRITICAL",
                        "message": f"污点传播: 用户输入 '{arg.id}' 直接传入危险函数 {func_name}()"
                    })

        self.generic_visit(node)

    def _get_func_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                return f"{node.value.id}.{node.attr}"
        return ""


def track_taint(filepath: Path) -> List[dict]:
    """Track taint flow in a Python file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(content, filename=str(filepath))
    except Exception:
        return []

    visitor = TaintTrackingVisitor()
    visitor.visit(tree)
    return visitor.findings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python taint_tracker.py <file.py>")
        sys.exit(1)

    findings = track_taint(Path(sys.argv[1]))
    for f in findings:
        print(f"[{f['severity']}] line {f['line']}: {f['message']}")
