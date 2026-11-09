"""Directional warp

gl-transitions, pschroen, MIT.
"""
from pyshader import *

DIRECTION = float2(-1.0, 1.0)
SMOOTHNESS = 0.5
CENTER = float2(0.5, 0.5)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    v = normalize(DIRECTION)
    v /= abs(v.x) + abs(v.y)
    d = v.x * CENTER.x + v.y * CENTER.y
    m = 1.0 - smoothstep(-SMOOTHNESS, 0.0, v.x * uv.x + v.y * uv.y - (d - 0.5 + t * (1.0 + SMOOTHNESS)))
    return mix(tex_out((uv - 0.5) * (1.0 - m) + 0.5), tex_in((uv - 0.5) * m + 0.5), m)
