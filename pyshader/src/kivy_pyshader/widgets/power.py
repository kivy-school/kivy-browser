"""Power toggle

A ring and a power sign, faint light guides. Down, a light runs round the
ring from the top, the sign lights and the inside glows; up, it drains
back. stdlib `light` (glow_edge, glow_inner, tonemap_exposure), `sdf.sd_arc`.
"""
from pyshader import *
import pyshader.stdlib.fragment.light as light
import pyshader.stdlib.fragment.sdf as sdf
from pyshader.stdlib.fragment.easing import cubic_in_out

from forms import within, panel


def sign(p: float2) -> float:
    gap = 2.5
    arc = sdf.sd_arc(float2(p.x, -p.y), float2(sin(gap), cos(gap)), 0.13, 0.018)
    return min(arc, sdf.sd_segment(p, float2(0.0, 0.02), float2(0.0, 0.16)) - 0.018)


def main(uv: float2, resolution: float2, morph: float, tint: float4) -> float4:
    p = within(uv, resolution)
    k = cubic_in_out(clamp(morph, 0.0, 1.0))
    ring = sdf.op_onion(sdf.sd_circle(p, 0.34), 0.02)
    # How far round from the top, clockwise, 0..1.
    f = fract(0.25 - atan2(p.y, p.x) / (2.0 * PI))
    end = k * 1.04 - 0.02
    run = 1.0 - smoothstep(end - 0.01, end + 0.01, f)
    head = exp(-max(end - f, 0.0) * 10.0) * sin(PI * k)
    c = tint.rgb * light.glow_edge(ring, 0.006) * (0.08 + run * (0.6 + 2.0 * head))
    c += tint.rgb * light.glow_edge(sign(p), 0.006) * (0.08 + 0.9 * k)
    c += tint.rgb * 0.4 * k * light.glow_inner(sdf.sd_circle(p, 0.32), 0.06)
    rgb = light.tonemap_exposure(c + float3(0.03, 0.035, 0.05), 1.0)
    return panel(uv, resolution, rgb, tint)
