---
name: dangerous-skill
description: A skill with lots of security issues.
---

# Dangerous Skill

This skill has all kinds of security problems.

```python
import os
import subprocess

API_KEY = "sk-1234567890abcdef"

def run_cmd(cmd):
    os.system(cmd)
    eval(cmd)
    subprocess.run(cmd, shell=True)
```
