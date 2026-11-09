"""Cross zoom

gl-transitions, rectalogic, MIT.
"""
from pyshader import *

STRENGTH = 0.4


def linear_ease(begin: float, change: float, duration: float, x: float) -> float:
    return change * x / duration + begin


def exponential_ease_in_out(begin: float, change: float, duration: float, x: float) -> float:
    if x == 0.0:
        return begin
    if x == duration:
        return begin + change
    k = x / (duration / 2.0)
    if k < 1.0:
        return change / 2.0 * pow(2.0, 10.0 * (k - 1.0)) + begin
    return change / 2.0 * (-pow(2.0, -10.0 * (k - 1.0)) + 2.0) + begin


def sinusoidal_ease_in_out(begin: float, change: float, duration: float, x: float) -> float:
    return -change / 2.0 * (cos(PI * x / duration) - 1.0) + begin


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def cross_fade(p: float2, dissolve: float) -> float3:
    return mix(tex_out(p).rgb, tex_in(p).rgb, dissolve)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    center = float2(linear_ease(0.25, 0.5, 1.0, t), 0.5)
    dissolve = exponential_ease_in_out(0.0, 1.0, 1.0, t)
    strength = sinusoidal_ease_in_out(0.0, STRENGTH, 0.5, t)
    color = float3(0.0)
    total = 0.0
    to_center = center - uv
    offset = rand(uv)
    for i in range(41):
        percent = (float(i) + offset) / 40.0
        weight = 4.0 * (percent - percent * percent)
        color += cross_fade(uv + to_center * percent * strength, dissolve) * weight
        total += weight
    return float4(color / total, 1.0)
