"""Mosaic

gl-transitions, Xaychru, MIT.
"""
from pyshader import *

END_X = 2.0
END_Y = -1.0


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def rotate(v: float2, a: float) -> float2:
    c = cos(a)
    s = sin(a)
    return float2(v.x * c + v.y * s, -v.x * s + v.y * c)


def cos_interpolation(x: float) -> float:
    return -cos(x * PI) / 2.0 + 0.5


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    rp = uv - 0.5
    rpr = t * 2.0 - 1.0
    z = -(rpr * rpr * 2.0) + 3.0
    rp *= abs(z)
    ci = cos_interpolation(t)
    rp += mix(float2(0.5, 0.5), float2(END_X + 0.5, END_Y + 0.5), ci * ci)
    mrp = mod(rp, 1.0)
    cell = floor(rp)
    on_end = cell.x == END_X and cell.y == END_Y
    if not on_end:
        angle = floor(rand(cell) * 4.0) * 0.5 * PI
        mrp = float2(0.5) + rotate(mrp - float2(0.5), angle)
    if on_end or rand(cell) > 0.5:
        return tex_in(mrp)
    return tex_out(mrp)
