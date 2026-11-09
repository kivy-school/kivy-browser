"""Merge toggle

Down slides a circle and a box together and melts them into one with a
smooth union; up pulls them apart again. stdlib `sdf`.
"""
from pyshader import *
import pyshader.stdlib.fragment.sdf as sdf
from pyshader.stdlib.fragment.easing import back_in_out

from forms import within, plate, over


def main(uv: float2, resolution: float2, morph: float, tint: float4) -> float4:
    p = within(uv, resolution)
    k = back_in_out(clamp(morph, 0.0, 1.0))
    gap = mix(0.26, 0.0, k)
    a = sdf.sd_circle(p - float2(gap, 0.0), 0.17)
    b = sdf.sd_box(p + float2(gap, 0.0), float2(0.13))
    d = sdf.op_smooth_union(a, b, mix(0.02, 0.22, clamp(k, 0.0, 1.0)))
    edge = sdf.stroke_smooth(d, 0.01, 0.003)
    shape = float4(mix(tint.rgb, float3(1.0), edge * 0.6), tint.a * max(sdf.fill_smooth(d, 0.004), edge))
    return over(shape, plate(uv, resolution, tint, sin(PI * clamp(morph, 0.0, 1.0))))
