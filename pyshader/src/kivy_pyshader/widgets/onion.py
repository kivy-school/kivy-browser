"""Onion button

Every press sends outlines out from the shape, each fainter than the last.
stdlib `sdf.op_onion`.
"""
from pyshader import *
import pyshader.stdlib.fragment.sdf as sdf
from pyshader.stdlib.fragment.easing import quad_out

from forms import centered, form

ECHOES = 3


def main(uv: float2, resolution: float2, shape: float, pressed: float, tint: float4) -> float4:
    p = centered(uv, resolution)
    d = form(p, shape)
    k = clamp(pressed, 0.0, 1.0)
    glow = 0.0
    for i in range(ECHOES):
        step_k = quad_out(clamp(k * 1.3 - float(i) * 0.15, 0.0, 1.0))
        ring = sdf.stroke_smooth(sdf.op_onion(d - step_k * 0.2, 0.01), 0.006, 0.003)
        glow = max(glow, ring * (1.0 - step_k) * (1.0 - float(i) * 0.25))
    body = sdf.fill_smooth(d, 0.004)
    rgb = mix(tint.rgb, float3(1.0), glow * (1.0 - body))
    return float4(rgb, tint.a * max(body, glow))
