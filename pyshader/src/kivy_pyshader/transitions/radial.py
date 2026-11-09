"""Radial

gl-transitions, Xaychru, MIT.
"""
from pyshader import *

SMOOTHNESS = 1.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    rp = uv * 2.0 - 1.0
    return mix(tex_in(uv), tex_out(uv), smoothstep(0.0, SMOOTHNESS, atan(rp.y, rp.x) - (t - 0.5) * PI * 2.5))
