"""Squares wire

gl-transitions, gre, MIT.
"""
from pyshader import *

SQUARES = float2(10.0, 10.0)
DIRECTION = float2(1.0, -0.5)
SMOOTHNESS = 1.6
CENTER = float2(0.5, 0.5)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    v = normalize(DIRECTION)
    v /= abs(v.x) + abs(v.y)
    d = v.x * CENTER.x + v.y * CENTER.y
    pr = smoothstep(-SMOOTHNESS, 0.0, v.x * uv.x + v.y * uv.y - (d - 0.5 + t * (1.0 + SMOOTHNESS)))
    sq = fract(uv * SQUARES)
    lo = float2(pr / 2.0)
    hi = float2(1.0 - pr / 2.0)
    a = (1.0 - step(t, 0.0)) * step(lo.x, sq.x) * step(lo.y, sq.y) * step(sq.x, hi.x) * step(sq.y, hi.y)
    return mix(tex_out(uv), tex_in(uv), a)
