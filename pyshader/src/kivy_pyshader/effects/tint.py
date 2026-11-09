"""Tint (arguments)

`tint` and `strength` are shader arguments: uniforms the app sets.
"""
from pyshader import *


def main(uv: float2, tint: float4, strength: float) -> float4:
    c = layer(uv)
    return float4(mix(c.rgb, tint.rgb, strength * c.a), c.a)
