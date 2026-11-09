"""Hexagonalize

gl-transitions, Fernando Kuteken, MIT.
"""
from pyshader import *

STEPS = 50.0
HORIZONTAL_HEXAGONS = 20.0


class Hexagon:
    q: float
    r: float
    s: float


def create(q: float, r: float) -> Hexagon:
    return Hexagon(q, r, -q - r)


def round_hexagon(h: Hexagon) -> Hexagon:
    q = floor(h.q + 0.5)
    r = floor(h.r + 0.5)
    s = floor(h.s + 0.5)
    dq = abs(q - h.q)
    dr = abs(r - h.r)
    ds = abs(s - h.s)
    if dq > dr and dq > ds:
        q = -r - s
    elif dr > ds:
        r = -q - s
    return create(q, r)


def from_point(point: float2, size: float, ratio: float) -> Hexagon:
    p = (float2(point.x, point.y / ratio) - 0.5) / size
    return round_hexagon(create(sqrt(3.0) / 3.0 * p.x - p.y / 3.0, 2.0 / 3.0 * p.y))


def to_point(h: Hexagon, size: float, ratio: float) -> float2:
    x = (sqrt(3.0) * h.q + sqrt(3.0) / 2.0 * h.r) * size + 0.5
    y = (3.0 / 2.0 * h.r) * size + 0.5
    return float2(x, y * ratio)


def main(uv: float2, t: float, resolution: float2, tex_in: Texture, tex_out: Texture) -> float4:
    ratio = resolution.x / resolution.y
    dist = ceil(2.0 * min(t, 1.0 - t) * STEPS) / STEPS
    point = uv
    if dist > 0.0:
        size = sqrt(3.0) / 3.0 * dist / HORIZONTAL_HEXAGONS
        point = to_point(from_point(uv, size, ratio), size, ratio)
    return mix(tex_out(point), tex_in(point), t)
