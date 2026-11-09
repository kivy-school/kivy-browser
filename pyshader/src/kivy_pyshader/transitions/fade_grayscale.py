"""Fade grayscale

gl-transitions, gre, MIT.
"""
from pyshader import *

INTENSITY = 0.5


def grayscale(color: float3) -> float3:
    return float3(0.2126 * color.r + 0.7152 * color.g + 0.0722 * color.b)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    fc = tex_out(uv)
    tc = tex_in(uv)
    return mix(mix(float4(grayscale(fc.rgb), 1.0), fc, smoothstep(1.0 - INTENSITY, 0.0, t)),
               mix(float4(grayscale(tc.rgb), 1.0), tc, smoothstep(INTENSITY, 1.0, t)), t)
