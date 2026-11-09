"""Kaleidoscope

gl-transitions, nwoeanhinnogaehr, MIT.
"""
from pyshader import *

SPEED = 1.0
ANGLE = 1.0
POWER = 1.5


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    k = pow(t, POWER) * SPEED
    p = uv - 0.5
    for i in range(7):
        p = float2(sin(k) * p.x + cos(k) * p.y, sin(k) * p.y - cos(k) * p.x)
        k += ANGLE
        p = abs(mod(p, 2.0) - 1.0)
    return mix(mix(tex_out(uv), tex_in(uv), t), mix(tex_out(p), tex_in(p), t), 1.0 - 2.0 * abs(t - 0.5))
