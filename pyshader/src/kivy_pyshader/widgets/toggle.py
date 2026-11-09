"""Morph toggle

Down morphs shape A into shape B, up morphs it back, turning and changing
color on the way.
"""
from pyshader import *
from pyshader.stdlib.fragment.sdf import fill_smooth
from pyshader.stdlib.fragment.easing import back_in_out

from forms import form, centered


def main(uv: float2, resolution: float2, shape_a: float, shape_b: float, morph: float, tint: float4, tint_on: float4) -> float4:
    p = centered(uv, resolution)
    k = back_in_out(clamp(morph, 0.0, 1.0))
    a = k * PI * 0.5
    q = float2(cos(a) * p.x - sin(a) * p.y, sin(a) * p.x + cos(a) * p.y)
    d = mix(form(q, shape_a), form(q, shape_b), k)
    color = mix(tint, tint_on, clamp(k, 0.0, 1.0))
    return float4(color.rgb, color.a * fill_smooth(d, 0.006))
