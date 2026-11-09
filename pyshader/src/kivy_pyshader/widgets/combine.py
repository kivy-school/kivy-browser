"""Combine toggle

A circle and a box apart; down slides them together into one way of
combining them (`op`: union, smooth union, smooth subtract, smooth
intersect), up pulls them apart again. stdlib `sdf`.
"""
from pyshader import *
import pyshader.stdlib.fragment.sdf as sdf
from pyshader.stdlib.fragment.easing import cubic_in_out

from forms import centered


def combine(i: float, a: float, b: float) -> float:
    if i < 0.5:
        return sdf.op_union(a, b)
    if i < 1.5:
        return sdf.op_smooth_union(a, b, 0.15)
    if i < 2.5:
        return sdf.op_smooth_subtract(a, b, 0.05)
    return sdf.op_smooth_intersect(a, b, 0.05)


def main(uv: float2, resolution: float2, op: float, morph: float, tint: float4) -> float4:
    p = centered(uv, resolution)
    k = cubic_in_out(clamp(morph, 0.0, 1.0))
    gap = mix(0.3, 0.08, k)
    a = sdf.sd_circle(p - float2(gap, 0.0), 0.2)
    b = sdf.sd_box(p + float2(gap, 0.0), float2(0.15))
    d = mix(sdf.op_union(a, b), combine(op, a, b), k)
    body = sdf.fill_smooth(d, 0.004)
    lines = sdf.stroke_smooth(sdf.op_onion(d, 0.06), 0.008, 0.003)
    return float4(mix(tint.rgb, float3(1.0), lines), tint.a * max(body, lines))
