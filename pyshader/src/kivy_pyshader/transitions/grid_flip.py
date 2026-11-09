"""Grid flip

gl-transitions, TimDonselaar, MIT.
"""
from pyshader import *

SIZE = float2(4.0)
PAUSE = 0.1
DIVIDER_WIDTH = 0.05
BG_COLOR = float4(0.0, 0.0, 0.0, 1.0)
RANDOMNESS = 0.1


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def delta(p: float2) -> float:
    pos = floor(SIZE * p)
    size = 1.0 / SIZE
    top = size.y * (pos.y + 1.0)
    bottom = size.y * pos.y
    left = size.x * pos.x
    right = size.x * (pos.x + 1.0)
    return min(min(abs(p.x - left), abs(p.x - right)), min(abs(p.y - top), abs(p.y - bottom)))


def divider_size() -> float:
    size = 1.0 / SIZE
    return min(size.x, size.y) * DIVIDER_WIDTH


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    on_divider = delta(uv) < divider_size()
    if t < PAUSE:
        alpha = 1.0 - t / PAUSE if on_divider else 1.0
        return mix(BG_COLOR, tex_out(uv), alpha)
    if t < 1.0 - PAUSE:
        if on_divider:
            return BG_COLOR
        k = (t - PAUSE) / (1.0 - PAUSE * 2.0)
        pos = floor(SIZE * uv)
        r = rand(pos) - RANDOMNESS
        cp = smoothstep(0.0, 1.0 - r, k)
        size = 1.0 / SIZE.x
        d = pos.x * size
        offset = size / 2.0 + d
        p = float2((uv.x - offset) / abs(cp - 0.5) * 0.5 + offset, uv.y)
        s = step(abs(SIZE.x * (uv.x - d) - 0.5), abs(cp - 0.5))
        return mix(BG_COLOR, mix(tex_in(p), tex_out(p), step(cp, 0.5)), s)
    alpha = (t - 1.0 + PAUSE) / PAUSE if on_divider else 1.0
    return mix(BG_COLOR, tex_in(uv), alpha)
