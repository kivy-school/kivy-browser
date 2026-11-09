"""Cross warp

gl-transitions, Eke Péter, MIT.
"""
from pyshader import *


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    x = smoothstep(0.0, 1.0, t * 2.0 + uv.x - 1.0)
    return mix(tex_out((uv - 0.5) * (1.0 - x) + 0.5), tex_in((uv - 0.5) * x + 0.5), x)
