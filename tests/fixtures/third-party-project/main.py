"""一个模拟的开源项目，里面有各种常见问题（修复后）。"""
import os
import subprocess
import requests
import json

API_KEY = os.getenv("API_KEY", "")

def run_command(cmd_list):
    return subprocess.run(cmd_list, shell=False, capture_output=True)

def fetch_data(url):
    response = requests.get(url)
    return response.text

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def write_log(log_file, message):
    with open(log_file, 'a') as f:
        f.write(message + '\n')
