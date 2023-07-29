from typing import List

from svgwrite import Drawing


def create_svg_chart(
    data: List,
    width: int = 300,
    height: int = 100,
    line_color: str = "#1e3a8a",
    marker_color: str = "#1e3a8a",
):
    x_spacing = width // len(data)
    y_factor = height / max(max(data) + 50, 100)

    dwg = Drawing(size=(width, height))

    dwg.add(dwg.path(d=f"M0,0 V{height}", stroke="#374151", stroke_width=1))
    dwg.add(dwg.path(d=f"M0,{height} H{width}", stroke="#374151", stroke_width=1))

    path = dwg.path(stroke=line_color, stroke_width=2, fill="none")
    path.push(f"M0,{height - data[0] * y_factor} ")
    for x, y in enumerate(data[1:], 2):
        path.push(f"L{(x-1) * x_spacing},{height - y * y_factor} ")
    dwg.add(path)

    for x, y in enumerate(data):
        dwg.add(
            dwg.circle(
                center=(x * x_spacing, height - y * y_factor), r=6, fill=marker_color
            )
        )

    return dwg.tostring()
