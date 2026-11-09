"""Half math

16-bit float math, a float hash, and vector comparisons reduced with any()/all().
"""
from pyshader import *


def hash21(p: float2) -> float:
    q = fract(float3(p.x, p.y, p.x) * 0.1031)
    q += dot(q, q.yzx + 33.33)
    return fract((q.x + q.y) * q.z)


def main(uv: float2, time: float) -> float4:
    cell = floor(uv * 12.0)
    n = hash21(cell + floor(time))
    h: half2 = half2(uv)
    hv = h * half(2.0) - half(1.0)
    ring = float(length(hv))
    bright = any(abs(hv) > half(0.9)) or all(abs(hv) < half(0.1))
    base = float3(n, fract(n * 7.0), fract(n * 13.0))
    return float4(base * (1.0 - ring * 0.5) + (float3(0.4) if bright else float3(0.0)), 1.0)
