"""Colour distance

gl-transitions, P-Seebauer, MIT.
"""
from pyshader import *

POWER = 5.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    a = tex_out(uv)
    b = tex_in(uv)
    m = step(distance(a, b), t)
    return mix(mix(a, b, m), b, pow(t, POWER))
