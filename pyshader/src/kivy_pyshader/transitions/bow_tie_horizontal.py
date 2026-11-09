"""Bow tie horizontal

gl-transitions, huynx, MIT.
"""
from pyshader import *


def check(p1: float2, p2: float2, p3: float2) -> float:
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)


def in_triangle(pt: float2, p1: float2, p2: float2, p3: float2) -> bool:
    b1 = check(pt, p1, p2) < 0.0
    b2 = check(pt, p2, p3) < 0.0
    b3 = check(pt, p3, p1) < 0.0
    return b1 == b2 and b2 == b3


def blur_edge(bot1: float2, bot2: float2, top: float2, pt: float2) -> float:
    edge = bot1 - top
    dist1 = abs(dot(normalize(float2(edge.y, -edge.x)), bot1 - pt))
    edge = bot2 - top
    min_dist = min(abs(dot(normalize(float2(edge.y, -edge.x)), bot2 - pt)), dist1)
    return min_dist / 0.005 if min_dist < 0.005 else 1.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    l1 = float2(t, 0.5)
    l2 = float2(0.0, 0.5 - t)
    l3 = float2(0.0, 0.5 + t)
    r1 = float2(1.0 - t, 0.5)
    r2 = float2(1.0, 0.5 - t)
    r3 = float2(1.0, 0.5 + t)
    if in_triangle(uv, l1, l2, l3):
        if t < 0.1:
            return tex_out(uv)
        if uv.x < 0.5:
            return mix(tex_out(uv), tex_in(uv), blur_edge(l2, l3, l1, uv))
        return tex_in(uv) if t > 0.0 else tex_out(uv)
    if in_triangle(uv, r1, r2, r3):
        if uv.x >= 0.5:
            return mix(tex_out(uv), tex_in(uv), blur_edge(r2, r3, r1, uv))
        return tex_out(uv)
    return tex_out(uv)
