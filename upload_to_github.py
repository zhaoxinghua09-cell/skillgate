#!/usr/bin/env python3
"""
批量上传本地文件到 GitHub 仓库——不用 git，直接用 GitHub API。
"""
import os
import base64
import requests
import subprocess
from pathlib import Path

# 配置
REPO_OWNER = "zhaoxinghua09-cell"
REPO_NAME = "skillgate"
BRANCH = "main"
LOCAL_DIR = Path(".")

# 获取 token
def get_token():
    result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
    return result.stdout.strip()

# 上传单个文件
def upload_file(token, file_path):
    # 相对路径
    rel_path = str(file_path.relative_to(LOCAL_DIR)).replace("\\", "/")
    
    # 读取文件内容
    with open(file_path, "rb") as f:
        content = f.read()
    
    # base64 编码
    content_b64 = base64.b64encode(content).decode()
    
    # API 请求
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{rel_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"Upload {rel_path}",
        "content": content_b64,
        "branch": BRANCH
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"✅ Uploaded: {rel_path}")
        return True
    else:
        print(f"❌ Failed: {rel_path} - {response.status_code} - {response.text}")
        return False

# 主函数
def main():
    token = get_token()
    print(f"Token: {token[:10]}...")
    
    # 遍历所有文件
    files = []
    for root, dirs, filenames in os.walk(LOCAL_DIR):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in ["__pycache__", ".git", "node_modules", ".vscode"]]
        
        for filename in filenames:
            file_path = Path(root) / filename
            rel_path = file_path.relative_to(LOCAL_DIR)
            
            # 排除文件
            if any(part.startswith(".") and part != ".gitignore" for part in rel_path.parts):
                continue
            if file_path.suffix in [".pyc", ".pyo", ".log", ".tmp"]:
                continue
            
            files.append(file_path)
    
    print(f"Total files to upload: {len(files)}")
    
    # 上传
    success = 0
    failed = 0
    for i, file_path in enumerate(files):
        print(f"\n[{i+1}/{len(files)}] ", end="")
        if upload_file(token, file_path):
            success += 1
        else:
            failed += 1
    
    print(f"\n\n=== Done ===")
    print(f"Success: {success}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    main()
