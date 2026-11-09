"""Random squares

gl-transitions, gre, MIT.
"""
from pyshader import *

SIZE = float2(10.0, 10.0)
SMOOTHNESS = 0.5


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    r = rand(floor(SIZE * uv))
    m = smoothstep(0.0, -SMOOTHNESS, r - t * (1.0 + SMOOTHNESS))
    return mix(tex_out(uv), tex_in(uv), m)
