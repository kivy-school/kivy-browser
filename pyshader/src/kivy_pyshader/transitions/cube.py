"""Cube

gl-transitions, gre, MIT.
"""
from pyshader import *

PERSP = 0.7
UNZOOM = 0.3
REFLECTION = 0.4
FLOATING = 3.0


def project(p: float2) -> float2:
    return p * float2(1.0, -1.2) + float2(0.0, -FLOATING / 100.0)


def in_bounds(p: float2) -> bool:
    return all(float2(0.0) < p) and all(p < float2(1.0))


def background(pfr: float2, pto: float2) -> float4:
    c = float4(0.0, 0.0, 0.0, 1.0)
    q = project(pfr)
    if in_bounds(q):
        c += mix(float4(0.0), tex_out(q), REFLECTION * mix(1.0, 0.0, q.y))
    q = project(pto)
    if in_bounds(q):
        c += mix(float4(0.0), tex_in(q), REFLECTION * mix(1.0, 0.0, q.y))
    return c


def xskew(p: float2, persp: float, center: float) -> float2:
    x = mix(p.x, 1.0 - p.x, center)
    d = abs(center - 0.5)
    skewed = float2(x, (p.y - 0.5 * (1.0 - persp) * x) / (1.0 + (persp - 1.0) * x))
    return ((skewed - float2(0.5 - d, 0.0)) * float2(0.5 / d * (1.0 if center < 0.5 else -1.0), 1.0)
            + float2(0.0 if center < 0.5 else 1.0, 0.0))


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    uz = UNZOOM * 2.0 * (0.5 - abs(0.5 - t))
    p = -uz * 0.5 + (1.0 + uz) * uv
    from_p = xskew((p - float2(t, 0.0)) / float2(1.0 - t, 1.0), 1.0 - mix(t, 0.0, PERSP), 0.0)
    to_p = xskew(p / float2(t, 1.0), mix(pow(t, 2.0), 1.0, PERSP), 1.0)
    if in_bounds(from_p):
        return tex_out(from_p)
    if in_bounds(to_p):
        return tex_in(to_p)
    return background(from_p, to_p)
