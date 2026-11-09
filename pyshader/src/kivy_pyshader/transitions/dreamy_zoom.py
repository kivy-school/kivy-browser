"""Dreamy zoom

gl-transitions, Zeh Fernando, MIT.
"""
from pyshader import *

DEG2RAD = 0.03926990816987241548078304229099
ROTATION = 6.0
SCALE = 1.2


def main(uv: float2, t: float, resolution: float2, tex_in: Texture, tex_out: Texture) -> float4:
    ratio = resolution.x / resolution.y
    first = t < 0.5
    phase = t * 2.0 if first else (t - 0.5) * 2.0
    offset = mix(0.0, ROTATION * DEG2RAD, phase) if first else mix(-ROTATION * DEG2RAD, 0.0, phase)
    scale = mix(1.0, SCALE, phase) if first else mix(SCALE, 1.0, phase)
    p = (uv - float2(0.5, 0.5)) / scale * float2(ratio, 1.0)
    angle = atan(p.y, p.x) + offset
    dist = length(p)
    p.x = cos(angle) * dist / ratio + 0.5
    p.y = sin(angle) * dist + 0.5
    c = tex_out(p) if first else tex_in(p)
    return c + (mix(0.0, 1.0, phase) if first else mix(1.0, 0.0, phase))
