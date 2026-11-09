"""Heart

gl-transitions, gre, MIT.
"""
from pyshader import *


def in_heart(p: float2, center: float2, size: float) -> float:
    if size == 0.0:
        return 0.0
    o = (p - center) / (1.6 * size)
    a = o.x * o.x + o.y * o.y - 0.3
    return step(a * a * a, o.x * o.x * o.y * o.y * o.y)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    return mix(tex_out(uv), tex_in(uv), in_heart(uv, float2(0.5, 0.4), t))
