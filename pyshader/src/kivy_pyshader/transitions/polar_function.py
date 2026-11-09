"""Polar function

gl-transitions, Fernando Kuteken, MIT.
"""
from pyshader import *

SEGMENTS = 5.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    angle = atan(uv.y - 0.5, uv.x - 0.5) - 0.5 * PI
    radius = (cos(SEGMENTS * angle) + 4.0) / 4.0
    if length(uv - float2(0.5, 0.5)) > radius * t:
        return tex_out(uv)
    return tex_in(uv)
