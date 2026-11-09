"""Linear blur

gl-transitions, gre, MIT.
"""
from pyshader import *

INTENSITY = 0.1
PASSES = 6


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    c1 = float4(0.0)
    c2 = float4(0.0)
    disp = INTENSITY * (0.5 - abs(0.5 - t))
    for xi in range(PASSES):
        x = float(xi) / float(PASSES) - 0.5
        for yi in range(PASSES):
            y = float(yi) / float(PASSES) - 0.5
            v = float2(x, y)
            c1 += tex_out(uv + disp * v)
            c2 += tex_in(uv + disp * v)
    c1 /= float(PASSES * PASSES)
    c2 /= float(PASSES * PASSES)
    return mix(c1, c2, t)
