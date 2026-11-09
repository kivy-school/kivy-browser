"""Pixelize

gl-transitions, gre, MIT.
"""
from pyshader import *

SQUARES_MIN = 20.0
STEPS = 50.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    d = min(t, 1.0 - t)
    dist = ceil(d * STEPS) / STEPS
    p = uv
    if dist > 0.0:
        size = 2.0 * dist / SQUARES_MIN
        p = (floor(uv / size) + 0.5) * size
    return mix(tex_out(p), tex_in(p), t)
