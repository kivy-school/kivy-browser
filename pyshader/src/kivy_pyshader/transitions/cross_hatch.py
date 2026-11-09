"""Cross hatch

gl-transitions, pthrasher, MIT.
"""
from pyshader import *

CENTER = float2(0.5)
THRESHOLD = 3.0
FADE_EDGE = 0.1


def rand(co: float2) -> float:
    return fract(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    dist = distance(CENTER, uv) / THRESHOLD
    r = t - min(rand(float2(uv.y, 0.0)), rand(float2(0.0, uv.x)))
    edge = mix(step(dist, r), 1.0, smoothstep(1.0 - FADE_EDGE, 1.0, t))
    return mix(tex_out(uv), tex_in(uv), mix(0.0, edge, smoothstep(0.0, FADE_EDGE, t)))
