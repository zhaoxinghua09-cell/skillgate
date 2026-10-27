"""Dangerous skill with real security issues."""
import os
import subprocess

API_KEY = "sk-1234567890abcdef"

def run_cmd(cmd):
    os.system(cmd)
    eval(cmd)
    subprocess.run(cmd, shell=True)
