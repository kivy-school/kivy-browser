"""Butterfly wave scrawler

gl-transitions, mandubian, MIT.
"""
from pyshader import *

AMPLITUDE = 1.0
WAVES = 30.0
COLOR_SEPARATION = 0.3


def compute(p: float2, progress: float, center: float2) -> float:
    o = p * sin(progress * AMPLITUDE) - center
    theta = acos(dot(o, float2(1.0, 0.0))) * WAVES
    return (exp(cos(theta)) - 2.0 * cos(4.0 * theta) + pow(sin((2.0 * theta - PI) / 24.0), 5.0)) / 10.0


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    inv = 1.0 - t
    disp = compute(uv, t, float2(0.5, 0.5))
    incoming = tex_in(uv + inv * disp)
    outgoing = float4(tex_out(uv + t * disp * (1.0 - COLOR_SEPARATION)).r,
                      tex_out(uv + t * disp).g,
                      tex_out(uv + t * disp * (1.0 + COLOR_SEPARATION)).b, 1.0)
    return incoming * t + outgoing * inv
