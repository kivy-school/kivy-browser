"""Dreamy

gl-transitions, mikolalysenko, MIT.
"""
from pyshader import *


def offset(progress: float, x: float) -> float2:
    return float2(0.0, 0.03 * progress * cos(10.0 * (progress + x)))


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    return mix(tex_out(uv + offset(t, uv.x)), tex_in(uv + offset(1.0 - t, uv.x)), t)
