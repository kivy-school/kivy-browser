"""The shapes the widgets morph between, by index, as distances (stdlib `sdf`)."""
from pyshader import *
from pyshader.stdlib.fragment.sdf import sd_circle, sd_star, sd_heart, sd_hexagon, sd_rounded_box

COUNT = 5.0


def form(p: float2, index: float) -> float:
    if index < 0.5:
        return sd_circle(p, 0.32)
    if index < 1.5:
        return sd_star(p, 0.4, 5, 2.6)
    if index < 2.5:
        return sd_heart(p * 1.65 + float2(0.0, 0.5)) / 1.65
    if index < 3.5:
        return sd_hexagon(p, 0.3)
    return sd_rounded_box(p, float2(0.29), float4(0.08))


def centered(uv: float2, resolution: float2) -> float2:
    return (uv - 0.5) * resolution / min(resolution.x, resolution.y)
