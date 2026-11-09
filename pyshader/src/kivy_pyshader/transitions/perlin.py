"""Perlin

gl-transitions, Rich Harris, MIT.
"""
from pyshader import *

SCALE = 4.0
SMOOTHNESS = 0.01
SEED = 12.9898


def random(co: float2) -> float:
    dt = dot(co, float2(SEED, 78.233))
    return fract(sin(mod(dt, 3.14)) * 43758.5453)


def value_noise(st: float2) -> float:
    i = floor(st)
    f = fract(st)
    a = random(i)
    b = random(i + float2(1.0, 0.0))
    c = random(i + float2(0.0, 1.0))
    d = random(i + float2(1.0, 1.0))
    u = f * f * (3.0 - 2.0 * f)
    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    n = value_noise(uv * SCALE)
    p = mix(-SMOOTHNESS, 1.0 + SMOOTHNESS, t)
    q = smoothstep(p - SMOOTHNESS, p + SMOOTHNESS, n)
    return mix(tex_out(uv), tex_in(uv), 1.0 - q)
