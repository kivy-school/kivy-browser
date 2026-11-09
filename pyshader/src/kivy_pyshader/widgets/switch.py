"""Switch toggle

An on/off switch: a pill outline with a knob that slides across and melts
into the outline on the way. On, it can change to `tint_on` and bloom by
`glow`. stdlib `sdf` (onion, smooth union).
"""
from pyshader import *
import pyshader.stdlib.fragment.sdf as sdf
from pyshader.stdlib.fragment.easing import cubic_in_out

from forms import centered


def main(uv: float2, resolution: float2, morph: float, tint: float4, tint_on: float4, glow: float) -> float4:
    p = centered(uv, resolution)
    k = cubic_in_out(clamp(morph, 0.0, 1.0))
    half = float2(min(0.7, resolution.x / resolution.y * 0.4), 0.27)
    track = sdf.sd_rounded_box(p, half, float4(half.y))
    knob = sdf.sd_circle(p - float2(mix(-1.0, 1.0, k) * (half.x - half.y), 0.0), 0.19)
    d = sdf.op_smooth_union(sdf.op_onion(track, 0.04), knob, 0.08)
    color = mix(tint, tint_on, k)
    inside = sdf.fill_smooth(track, 0.004) * k * 0.35
    shape = max(sdf.fill_smooth(d, 0.004), inside)
    bloom = glow * k * exp(-max(min(d, track), 0.0) * 30.0) * 0.8
    rgb = mix(color.rgb, float3(1.0), bloom * shape * 0.4)
    return float4(rgb, color.a * max(shape, bloom))
