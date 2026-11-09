"""Morph toggle

Down morphs shape A into shape B, up morphs it back, turning on the way.
"""
from pyshader import *
from pyshader.stdlib.fragment.sdf import fill_smooth
from pyshader.stdlib.fragment.easing import back_in_out

from forms import form, within, plate, over


def main(uv: float2, resolution: float2, shape_a: float, shape_b: float, morph: float, tint: float4) -> float4:
    p = within(uv, resolution)
    k = back_in_out(clamp(morph, 0.0, 1.0))
    a = k * PI * 0.5
    q = float2(cos(a) * p.x - sin(a) * p.y, sin(a) * p.x + cos(a) * p.y)
    d = mix(form(q, shape_a), form(q, shape_b), k)
    return over(float4(tint.rgb, tint.a * fill_smooth(d, 0.006)), plate(uv, resolution, tint, sin(PI * clamp(morph, 0.0, 1.0))))
