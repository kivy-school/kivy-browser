"""Fade color

gl-transitions, gre, MIT.
"""
from pyshader import *

COLOR = float3(0.0)
COLOR_PHASE = 0.3


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    color = float4(COLOR, 1.0)
    return mix(mix(color, tex_out(uv), smoothstep(1.0 - COLOR_PHASE, 0.0, t)),
               mix(color, tex_in(uv), smoothstep(COLOR_PHASE, 1.0, t)), t)
