"""Doorway

gl-transitions, gre, MIT.
"""
from pyshader import *

REFLECTION = 0.4
PERSPECTIVE = 0.4
DEPTH = 3.0
BLACK = float4(0.0, 0.0, 0.0, 1.0)


def in_bounds(p: float2) -> bool:
    return all(float2(0.0) < p) and all(p < float2(1.0))


def project(p: float2) -> float2:
    return p * float2(1.0, -1.2) + float2(0.0, -0.02)


def background(pto: float2) -> float4:
    c = BLACK
    q = project(pto)
    if in_bounds(q):
        c += mix(BLACK, tex_in(q), REFLECTION * mix(1.0, 0.0, q.y))
    return c


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    pfr = float2(-1.0)
    slit = 2.0 * abs(uv.x - 0.5) - t
    if slit > 0.0:
        pfr = uv + (-1.0 if uv.x > 0.5 else 1.0) * float2(0.5 * t, 0.0)
        d = 1.0 / (1.0 + PERSPECTIVE * t * (1.0 - slit))
        pfr.y -= d / 2.0
        pfr.y *= d
        pfr.y += d / 2.0
    size = mix(1.0, DEPTH, 1.0 - t)
    pto = (uv - 0.5) * size + 0.5
    if in_bounds(pfr):
        return tex_out(pfr)
    if in_bounds(pto):
        return tex_in(pto)
    return background(pto)
