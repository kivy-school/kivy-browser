"""The shapes the widgets morph between, by index, as distances (stdlib `sdf`),
and the plate that outlines a widget."""
from pyshader import *
from pyshader.stdlib.fragment.sdf import (sd_circle, sd_star, sd_heart, sd_hexagon, sd_rounded_box,
                                          fill_smooth, stroke_smooth)

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


def within(uv: float2, resolution: float2) -> float2:
    """`centered`, the shapes shrunk to leave room for the plate."""
    return centered(uv, resolution) * 1.3


def bounds(uv: float2, resolution: float2) -> float:
    """Distance in pixels to the widget's rounded outline, negative inside."""
    return sd_rounded_box((uv - 0.5) * resolution, resolution * 0.5 - 3.0, float4(18.0))


def plate(uv: float2, resolution: float2, tint: float4, lit: float) -> float4:
    """The widget's outline over its whole size, brighter while `lit`."""
    d = bounds(uv, resolution)
    fill = fill_smooth(d, 1.0) * (0.1 + 0.14 * lit)
    line = stroke_smooth(d, 1.5 + 1.5 * lit, 0.75) * (0.75 + 0.25 * lit)
    return float4(tint.rgb, tint.a * max(fill, line))


def panel(uv: float2, resolution: float2, rgb: float3, tint: float4) -> float4:
    """`rgb` filling the widget's outline, the outline drawn over it."""
    d = bounds(uv, resolution)
    line = stroke_smooth(d, 1.5, 0.75) * 0.75
    return float4(mix(rgb, tint.rgb, line), tint.a * max(fill_smooth(d, 1.0), line))


def over(top: float4, under: float4) -> float4:
    a = top.a + under.a * (1.0 - top.a)
    return float4((top.rgb * top.a + under.rgb * under.a * (1.0 - top.a)) / max(a, 0.0001), a)
