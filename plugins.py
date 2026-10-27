"""
SkillGate Plugin System — 让用户可以自定义规则。
"""
import importlib.util
from pathlib import Path
from typing import List, Callable


class Rule:
    """Custom rule definition."""
    def __init__(self, name: str, category: str, severity: str, check_fn: Callable):
        self.name = name
        self.category = category
        self.severity = severity
        self.check_fn = check_fn  # function(filepath: Path) -> list[Finding]


class PluginLoader:
    """Load custom rules from .skillgate/plugins/ directory."""

    def __init__(self, skill_dir: str):
        self.plugin_dir = Path(skill_dir) / ".skillgate" / "plugins"
        self.rules: List[Rule] = []

    def load(self):
        """Load all plugins from the plugins directory."""
        if not self.plugin_dir.exists():
            return

        for plugin_file in self.plugin_dir.glob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Look for register_rules function
                if hasattr(module, "register_rules"):
                    rules = module.register_rules()
                    self.rules.extend(rules)
                    print(f"Loaded plugin: {plugin_file.name} ({len(rules)} rules)")
            except Exception as e:
                print(f"Failed to load plugin {plugin_file.name}: {e}")

    def run(self, filepath: Path) -> list:
        """Run all loaded rules on a file."""
        findings = []
        for rule in self.rules:
            try:
                findings.extend(rule.check_fn(filepath))
            except Exception:
                pass
        return findings


# Example plugin template
EXAMPLE_PLUGIN = '''"""
Example SkillGate Plugin — 自定义规则示例。
放到 .skillgate/plugins/ 目录下即可自动加载。
"""
from pathlib import Path
from skillgate import Finding


def register_rules():
    """Return list of custom rules."""
    return [
        Rule(
            name="no-console-log",
            category="custom",
            severity="MEDIUM",
            check_fn=check_no_console_log
        )
    ]


def check_no_console_log(filepath: Path) -> list:
    """Check for console.log in JS files."""
    findings = []
    if filepath.suffix not in (".js", ".ts"):
        return findings

    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(content.splitlines(), 1):
            if "console.log(" in line:
                findings.append(Finding(
                    severity="LOW",
                    category="custom/console-log",
                    message="console.log 调试语句",
                    file=str(filepath),
                    line=i
                ))
    except Exception:
        pass

    return findings
'''


if __name__ == "__main__":
    # Save example plugin
    Path("example_plugin.py").write_text(EXAMPLE_PLUGIN, encoding="utf-8")
    print("Example plugin saved to example_plugin.py")
