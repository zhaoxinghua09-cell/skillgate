"""
SkillGate 压力测试。
测试极限情况：大项目、多文件、复杂代码、内存占用。
"""
import time
import tracemalloc
from pathlib import Path
import sys
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent))


def create_large_test_project(num_files: int = 100, lines_per_file: int = 100):
    """创建一个大的测试项目。"""
    tmpdir = tempfile.mkdtemp(prefix="skillgate-pressure-")
    project = Path(tmpdir)

    # 创建一些危险代码样本
    dangerous_code = '''
import os
import subprocess

def dangerous_function(user_input):
    eval(user_input)
    os.system(f"echo {user_input}")
    subprocess.run(f"ls {user_input}", shell=True)
    return pickle.loads(user_input)
'''

    # 创建一些正常代码样本
    normal_code = '''
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, x):
        self.result += x
        return self.result
'''

    for i in range(num_files):
        filename = project / f"module_{i:03d}.py"
        if i % 5 == 0:
            filename.write_text(dangerous_code)
        else:
            filename.write_text(normal_code)

    return project


def pressure_test_large_project():
    """压力测试：扫描大项目。"""
    print("=" * 60)
    print("  🔥 压力测试：大项目扫描")
    print("=" * 60)

    from skillgate import scan_skill

    # 测试不同大小
    for num_files in [10, 50, 100]:
        print(f"\n  📊 测试 {num_files} 个文件...")
        project = create_large_test_project(num_files=num_files)

        tracemalloc.start()
        start = time.time()
        result = scan_skill(str(project))
        elapsed = time.time() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"    扫描耗时: {elapsed:.2f} 秒")
        print(f"    文件数量: {result.files_scanned}")
        print(f"    发现问题: {len(result.findings)}")
        print(f"    内存峰值: {peak / 1024 / 1024:.1f} MB")

        # 清理
        shutil.rmtree(project)


def pressure_test_deep_nesting():
    """压力测试：深层嵌套目录。"""
    print("\n" + "=" * 60)
    print("  🔥 压力测试：深层嵌套目录")
    print("=" * 60)

    from skillgate import scan_skill

    tmpdir = tempfile.mkdtemp(prefix="skillgate-deep-")
    deep = Path(tmpdir)
    for i in range(10):
        deep = deep / f"level_{i}"
        deep.mkdir()
        (deep / "test.py").write_text("import os\nos.system('ls')\n")

    start = time.time()
    result = scan_skill(tmpdir)
    elapsed = time.time() - start

    print(f"    嵌套深度: 10 层")
    print(f"    扫描耗时: {elapsed:.2f} 秒")
    print(f"    发现问题: {len(result.findings)}")

    shutil.rmtree(tmpdir)


def main():
    print("\n" + "=" * 60)
    print("  🧪 SkillGate 压力测试")
    print("=" * 60)

    pressure_test_large_project()
    pressure_test_deep_nesting()

    print("\n" + "=" * 60)
    print("  ✅ 压力测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
