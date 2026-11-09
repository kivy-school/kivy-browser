"""Circle

gl-transitions, Fernando Kuteken, MIT.
"""
from pyshader import *

CENTER = float2(0.5, 0.5)
BACK_COLOR = float3(0.1, 0.1, 0.1)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    dist = length(uv - CENTER)
    radius = sqrt(8.0) * abs(t - 0.5)
    if dist > radius:
        return float4(BACK_COLOR, 1.0)
    return tex_out(uv) if t < 0.5 else tex_in(uv)
