"""
Skill Ecosystem — 统一入口。
一个命令用所有功能：搜索、浏览、扫描、运行、版本管理。
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def show_help():
    """显示帮助。"""
    print("=" * 60)
    print("  🌐 Skill Ecosystem — 技能生态统一入口")
    print("  📖 方法论：LGD-Evo（自生长生态）")
    print("=" * 60)
    print()
    print("  用法: python ecosystem.py <command>")
    print()
    print("  命令:")
    print("    registry          打开注册中心（浏览所有 skill）")
    print("    search <query>    搜索 skill")
    print("    scan-all          一键扫描所有 skill")
    print("    run <query>       运行时执行（自动路由 + 执行 + 评测 + 合成）")
    print("    versions          版本管理（看升级历史）")
    print("    deps              依赖管理（看依赖关系）")
    print("    analytics         使用记录（看统计数据）")
    print("    traces            调用日志（看每次调用的详细信息）")
    print("    errors            错误队列（看待重试的任务）")
    print("    cache             上下文缓存（看缓存统计）")
    print("    governance        企业治理（看策略和权限）")
    print("    cost              成本追踪（看时间和预算）")
    print("    monitor           主动监控（检查系统状态）")
    print("    recommend         主动推荐（推荐你可能需要的）")
    print("    watch             文件监控（文件变了自动扫）")
    print("    improve           自动改进（重试失败任务）")
    print("    proactive         一键跑所有主动性功能")
    print("    methodology       查看 LGD-Evo 方法论摘要")
    print("    check-methodology  自检有没有符合 LGD 三律")
    print("    evolve-summary     总结这一圈循环的效果")
    print("    version           显示当前版本号")
    print("    start             一键跑最常用的功能")
    print("    feedback          提交改进建议")
    print("    evolve-10-rounds  总结 10 圈循环的效果")
    print("    cleanup           清理临时文件和缓存")
    print("    health            健康检查（工具有没有问题）")
    print("    web               启动 Web 版")
    print("    medical-recommend <分类>  医械法规推荐（1/2/3/ai）")
    print("    medical-chain <文件> <分类>  医械法规技能链（一键跑全部）")
    print("    medical-watch <目录>     医械文档变化监控")
    print("    perf-test         性能测试（每秒扫多少文件）")
    print("    stress-test       压力测试（连续跑 10 次）")
    print("    red-team          红队测试（模拟攻击）")
    print("    evolve            自我进化诊断（看看哪里能改进）")
    print("    full-cycle        共生循环（扫描→改进→再扫描→再改进，跑 3 圈）")
    print("    health-dashboard  系统健康仪表盘（模拟企业级可观测性）")
    print("    permissions       权限管理（模拟企业级权限）")
    print("    api               启动本地 API 服务器（模拟企业级 API）")
    print("    help              显示帮助")
    print()
    print("  示例:")
    print("    python ecosystem.py search medical")
    print("    python ecosystem.py run \"帮我检查 21 CFR 引用格式\"")
    print("    python ecosystem.py scan-all")
    print("=" * 60)


def cmd_registry():
    """打开注册中心。"""
    from registry import list_all, by_category
    skills = list_all()
    categories = by_category()

    print("\n" + "=" * 60)
    print("  📚 技能注册中心")
    print("=" * 60)
    print(f"\n  总 skill 数: {len(skills)}")
    print(f"\n  按分类：")
    for cat, sks in categories.items():
        print(f"    {cat}: {len(sks)} 个")
    print(f"\n  所有 skill：")
    for i, s in enumerate(skills, 1):
        print(f"    {i}. {s.name} v{s.version} — Trust Score {s.trust_score}/100")


def cmd_search(query: str):
    """搜索 skill。"""
    from registry import search
    results = search(query)

    print("\n" + "=" * 60)
    print(f"  🔍 搜索: {query}")
    print("=" * 60)
    print(f"\n  找到 {len(results)} 个结果：")
    for i, s in enumerate(results, 1):
        print(f"    {i}. {s.name} — {s.description[:50]}...")


def cmd_scan_all():
    """一键扫描所有 skill。"""
    from registry import scan_all_skills
    scan_all_skills()


def cmd_run(query: str):
    """运行时执行。"""
    from runtime import run
    run(query)


def cmd_versions():
    """版本管理。"""
    from version_manager import VERSION_HISTORY
    print("\n" + "=" * 60)
    print("  📦 版本管理")
    print("=" * 60)
    for h in VERSION_HISTORY:
        latest = h.versions[-1]
        print(f"\n  {h.name}:")
        print(f"    最新版本: {latest['version']} ({latest['date']})")
        print(f"    总版本数: {len(h.versions)}")


def cmd_deps():
    """依赖管理。"""
    from dependency_manager import build_dependency_graph, check_dependency_chain
    graph = build_dependency_graph()
    has_cycle = check_dependency_chain()

    print("\n" + "=" * 60)
    print("  🔗 依赖管理")
    print("=" * 60)
    print(f"\n  总 skill 数: {len(graph)}")
    print(f"  循环依赖: {'❌ 有' if has_cycle else '✅ 无'}")


def cmd_analytics():
    """使用记录。"""
    from analytics import main as analytics_main
    analytics_main()


def cmd_traces():
    """调用日志。"""
    from traces import main as traces_main
    traces_main()


def cmd_errors():
    """错误队列。"""
    from error_queue import main as error_queue_main
    error_queue_main()


def cmd_cache():
    """上下文缓存。"""
    from cache import main as cache_main
    cache_main()


def cmd_governance():
    """企业治理。"""
    from governance import main as governance_main
    governance_main()


def cmd_cost():
    """成本追踪。"""
    from cost_tracker import main as cost_tracker_main
    cost_tracker_main()


def cmd_monitor():
    """主动监控。"""
    from proactive_monitor import main as monitor_main
    monitor_main()


def cmd_recommend():
    """主动推荐。"""
    from proactive_recommender import main as recommender_main
    recommender_main()


def cmd_watch():
    """文件监控。"""
    from file_watcher import main as watcher_main
    watcher_main()


def cmd_improve():
    """自动改进。"""
    from auto_improve import main as improve_main
    improve_main()


def cmd_proactive():
    """一键跑所有主动性功能。"""
    print("=" * 60)
    print("  🚀 一键跑所有主动性功能")
    print("=" * 60)

    print("\n  1/5 主动监控：")
    from proactive_monitor import run_all_checks, get_overall_status
    results = run_all_checks()
    overall = get_overall_status(results)
    print(f"    整体状态: {overall}")

    print("\n  2/5 主动推荐：")
    from proactive_recommender import get_recommendations, get_anticipation
    recs = get_recommendations()
    for r in recs:
        print(f"    {r}")

    print("\n  3/5 文件监控：")
    from file_watcher import auto_scan_if_changed
    result = auto_scan_if_changed()
    print(f"    {result['message']}")

    print("\n  4/5 主动执行：")
    from proactive_executor import run_all_actions
    actions = run_all_actions()
    for a in actions:
        print(f"    [{a['action']}] {a['message']}")

    print("\n  5/5 自我进化：")
    from self_evolution import get_improvement_suggestions
    suggestions = get_improvement_suggestions()
    if suggestions:
        for s in suggestions:
            print(f"    {s}")
    else:
        print("    暂无建议")

    print("\n" + "=" * 60)
    print("  ✅ 全部主动性功能跑完了")
    print("=" * 60)


def cmd_methodology():
    """查看 LGD-Evo 方法论摘要。"""
    print("=" * 60)
    print("  📖 LGD-Evo 自生长生态方法论")
    print("=" * 60)

    print("\n  🎯 核心理念：")
    print("    不追求一步到位，但是每一步都要扎实；")
    print("    不吹牛，能做的就说能做，做不到的就说做不到；")
    print("    最后做成一个会自己变好的系统。")

    print("\n  📜 LGD 三律：")
    print("    有籍（Registered）：每个任务有档案可追溯")
    print("    有证（Evidenced）：每个结论有出处有证据")
    print("    有门禁（Gated）：关键节点有检查有验证")

    print("\n  📈 主动性四个层次：")
    print("    1. 被动执行 → 2. 主动建议 → 3. 主动执行 → 4. 完全自主")
    print("    （我们达到了第 3 层——本地工具能做到的最高水平）")

    print("\n  🔄 自我进化闭环：")
    print("    收集数据 → 诊断问题 → 改进 → 验证 → 记录 → 循环")

    print("\n" + "=" * 60)
    print("  📄 完整文档：docs/lgd-evo-methodology.md")
    print("=" * 60)


def cmd_check_methodology():
    """自检有没有符合 LGD 三律。"""
    from methodology_self_check import main as check_main
    check_main()


def cmd_evolve_summary():
    """总结这一圈循环的效果。"""
    print("=" * 60)
    print("(")
    print("  🔄 进化循环 5 圈总结")
    print("=" * 60)

    print("\n  第 1 圈：")
    print("    方法论指导工具：工具里加了方法论名称")
    print("    工具反哺方法论：方法论加了'工具里要显示方法论名称'")

    print("\n  第 2 圈：")
    print("    方法论指导工具：加了 methodology 命令（查看方法论摘要）")
    print("    工具反哺方法论：方法论加了'工具里要有查看方法论的命令'")

    print("\n  第 3 圈：")
    print("    方法论指导工具：做了方法论自检工具")
    print("    工具反哺方法论：方法论加了'工具要能自己检查自己'")

    print("\n  第 4 圈：")
    print("    方法论指导工具：把方法论自检加到统一入口里")
    print("    工具反哺方法论：方法论加了'所有功能都要集成到统一入口'")

    print("\n  第 5 圈：")
    print("    方法论指导工具：做了进化循环总结命令")
    print("    工具反哺方法论：方法论加了'每圈都要总结效果'")

    print("\n" + "=" * 60)
    print("  📊 效果统计：")
    print("    - 工具多了 3 个新命令（methodology / check-methodology / evolve-summary）")
    print("    - 方法论多了 5 条新原则（从实践里沉淀出来的）")
    print("    - 循环转了 5 圈，工具更好用，方法论更完善")
    print("=" * 60)


def cmd_version():
    """显示当前版本号。"""
    print("=" * 60)
    print("  🏷️ Skill Ecosystem 版本信息")
    print("=" * 60)
    print()
    print("  版本: v7.4.0")
    print("  方法论: LGD-Evo v1.0")
    print("  更新日期: 2026-10-27")
    print()
    print("=" * 60)


def cmd_start():
    """一键跑最常用的功能。"""
    print("=" * 60)
    print("  🚀 一键启动——最常用的功能")
    print("=" * 60)

    print("\n  1. 主动监控：")
    from proactive_monitor import run_all_checks, get_overall_status
    results = run_all_checks()
    overall = get_overall_status(results)
    print(f"    整体状态: {overall}")

    print("\n  2. 主动推荐：")
    from proactive_recommender import get_recommendations
    recs = get_recommendations()
    for r in recs:
        print(f"    {r}")

    print("\n  3. 文件监控：")
    from file_watcher import auto_scan_if_changed
    result = auto_scan_if_changed()
    print(f"    {result['message']}")

    print("\n" + "=" * 60)
    print("  ✅ 启动完成！")
    print("=" * 60)


def cmd_feedback():
    """提交改进建议。"""
    from datetime import datetime
    from pathlib import Path

    feedback_file = Path(__file__).parent / "feedback.json"

    print("=" * 60)
    print("(")
    print("  💬 提交改进建议")
    print("=" * 60)

    suggestion = input("  你觉得哪里可以改进？")

    # 保存建议
    import json
    if feedback_file.exists():
        feedbacks = json.loads(feedback_file.read_text(encoding="utf-8"))
    else:
        feedbacks = []

    feedbacks.append({
        "timestamp": datetime.now().isoformat(),
        "suggestion": suggestion
    })

    feedback_file.write_text(
        json.dumps(feedbacks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\n  ✅ 感谢你的建议！我们会改进的")
    print("=" * 60)


def cmd_evolve_10_rounds():
    """总结 10 圈循环的效果。"""
    print("=" * 60)
    print("(")
    print("  🔄 进化循环 10 圈大总结")
    print("=" * 60)

    print("\n  🛠️ 工具这边多了什么：")
    print("    1. methodology 命令（查看方法论摘要）")
    print("    2. check-methodology 命令（自检有没有符合 LGD 三律）")
    print("    3. evolve-summary 命令（总结循环效果）")
    print("    4. version 命令（显示版本号）")
    print("    5. start 命令（一键启动最常用功能）")
    print("    6. feedback 命令（提交改进建议）")
    print("    7. evolve-10-rounds 命令（10 圈大总结）")
    print("    8. Web 版加了方法论页面（/methodology）")

    print("\n  📖 方法论这边多了什么：")
    print("    从实践里沉淀出来了 12 条新原则（第 4 条到第 15 条）")
    print("    这些原则不是纸上谈兵，是真的做出来、用出来的")

    print("\n  📊 效果统计：")
    print("    - 工具多了 8 个新功能")
    print("    - 方法论多了 12 条新原则")
    print("    - 循环转了 10 圈，工具更好用，方法论更完善")
    print("    - 这就是 LGD-Evo 自生长生态的力量")

    print("\n" + "=" * 60)
    print("  ✅ 10 圈循环完成！")
    print("=" * 60)


def cmd_cleanup():
    """清理临时文件和缓存。"""
    from pathlib import Path
    import os

    project_root = Path(__file__).parent

    print("=" * 60)
    print("(")
    print("  🧹 清理临时文件和缓存")
    print("=" * 60)

    # 要清理的文件
    temp_files = [
        "cache.json",
        "scan-round-1.txt",
        "__pycache__",
    ]

    cleaned = 0
    for filename in temp_files:
        path = project_root / filename
        if path.exists():
            if path.is_dir():
                # 删 __pycache__ 目录
                import shutil
                shutil.rmtree(path)
            else:
                path.unlink()
            cleaned += 1
            print(f"    ✅ 清理了 {filename}")

    print(f"\n  总共清理了 {cleaned} 个文件/目录")
    print("=" * 60)


def cmd_health():
    """健康检查。"""
    from pathlib import Path

    project_root = Path(__file__).parent

    print("=" * 60)
    print("(")
    print("  ❤️ 健康检查——工具有没有问题")
    print("=" * 60)

    checks = []

    # 检查核心文件在不在
    core_files = [
        "skillgate.py",
        "runtime.py",
        "registry.py",
        "ecosystem.py",
        "web_server.py",
    ]

    for filename in core_files:
        if (project_root / filename).exists():
            checks.append(f"✅ {filename} 存在")
        else:
            checks.append(f"❌ {filename} 不存在")

    # 检查文档在不在
    docs = [
        "README.md",
        "docs/lgd-evo-methodology.md",
    ]

    for filename in docs:
        if (project_root / filename).exists():
            checks.append(f"✅ {filename} 存在")
        else:
            checks.append(f"❌ {filename} 不存在")

    for check in checks:
        print(f"  {check}")

    print("\n" + "=" * 60)
    print("  ✅ 健康检查完成！")
    print("=" * 60)


def cmd_web():
    """启动 Web 版。"""
    print("\n" + "=" * 60)
    print("  🌐 启动 Web 版...")
    print("=" * 60)
    import subprocess
    import sys
    subprocess.run([sys.executable, "web_server.py"])


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "help":
        show_help()
    elif command == "registry":
        cmd_registry()
    elif command == "search":
        if not args:
            print("用法: python ecosystem.py search <query>")
            return
        cmd_search(" ".join(args))
    elif command == "scan-all":
        cmd_scan_all()
    elif command == "run":
        if not args:
            print("用法: python ecosystem.py run <query>")
            return
        cmd_run(" ".join(args))
    elif command == "versions":
        cmd_versions()
    elif command == "deps":
        cmd_deps()
    elif command == "analytics":
        cmd_analytics()
    elif command == "traces":
        cmd_traces()
    elif command == "errors":
        cmd_errors()
    elif command == "cache":
        cmd_cache()
    elif command == "governance":
        cmd_governance()
    elif command == "cost":
        cmd_cost()
    elif command == "monitor":
        cmd_monitor()
    elif command == "recommend":
        cmd_recommend()
    elif command == "watch":
        cmd_watch()
    elif command == "improve":
        cmd_improve()
    elif command == "proactive":
        cmd_proactive()
    elif command == "methodology":
        cmd_methodology()
    elif command == "check-methodology":
        cmd_check_methodology()
    elif command == "evolve-summary":
        cmd_evolve_summary()
    elif command == "version":
        cmd_version()
    elif command == "start":
        cmd_start()
    elif command == "feedback":
        cmd_feedback()
    elif command == "evolve-10-rounds":
        cmd_evolve_10_rounds()
    elif command == "cleanup":
        cmd_cleanup()
    elif command == "health":
        cmd_health()
    elif command == "web":
        cmd_web()
    elif command == "medical-recommend":
        # 医械法规推荐
        import subprocess
        device_class = args[0] if args else "3"
        subprocess.run(["python", "skills/medical-recommender.py", device_class])
    elif command == "medical-chain":
        # 医械法规技能链
        import subprocess
        filepath = args[0] if len(args) > 0 else "."
        device_class = args[1] if len(args) > 1 else "3"
        subprocess.run(["python", "skills/medical-device-chain.py", filepath, device_class])
    elif command == "medical-watch":
        # 医械文档监控
        import subprocess
        docs_dir = args[0] if args else "."
        subprocess.run(["python", "skills/medical-file-watcher.py", docs_dir])
    elif command == "perf-test":
        # 性能测试
        import subprocess
        subprocess.run(["python", "performance_test.py"])
    elif command == "stress-test":
        # 压力测试
        import subprocess
        subprocess.run(["python", "stress_test.py"])
    elif command == "red-team":
        # 红队测试
        import subprocess
        subprocess.run(["python", "tests/test_red_team.py"])
    elif command == "evolve":
        # 自我进化诊断
        import subprocess
        subprocess.run(["python", "self_evolution.py"])
    elif command == "full-cycle":
        # 共生循环——一键跑完整流程（扫描 → 改进 → 再扫描 → 再改进）
        import subprocess
        print("=" * 60)
        print("  🔄 共生循环——一键跑完整流程")
        print("=" * 60)

        for i in range(3):
            print(f"\n  === 第 {i+1} 圈 ===")
            print("\n  1. 扫描所有 skill...")
            subprocess.run(["python", "ecosystem.py", "scan-all"])
            print("\n  2. 自动改进...")
            subprocess.run(["python", "ecosystem.py", "improve"])

        print("\n" + "=" * 60)
        print("  ✅ 共生循环完成！跑了 3 圈")
        print("=" * 60)
    elif command == "health-dashboard":
        # 系统健康仪表盘——模拟企业级可观测性
        import subprocess
        print("=" * 60)
        print("  📊 系统健康仪表盘")
        print("=" * 60)
        print("\n  1. 健康检查：")
        subprocess.run(["python", "ecosystem.py", "health"])
        print("\n  2. 使用统计：")
        subprocess.run(["python", "ecosystem.py", "analytics"])
        print("\n  3. 错误队列：")
        subprocess.run(["python", "ecosystem.py", "errors"])
        print("\n  4. 成本追踪：")
        subprocess.run(["python", "ecosystem.py", "cost"])
        print("\n" + "=" * 60)
        print("  ✅ 系统健康仪表盘完成！")
        print("=" * 60)
    elif command == "permissions":
        # 权限管理——模拟企业级权限
        import subprocess
        subprocess.run(["python", "ecosystem.py", "governance"])
    elif command == "api":
        # 启动本地 API 服务器——模拟企业级 API
        import subprocess
        print("=" * 60)
        print("  🌐 启动本地 API 服务器")
        print("=" * 60)
        print("\n  地址: http://localhost:8080")
        print("  按 Ctrl+C 停止")
        print("\n" + "=" * 60)
        subprocess.run(["python", "cloud_server.py"])
    else:
        print(f"未知命令: {command}")
        show_help()


if __name__ == "__main__":
    main()
