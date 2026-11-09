"""Tangent motion blur

gl-transitions, chenkai, MIT.
"""
from pyshader import *

RATIO = 1.0


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def motion_blur_out(st: float2, speed: float2) -> float4:
    color = float3(0.0)
    total = 0.0
    offset = rand(st)
    for i in range(21):
        percent = (float(i) + offset) / 20.0
        weight = 4.0 * (percent - percent * percent)
        color += tex_out(fract(st + speed * percent)).rgb * weight
        total += weight
    return float4(color / total, 1.0)


def motion_blur_in(st: float2, speed: float2) -> float4:
    color = float3(0.0)
    total = 0.0
    offset = rand(st)
    for i in range(21):
        percent = (float(i) + offset) / 20.0
        weight = 4.0 * (percent - percent * percent)
        color += tex_in(fract(st + speed * percent)).rgb * weight
        total += weight
    return float4(color / total, 1.0)


def bez_a(a1: float, a2: float) -> float:
    return 1.0 - 3.0 * a2 + 3.0 * a1


def bez_b(a1: float, a2: float) -> float:
    return 3.0 * a2 - 6.0 * a1


def bez_c(a1: float) -> float:
    return 3.0 * a1


def slope(x: float, a1: float, a2: float) -> float:
    return 3.0 * bez_a(a1, a2) * x * x + 2.0 * bez_b(a1, a2) * x + bez_c(a1)


def bezier(x: float, a1: float, a2: float) -> float:
    return ((bez_a(a1, a2) * x + bez_b(a1, a2)) * x + bez_c(a1)) * x


def t_for_x(x: float, x1: float, x2: float) -> float:
    guess = x
    for i in range(4):
        s = slope(guess, x1, x2)
        if s == 0.0:
            return guess
        guess -= (bezier(guess, x1, x2) - x) / s
    return guess


def key_spline(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
    if x1 == y1 and x2 == y2:
        return x
    return bezier(t_for_x(x, x1, x2), y1, y2)


def normpdf(x: float) -> float:
    return exp(-20.0 * pow(x - 0.5, 2.0))


def rotate_uv(p: float2, angle: float, anchor: float2) -> float2:
    q = p - anchor
    s = sin(angle)
    c = cos(angle)
    return float2(c * q.x + s * q.y, -s * q.x + c * q.y) + anchor


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    easing = key_spline(t, 0.68, 0.01, 0.17, 0.98)
    blur = normpdf(easing)
    rotation = PI
    r = rotation * easing if easing <= 0.5 else -rotation + rotation * easing
    current = rotate_uv(float2(uv.x, uv.y / RATIO), r, float2(1.0, 0.0))
    current.y *= RATIO
    interval = 0.0167 * 2.0
    r = rotation * (easing + interval) if easing <= 0.5 else -rotation + rotation * (easing + interval)
    following = rotate_uv(float2(uv.x, uv.y / RATIO), r, float2(1.0, 0.0))
    following.y *= RATIO
    speed = (following - current) / interval * blur * 0.5
    if easing <= 0.5:
        return motion_blur_out(current, speed)
    return motion_blur_in(current, speed)
