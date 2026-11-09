"""Multiply blend

gl-transitions, Fernando Kuteken, MIT.
"""
from pyshader import *


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    blended = tex_out(uv) * tex_in(uv)
    if t < 0.5:
        return mix(tex_out(uv), blended, 2.0 * t)
    return mix(blended, tex_in(uv), 2.0 * t - 1.0)
