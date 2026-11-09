"""Luminance melt

gl-transitions, 0gust1, MIT.
"""
from pyshader import *

DIRECTION = 1.0
L_THRESHOLD = 0.8
ABOVE = False
C = float4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439)
CENTER = float2(1.0, DIRECTION)


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def mod289_3(x: float3) -> float3:
    return x - floor(x * (1.0 / 289.0)) * 289.0


def mod289_2(x: float2) -> float2:
    return x - floor(x * (1.0 / 289.0)) * 289.0


def permute(x: float3) -> float3:
    return mod289_3((x * 34.0 + 1.0) * x)


def snoise(v: float2) -> float:
    i = floor(v + dot(v, C.yy))
    x0 = v - i + dot(i, C.xx)
    i1 = float2(1.0, 0.0) if x0.x > x0.y else float2(0.0, 1.0)
    x12 = x0.xyxy + C.xxzz
    x12.xy -= i1
    i = mod289_2(i)
    p = permute(permute(i.y + float3(0.0, i1.y, 1.0)) + i.x + float3(0.0, i1.x, 1.0))
    m = max(0.5 - float3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0)
    m = m * m
    m = m * m
    x = 2.0 * fract(p * C.www) - 1.0
    h = abs(x) - 0.5
    a0 = x - floor(x + 0.5)
    m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h)
    g = float3(a0.x * x0.x + h.x * x0.y, a0.y * x12.x + h.y * x12.y, a0.z * x12.z + h.z * x12.w)
    return 130.0 * dot(m, g)


def luminance(color: float4) -> float:
    return color.r * 0.299 + color.g * 0.587 + color.b * 0.114


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    if t == 0.0:
        return tex_out(uv)
    if t == 1.0:
        return tex_in(uv)
    dist = distance(CENTER, uv) - t * exp(snoise(float2(uv.x, 0.0)))
    r = t - rand(float2(uv.x, 0.1))
    lum = luminance(tex_out(uv))
    melt = lum > L_THRESHOLD if ABOVE else lum < L_THRESHOLD
    m = 1.0 if dist <= r and melt else t * t * t
    return mix(tex_out(uv), tex_in(uv), m)
