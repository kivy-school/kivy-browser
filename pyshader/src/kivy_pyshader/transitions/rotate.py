"""Rotate

gl-transitions, haiyoucuv, MIT.
"""
from pyshader import *


def rotate(p: float2, angle: float) -> float2:
    c = cos(angle)
    s = sin(angle)
    return float2(p.x * c - p.y * s, p.x * s + p.y * c)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    p = fract(rotate(uv - 0.5, t * PI * 2.0) + 0.5)
    return mix(tex_out(p), tex_in(p), t)
