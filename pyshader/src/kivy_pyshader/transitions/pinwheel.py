"""Pinwheel

gl-transitions, Mr Speaker, MIT.
"""
from pyshader import *

SPEED = 2.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    pos = atan(uv.y - 0.5, uv.x - 0.5) + t * SPEED
    m = mod(pos, 3.1415 / 4.0)
    s = sign(t - m)
    return mix(tex_in(uv), tex_out(uv), step(s, 0.5))
