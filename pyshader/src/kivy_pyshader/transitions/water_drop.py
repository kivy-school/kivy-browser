"""Water drop

gl-transitions, Paweł Płóciennik, MIT.
"""
from pyshader import *

AMPLITUDE = 30.0
SPEED = 30.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    direction = uv - float2(0.5)
    dist = length(direction)
    if dist > t:
        return mix(tex_out(uv), tex_in(uv), t)
    offset = direction * sin(dist * AMPLITUDE - t * SPEED)
    return mix(tex_out(uv + offset), tex_in(uv), t)
