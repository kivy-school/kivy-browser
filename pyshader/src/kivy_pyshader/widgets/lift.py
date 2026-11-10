"""Lift toggle

A card on a surface. Down lifts it: its shadow grows, softens and falls
further away; up sets it back down. stdlib `light` (box_shadow,
drop_shadow).
"""
from pyshader import *
import pyshader.stdlib.fragment.light as light
import pyshader.stdlib.fragment.sdf as sdf
from pyshader.stdlib.fragment.easing import cubic_in_out

from forms import form, within, panel


def shadow(p: float2, shape: float, blur: float) -> float:
    if shape > 3.5:
        return light.box_shadow(p, float2(0.29), 0.08, blur)
    return light.drop_shadow(form(p, shape), blur)


def main(uv: float2, resolution: float2, shape: float, morph: float, tint: float4) -> float4:
    p = within(uv, resolution)
    k = cubic_in_out(clamp(morph, 0.0, 1.0))
    q = p / (1.0 + 0.06 * k)
    dark = (0.45 - 0.15 * k) * shadow(q + float2(0.0, 0.01 + 0.07 * k), shape, 0.01 + 0.05 * k)
    rgb = float3(0.85, 0.86, 0.89) * (1.0 - dark)
    rgb = mix(rgb, tint.rgb, sdf.fill_smooth(form(q, shape), 0.003))
    return panel(uv, resolution, rgb, tint)
