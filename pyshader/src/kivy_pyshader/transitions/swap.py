"""Swap

gl-transitions, gre, MIT.
"""
from pyshader import *

REFLECTION = 0.4
PERSPECTIVE = 0.2
DEPTH = 3.0

BLACK = float4(0.0, 0.0, 0.0, 1.0)


def in_bounds(p: float2) -> bool:
    return all(float2(0.0) < p) and all(p < float2(1.0))


def project(p: float2) -> float2:
    return p * float2(1.0, -1.2) + float2(0.0, -0.02)


def background(pfr: float2, pto: float2) -> float4:
    c = BLACK
    q = project(pfr)
    if in_bounds(q):
        c += mix(BLACK, tex_out(q), REFLECTION * mix(1.0, 0.0, q.y))
    q = project(pto)
    if in_bounds(q):
        c += mix(BLACK, tex_in(q), REFLECTION * mix(1.0, 0.0, q.y))
    return c


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    size = mix(1.0, DEPTH, t)
    persp = PERSPECTIVE * t
    pfr = (uv + float2(0.0, -0.5)) * float2(size / (1.0 - PERSPECTIVE * t), size / (1.0 - size * persp * uv.x)) + float2(0.0, 0.5)
    size = mix(1.0, DEPTH, 1.0 - t)
    persp = PERSPECTIVE * (1.0 - t)
    pto = ((uv + float2(-1.0, -0.5)) * float2(size / (1.0 - PERSPECTIVE * (1.0 - t)), size / (1.0 - size * persp * (0.5 - uv.x)))
           + float2(1.0, 0.5))
    if t < 0.5:
        if in_bounds(pfr):
            return tex_out(pfr)
        if in_bounds(pto):
            return tex_in(pto)
    if in_bounds(pto):
        return tex_in(pto)
    if in_bounds(pfr):
        return tex_out(pfr)
    return background(pfr, pto)
