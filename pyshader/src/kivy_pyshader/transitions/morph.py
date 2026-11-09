"""Morph

gl-transitions, paniq, MIT.
"""
from pyshader import *

STRENGTH = 0.1


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    ca = tex_out(uv)
    cb = tex_in(uv)
    oa = (ca.rg + ca.b) * 0.5 * 2.0 - 1.0
    ob = (cb.rg + cb.b) * 0.5 * 2.0 - 1.0
    oc = mix(oa, ob, 0.5) * STRENGTH
    return mix(tex_out(uv + oc * t), tex_in(uv - oc * (1.0 - t)), t)
