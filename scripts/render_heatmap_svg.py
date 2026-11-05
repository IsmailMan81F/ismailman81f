import json
import os

def render_svg():
    input_file = "data/contributions.json"
    if not os.path.exists(input_file):
        days = []
        total = 0
    else:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            days = data.get("days", [])
            total = data.get("total", 0)

    PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

    box_size = 10
    gap = 3
    x_offset = 20
    y_offset = 20
    
    rects_xml = []
    for idx, day in enumerate(days):
        week = idx // 7
        dow = idx % 7
        x = x_offset + week * (box_size + gap)
        y = y_offset + dow * (box_size + gap)
        lvl = min(max(day.get("level", 0), 0), 5)
        color = PALETTE[lvl]
        delay = (week + dow) * 0.02
        rects_xml.append(
            f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}">'
            f'<animateTransform attributeName="transform" type="translate" from="0 -10" to="0 0" '
            f'dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>'
            f'</rect>'
        )

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="150" viewBox="0 0 860 150">
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: #8b949e; }}
    .bg {{ fill: #0d1117; rx: 6px; }}
  </style>
  <rect width="100%" height="100%" class="bg" />
  <g transform="translate(10, 10)">
    {"".join(rects_xml)}
  </g>
  <text x="30" y="135">{total:,} contributions in the last year</text>
</svg>'''

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Generated contrib-heatmap.svg successfully.")

if __name__ == "__main__":
    render_svg()
