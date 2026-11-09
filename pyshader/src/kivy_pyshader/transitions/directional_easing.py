"""Directional easing

gl-transitions, Max Plotnikov, MIT.
"""
from pyshader import *

DIRECTION = float2(1.0, 0.0)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    easing = sqrt((2.0 - t) * t)
    p = uv + easing * sign(DIRECTION)
    f = fract(p)
    return mix(tex_in(f), tex_out(f), step(0.0, p.y) * step(p.y, 1.0) * step(0.0, p.x) * step(p.x, 1.0))
