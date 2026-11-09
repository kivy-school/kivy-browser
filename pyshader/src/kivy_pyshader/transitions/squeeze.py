"""Squeeze

gl-transitions, gre, MIT.
"""
from pyshader import *

COLOR_SEPARATION = 0.04


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    y = 0.5 + (uv.y - 0.5) / (1.0 - t)
    if y < 0.0 or y > 1.0:
        return tex_in(uv)
    fp = float2(uv.x, y)
    off = t * float2(0.0, COLOR_SEPARATION)
    c = tex_out(fp)
    cn = tex_out(fp - off)
    cp = tex_out(fp + off)
    return float4(cn.r, c.g, cp.b, c.a)
