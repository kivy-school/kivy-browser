"""Window blinds

gl-transitions, Fabien Benetou, MIT.
"""
from pyshader import *


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    k = t
    if mod(floor(uv.y * 100.0 * t), 2.0) == 0.0:
        k *= 2.0 - 0.5
    return mix(tex_out(uv), tex_in(uv), mix(k, t, smoothstep(0.8, 1.0, t)))
