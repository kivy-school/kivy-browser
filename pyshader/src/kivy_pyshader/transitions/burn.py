"""Burn

gl-transitions, gre, MIT.
"""
from pyshader import *

COLOR = float3(0.9, 0.4, 0.2)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    return mix(tex_out(uv) + float4(t * COLOR, 1.0), tex_in(uv) + float4((1.0 - t) * COLOR, 1.0), t)
