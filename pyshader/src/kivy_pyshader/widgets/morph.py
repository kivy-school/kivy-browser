"""Morph button

Every press morphs the shape into the next: circle, star, heart, hexagon,
rounded square. Distances from stdlib `sdf`, blended.
"""
from pyshader import *
from pyshader.stdlib.fragment.sdf import fill_smooth, stroke_smooth
from pyshader.stdlib.fragment.easing import cubic_in_out

from forms import form, within, plate, over


def main(uv: float2, resolution: float2, shape_from: float, shape_to: float, pressed: float, tint: float4) -> float4:
    p = within(uv, resolution)
    k = cubic_in_out(clamp(pressed, 0.0, 1.0))
    d = mix(form(p, shape_from), form(p, shape_to), k)
    body = fill_smooth(d, 0.006)
    edge = stroke_smooth(d, 0.016, 0.004)
    rgb = mix(tint.rgb, float3(1.0), edge * 0.7)
    return over(float4(rgb, tint.a * max(body, edge)), plate(uv, resolution, tint, 1.0 - clamp(pressed, 0.0, 1.0)))
