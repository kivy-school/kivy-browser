"""Window slice

gl-transitions, gre, MIT.
"""
from pyshader import *

COUNT = 10.0
SMOOTHNESS = 0.5


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    pr = smoothstep(-SMOOTHNESS, 0.0, uv.x - t * (1.0 + SMOOTHNESS))
    s = step(pr, fract(COUNT * uv.x))
    return mix(tex_out(uv), tex_in(uv), s)
