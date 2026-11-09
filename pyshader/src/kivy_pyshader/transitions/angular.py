"""Angular

gl-transitions, Fernando Kuteken, MIT.
"""
from pyshader import *

STARTING_ANGLE = 90.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    offset = STARTING_ANGLE * PI / 180.0
    angle = atan(uv.y - 0.5, uv.x - 0.5) + offset
    a = (angle + PI) / (2.0 * PI)
    a = a - floor(a)
    return mix(tex_out(uv), tex_in(uv), step(a, t))
