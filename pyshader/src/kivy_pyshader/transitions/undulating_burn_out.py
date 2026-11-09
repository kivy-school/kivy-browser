"""Undulating burn out

gl-transitions, pthrasher, MIT.
"""
from pyshader import *

SMOOTHNESS = 0.03
CENTER = float2(0.5)
COLOR = float3(0.0)


def quadratic_in_out(x: float) -> float:
    p = 2.0 * x * x
    return p if x < 0.5 else -p + 4.0 * x - 1.0


def gradient(r: float, dist: float) -> float:
    d = r - dist
    return mix(smoothstep(-SMOOTHNESS, 0.0, r - dist * (1.0 + SMOOTHNESS)), -1.0 - step(0.005, d),
               step(-0.005, d) * step(d, 0.01))


def wave(p: float2, x: float) -> float:
    q = p - CENTER
    degs = (degrees(atan(q.y, q.x)) + 180.0) * (PI * 30.0) / 360.0
    magnitude = mix(0.02, 0.09, smoothstep(0.0, 1.0, x))
    offset = mix(40.0, 30.0, smoothstep(0.0, 1.0, x))
    return x + quadratic_in_out(sin(degs)) * magnitude * sin(x * offset)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    m = gradient(wave(uv, t), distance(CENTER, uv))
    a = tex_out(uv)
    b = tex_in(uv)
    return mix(mix(a, b, m), mix(a, float4(COLOR, 1.0), 0.75), step(m, -2.0))
