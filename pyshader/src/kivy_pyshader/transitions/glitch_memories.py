"""Glitch memories

gl-transitions, Gunnar Roth, MIT.
"""
from pyshader import *


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    block = floor(uv / float2(16.0))
    noise = block / float2(64.0)
    noise += floor(float2(t) * float2(1200.0, 3500.0)) / float2(64.0)
    dist = (fract(noise) - 0.5) * 0.3 * (1.0 - t) if t > 0.0 else float2(0.0)
    red = uv + dist * 0.2
    green = uv + dist * 0.3
    blue = uv + dist * 0.5
    return float4(mix(tex_out(red), tex_in(red), t).r, mix(tex_out(green), tex_in(green), t).g,
                  mix(tex_out(blue), tex_in(blue), t).b, 1.0)
