"""Ripple button

A rounded button; a ring runs out from where it was touched and fades.
stdlib `sdf.sd_rounded_box`.
"""
from pyshader import *
from pyshader.stdlib.fragment.sdf import sd_rounded_box, fill_smooth
from pyshader.stdlib.fragment.easing import quad_out


def main(uv: float2, resolution: float2, touch: float2, pressed: float, tint: float4) -> float4:
    px = uv * resolution
    half = resolution * 0.5
    d = sd_rounded_box(px - half, half - 1.0, float4(min(half.x, half.y) * 0.5))
    body = fill_smooth(d, 1.0)
    k = quad_out(clamp(pressed, 0.0, 1.0))
    reach = k * length(resolution)
    dist = length(px - touch)
    ring = 1.0 - smoothstep(0.0, 14.0, abs(dist - reach))
    inside = 1.0 - smoothstep(reach - 1.0, reach + 1.0, dist)
    light = (ring * 0.55 + inside * 0.2) * (1.0 - k)
    return float4(mix(tint.rgb, float3(1.0), light), tint.a * body)
