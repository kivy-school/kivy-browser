"""Fly eye

gl-transitions, gre, MIT.
"""
from pyshader import *

SIZE = 0.04
ZOOM = 50.0
COLOR_SEPARATION = 0.3


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    inv = 1.0 - t
    disp = SIZE * float2(cos(ZOOM * uv.x), sin(ZOOM * uv.y))
    incoming = tex_in(uv + inv * disp)
    outgoing = float4(tex_out(uv + t * disp * (1.0 - COLOR_SEPARATION)).r,
                      tex_out(uv + t * disp).g,
                      tex_out(uv + t * disp * (1.0 + COLOR_SEPARATION)).b, 1.0)
    return incoming * t + outgoing * inv
