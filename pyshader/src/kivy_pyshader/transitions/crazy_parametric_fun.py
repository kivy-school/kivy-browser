"""Crazy parametric fun

gl-transitions, mandubian, MIT.
"""
from pyshader import *

A = 4.0
B = 1.0
AMPLITUDE = 120.0
SMOOTHNESS = 0.1


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    direction = uv - float2(0.5)
    dist = length(direction)
    x = (A - B) * cos(t) + B * cos(t * (A / B - 1.0))
    y = (A - B) * sin(t) - B * sin(t * (A / B - 1.0))
    offset = direction * float2(sin(t * dist * AMPLITUDE * x), sin(t * dist * AMPLITUDE * y)) / SMOOTHNESS
    return mix(tex_out(uv + offset), tex_in(uv), smoothstep(0.2, 1.0, t))
