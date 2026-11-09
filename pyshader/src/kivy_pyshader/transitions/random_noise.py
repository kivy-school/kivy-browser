"""Random noise

gl-transitions, towrabbit, MIT.
"""
from pyshader import *


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    return mix(tex_out(uv), tex_in(uv), floor(rand(uv) + t))
