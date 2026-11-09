"""Polka dots curtain

gl-transitions, bobylito, MIT.
"""
from pyshader import *

DOTS = 20.0
CENTER = float2(0.0, 0.0)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    next_image = distance(fract(uv * DOTS), float2(0.5)) < t / distance(uv, CENTER)
    return tex_in(uv) if next_image else tex_out(uv)
