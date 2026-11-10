"""Glint button

A bevelled button lit from above, casting a shadow. A press pushes it in,
the shadow tightening under it, and sweeps a glint across it. stdlib
`light` (bevel_normal, lambert, blinn_phong, fresnel, shine, drop_shadow).
"""
from pyshader import *
import pyshader.stdlib.fragment.light as light
import pyshader.stdlib.fragment.sdf as sdf

from forms import form, within, panel


def main(uv: float2, resolution: float2, shape: float, pressed: float, tint: float4) -> float4:
    p = within(uv, resolution)
    k = clamp(pressed, 0.0, 1.0)
    push = 1.0 - k
    q = p / (1.0 - 0.04 * push)
    d = form(q, shape)
    e = 0.001
    g = normalize(float2(form(q + float2(e, 0.0), shape) - d, form(q + float2(0.0, e), shape) - d))
    l = normalize(float3(-0.4, 0.6, 1.3))
    n = light.bevel_normal(d, g, 0.05)
    face = tint.rgb * (0.25 + 0.75 * light.lambert(n, l)) * (1.0 - 0.2 * push)
    face += float3(0.9) * light.blinn_phong(n, l, 80.0) + float3(0.3) * light.fresnel(n, 0.0, 4.0)
    face += float3(0.6) * light.shine(q, 0.9, mix(-0.7, 0.7, k), 0.1) * sin(PI * k)
    shadow = light.drop_shadow(form(q + float2(0.0, mix(0.05, 0.012, push)), shape), mix(0.035, 0.012, push))
    base = float3(0.13, 0.14, 0.18) * (1.0 - 0.6 * shadow)
    rgb = light.tonemap_reinhard(mix(base, face, sdf.fill_smooth(d, 0.003)) * 1.4)
    return panel(uv, resolution, rgb, tint)
