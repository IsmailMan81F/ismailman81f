import sys
import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"  # Bright to dark

def image_to_ascii(image_path, width=100):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        img = np.full((100, 100), 200, dtype=np.uint8)
        cv2.circle(img, (50, 40), 25, 50, -1)
        cv2.circle(img, (50, 90), 40, 50, -1)

    aspect_ratio = img.shape[0] / img.shape[1]
    height = int(width * aspect_ratio * 0.55)
    resized = cv2.resize(img, (width, height))
    
    ascii_rows = []
    for y in range(height):
        row = []
        for x in range(width):
            val = resized[y, x]
            idx = int((val / 255.0) * (len(RAMP) - 1))
            row.append(RAMP[idx])
        ascii_rows.append("".join(row))
    return ascii_rows

def make_svg(ascii_rows, output_path="avi-ascii.svg"):
    row_height = 7.5
    total_height = len(ascii_rows) * row_height + 20
    total_width = len(ascii_rows[0]) * 3.6 + 20

    text_lines = []
    for i, line in enumerate(ascii_rows):
        y = 20 + i * row_height
        delay = i * 0.05
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        text_lines.append(
            f'<text x="10" y="{y:.1f}" class="ascii-row" style="animation-delay: {delay:.2f}s;">{escaped_line}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="370" height="370" viewBox="0 0 {total_width:.0f} {total_height:.0f}">
  <style>
    .bg {{ fill: #0d1117; rx: 8px; stroke: #30363d; stroke-width: 1px; }}
    .ascii-row {{
      font-family: 'Courier New', Courier, monospace;
      font-size: 6px;
      fill: #8b949e;
      white-space: pre;
      opacity: 0;
      animation: typeIn 0.05s forwards;
    }}
    @keyframes typeIn {{ to {{ opacity: 1; }} }}
  </style>
  <rect width="100%" height="100%" class="bg"/>
  <g>
    {"".join(text_lines)}
  </g>
</svg>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    rows = image_to_ascii("source-prepped.png")
    make_svg(rows)
