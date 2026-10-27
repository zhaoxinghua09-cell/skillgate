"""
SkillGate HTML Report Generator — 生成完整的 HTML 扫描报告。
"""
from pathlib import Path


def generate_html_report(result) -> str:
    """Generate a complete HTML report from scan result."""
    score = result.trust_score
    grade = result.grade

    # Color based on score
    if score >= 90:
        score_color = "#238636"
        score_bg = "#0d1117"
    elif score >= 75:
        score_color = "#d29922"
        score_bg = "#0d1117"
    else:
        score_color = "#da3633"
        score_bg = "#0d1117"

    # Findings by severity
    critical = [f for f in result.findings if f.severity == "CRITICAL"]
    high = [f for f in result.findings if f.severity == "HIGH"]
    medium = [f for f in result.findings if f.severity == "MEDIUM"]
    low = [f for f in result.findings if f.severity == "LOW"]

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkillGate Report — {result.skill_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0d1117;
            color: #e6edf3;
            line-height: 1.6;
            padding: 40px 20px;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 1px solid #30363d;
        }}
        .score-circle {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: {score_color};
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 2.5rem;
            font-weight: bold;
            color: white;
        }}
        .skill-name {{ font-size: 1.5rem; margin-bottom: 10px; }}
        .grade {{ color: #8b949e; font-size: 1.1rem; }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}
        .stat-number {{ font-size: 1.5rem; font-weight: bold; }}
        .stat-label {{ color: #8b949e; font-size: 0.85rem; margin-top: 4px; }}

        .section {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .section-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #30363d;
        }}

        .finding-item {{
            padding: 12px;
            margin-bottom: 8px;
            border-left: 3px solid;
            background: #0d1117;
            border-radius: 0 6px 6px 0;
        }}
        .finding-critical {{ border-color: #f85149; }}
        .finding-high {{ border-color: #d29922; }}
        .finding-medium {{ border-color: #58a6ff; }}
        .finding-low {{ border-color: #8b949e; }}

        .finding-sev {{
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .finding-cat {{ color: #8b949e; font-size: 0.85rem; }}
        .finding-msg {{ margin: 4px 0; }}
        .finding-loc {{ color: #8b949e; font-size: 0.8rem; }}

        .footer {{
            text-align: center;
            color: #8b949e;
            font-size: 0.85rem;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #30363d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="score-circle">{score}</div>
            <div class="skill-name">{result.skill_name}</div>
            <div class="grade">Trust Score: {score}/100 · Grade: {grade}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" style="color: #f85149;">{len(critical)}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #d29922;">{len(high)}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #58a6ff;">{len(medium)}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #8b949e;">{len(low)}</div>
                <div class="stat-label">Low</div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📊 Scan Summary</div>
            <p><strong>Files scanned:</strong> {result.files_scanned}</p>
            <p><strong>Total findings:</strong> {len(result.findings)}</p>
            <p><strong>Skill directory:</strong> {result.skill_dir}</p>
        </div>

        {f'''
        <div class="section">
            <div class="section-title">🔴 Critical Findings ({len(critical)})</div>
            {"".join(f'''
            <div class="finding-item finding-critical">
                <div class="finding-sev" style="color: #f85149;">CRITICAL · {f.category}</div>
                <div class="finding-msg">{f.message}</div>
                <div class="finding-loc">{f.file}:{f.line or '?'}</div>
            </div>
            ''' for f in critical)}
        </div>
        ''' if critical else ''}

        {f'''
        <div class="section">
            <div class="section-title">🟠 High Findings ({len(high)})</div>
            {"".join(f'''
            <div class="finding-item finding-high">
                <div class="finding-sev" style="color: #d29922;">HIGH · {f.category}</div>
                <div class="finding-msg">{f.message}</div>
                <div class="finding-loc">{f.file}:{f.line or '?'}</div>
            </div>
            ''' for f in high)}
        </div>
        ''' if high else ''}

        {f'''
        <div class="section">
            <div class="section-title">🔵 Medium Findings ({len(medium)})</div>
            {"".join(f'''
            <div class="finding-item finding-medium">
                <div class="finding-sev" style="color: #58a6ff;">MEDIUM · {f.category}</div>
                <div class="finding-msg">{f.message}</div>
                <div class="finding-loc">{f.file}:{f.line or '?'}</div>
            </div>
            ''' for f in medium[:20])}
            {f'<p style="color: #8b949e; margin-top: 10px;">... and {len(medium) - 20} more</p>' if len(medium) > 20 else ''}
        </div>
        ''' if medium else ''}

        <div class="footer">
            <p>Generated by SkillGate v1.1.0</p>
            <p>Trust infrastructure for AI agent skills</p>
        </div>
    </div>
</body>
</html>'''

    return html


if __name__ == "__main__":
    print("HTML report generator module")
