"""Wipe right

gl-transitions, Jake Nelson, MIT.
"""
from pyshader import *


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    return mix(tex_out(uv), tex_in(uv), step(uv.x, t))
