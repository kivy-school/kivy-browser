"""Swirl

gl-transitions, Sergey Kosarevsky, MIT.
"""
from pyshader import *

RADIUS = 1.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    p = uv - float2(0.5, 0.5)
    dist = length(p)
    if dist < RADIUS:
        percent = (RADIUS - dist) / RADIUS
        a = mix(0.0, 1.0, t / 0.5) if t <= 0.5 else mix(1.0, 0.0, (t - 0.5) / 0.5)
        theta = percent * percent * a * 8.0 * 3.14159
        s = sin(theta)
        c = cos(theta)
        p = float2(dot(p, float2(c, -s)), dot(p, float2(s, c)))
    p += float2(0.5, 0.5)
    return mix(tex_out(p), tex_in(p), t)
