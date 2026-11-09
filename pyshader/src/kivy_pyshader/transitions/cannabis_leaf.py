"""Cannabis leaf

gl-transitions, Flexi23, MIT.
"""
from pyshader import *


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    if t == 0.0:
        return tex_out(uv)
    leaf = (uv - float2(0.5)) / 10.0 / pow(t, 3.5)
    leaf.y += 0.35
    r = 0.18
    o = atan(leaf.y, leaf.x)
    edge = 1.0 - length(leaf) + (r * (1.0 + sin(o)) * (1.0 + 0.9 * cos(8.0 * o))
                                 * (1.0 + 0.1 * cos(24.0 * o)) * (0.9 + 0.05 * cos(200.0 * o)))
    return mix(tex_out(uv), tex_in(uv), 1.0 - step(edge, 1.0))
