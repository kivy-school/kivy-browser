"""Rotate scale fade

gl-transitions, Fernando Kuteken, MIT.
"""
from pyshader import *

CENTER = float2(0.5, 0.5)
ROTATIONS = 1.0
SCALE = 8.0
BACK_COLOR = float4(0.15, 0.15, 0.15, 1.0)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    difference = uv - CENTER
    direction = normalize(difference)
    dist = length(difference)
    angle = 2.0 * PI * ROTATIONS * t
    c = cos(angle)
    s = sin(angle)
    scale = mix(SCALE, 1.0, 2.0 * abs(t - 0.5))
    rotated = float2(direction.x * c - direction.y * s, direction.x * s + direction.y * c)
    p = CENTER + rotated * dist / scale
    if p.x < 0.0 or p.x > 1.0 or p.y < 0.0 or p.y > 1.0:
        return BACK_COLOR
    return mix(tex_out(p), tex_in(p), t)
