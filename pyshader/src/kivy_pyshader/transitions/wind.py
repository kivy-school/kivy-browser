"""Wind

gl-transitions, gre, MIT.
"""
from pyshader import *

SIZE = 0.2


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    r = rand(float2(0.0, uv.y))
    m = smoothstep(0.0, -SIZE, uv.x * (1.0 - SIZE) + SIZE * r - t * (1.0 + SIZE))
    return mix(tex_out(uv), tex_in(uv), m)
