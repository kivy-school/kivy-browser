"""Simple zoom

gl-transitions, 0gust1, MIT.
"""
from pyshader import *

QUICKNESS = 0.8


def zoom(p: float2, amount: float) -> float2:
    return 0.5 + (p - 0.5) * (1.0 - amount)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    return mix(tex_out(zoom(uv, smoothstep(0.0, QUICKNESS, t))), tex_in(uv), smoothstep(QUICKNESS - 0.2, 1.0, t))
