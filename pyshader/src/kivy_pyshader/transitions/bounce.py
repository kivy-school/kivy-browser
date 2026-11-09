"""Bounce

gl-transitions, Adrian Purser, MIT.
"""
from pyshader import *

SHADOW_COLOUR = float4(0.0, 0.0, 0.0, 0.6)
SHADOW_HEIGHT = 0.075
BOUNCES = 3.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    stime = sin(t * PI / 2.0)
    phase = t * PI * BOUNCES
    y = abs(cos(phase)) * (1.0 - stime)
    d = uv.y - y
    fade = mix(d / SHADOW_HEIGHT * SHADOW_COLOUR.a + (1.0 - SHADOW_COLOUR.a), 1.0, smoothstep(0.95, 1.0, t))
    shadow = step(d, SHADOW_HEIGHT) * (1.0 - fade)
    return mix(mix(tex_in(uv), SHADOW_COLOUR, shadow), tex_out(float2(uv.x, uv.y + (1.0 - y))), step(d, 0.0))
