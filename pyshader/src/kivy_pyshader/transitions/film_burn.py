"""Film burn

gl-transitions, Anastasia Dunbar, MIT.
"""
from pyshader import *

SEED = 2.31
REPEATS = 50


def sigmoid(x: float, a: float) -> float:
    b = pow(x * 2.0, a) / 2.0
    if x > 0.5:
        b = 1.0 - pow(2.0 - x * 2.0, a) / 2.0
    return b


def rand1(co: float) -> float:
    return fract(sin(co * 24.9898 + SEED) * 43758.5453)


def rand2(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def apow(a: float, b: float) -> float:
    return pow(abs(a), b) * sign(b)


def pow3(a: float3, b: float3) -> float3:
    return float3(apow(a.r, b.r), apow(a.g, b.g), apow(a.b, b.b))


def smooth_mix(a: float, b: float, c: float) -> float:
    return mix(a, b, sigmoid(c, 2.0))


def random(co: float2, shift: float) -> float:
    p = co + 10.0
    a = fract(sin(dot(p, float2(12.9898 + floor(shift) * 0.5, 78.233 + SEED))) * 43758.5453)
    b = fract(sin(dot(p, float2(12.9898 + floor(shift + 1.0) * 0.5, 78.233 + SEED))) * 43758.5453)
    return smooth_mix(a, b, fract(shift))


def smooth_random(co: float2, shift: float) -> float:
    c = floor(co)
    bottom = smooth_mix(random(c, shift), random(c + float2(1.0, 0.0), shift), fract(co.x))
    top = smooth_mix(random(c + float2(0.0, 1.0), shift), random(c + float2(1.0, 1.0), shift), fract(co.x))
    return smooth_mix(bottom, top, fract(co.y))


def blend(p: float2, progress: float) -> float4:
    return mix(tex_out(p), tex_in(p), sigmoid(progress, 10.0))


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    f = float3(0.0)
    for n in range(13):
        i = float(n)
        f += (sin(uv.x * rand1(i) * 6.0 + t * 8.0 + rand1(i + 1.43))
              * sin(uv.y * rand1(i + 4.4) * 6.0 + t * 6.0 + rand1(i + 2.4)))
        spot = float2(smooth_random(float2(t * 1.3), i + 1.0), smooth_random(float2(t * 0.5), i + 6.25))
        f += 1.0 - clamp(length(uv - spot) * mix(20.0, 70.0, rand1(i)), 0.0, 1.0)
    f += 4.0
    f /= 11.0
    f = pow3(f * float3(1.0, 0.7, 0.6), float3(1.0, 2.0 - sin(t * PI), 1.3))
    f *= sin(t * PI)
    p = uv - 0.5
    p *= 1.0 + smooth_random(float2(t * 5.0), 6.3) * sin(t * PI) * 0.05
    p += 0.5
    blurred = float4(0.0)
    amount = sin(t * PI) * 0.03
    for m in range(REPEATS):
        k = float(m)
        a = degrees(k / float(REPEATS) * 360.0)
        q = float2(cos(a), sin(a)) * (rand2(float2(k, p.x + p.y)) + amount)
        blurred += blend(p + q * amount, t)
    blurred /= float(REPEATS)
    return blurred + float4(f, 0.0)
