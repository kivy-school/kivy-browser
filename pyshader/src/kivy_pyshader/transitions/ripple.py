"""Ripple

gl-transitions, gre, MIT.
"""
from pyshader import *

AMPLITUDE = 100.0
SPEED = 50.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    direction = uv - float2(0.5)
    dist = length(direction)
    offset = direction * (sin(t * dist * AMPLITUDE - t * SPEED) + 0.5) / 30.0
    return mix(tex_out(uv + offset), tex_in(uv), smoothstep(0.2, 1.0, t))
