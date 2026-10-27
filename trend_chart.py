"""
SkillGate Trend Chart Generator — 生成漂亮的 SVG Trust Score 趋势折线图。
"""


def generate_trend_chart(scores: list[float], labels: list[str]) -> str:
    """Generate a beautiful SVG line chart of Trust Score over time."""

    width = 600
    height = 200
    padding = 40

    # Calculate points
    if not scores:
        scores = [90]
        labels = ["Now"]

    min_score = min(scores) - 5
    max_score = max(scores) + 5
    min_score = max(0, min_score)
    max_score = min(100, max_score)

    x_step = (width - 2 * padding) / max(1, len(scores) - 1)
    y_range = max_score - min_score

    points = []
    for i, score in enumerate(scores):
        x = padding + i * x_step
        y = height - padding - ((score - min_score) / y_range) * (height - 2 * padding)
        points.append((x, y))

    # Build path
    path_d = f"M {points[0][0]} {points[0][1]}"
    for p in points[1:]:
        path_d += f" L {p[0]} {p[1]}"

    # Build SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
  <!-- Grid lines -->
  <line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="#333" stroke-width="1"/>
  <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" stroke="#333" stroke-width="1"/>

  <!-- Area fill -->
  <path d="{path_d} L {points[-1][0]} {height - padding} L {points[0][0]} {height - padding} Z" fill="#1f6feb22"/>

  <!-- Line -->
  <path d="{path_d}" fill="none" stroke="#1f6feb" stroke-width="2.5"/>

  <!-- Points -->
'''

    for i, (x, y) in enumerate(points):
        svg += f'  <circle cx="{x}" cy="{y}" r="4" fill="#1f6feb"/>\n'
        svg += f'  <text x="{x}" y="{height - padding + 15}" font-size="9" fill="#888" text-anchor="middle">{labels[i]}</text>\n'

    svg += f'</svg>'

    return svg


if __name__ == "__main__":
    scores = [75, 80, 82, 85, 90, 95]
    labels = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
    chart = generate_trend_chart(scores, labels)
    print(chart)
