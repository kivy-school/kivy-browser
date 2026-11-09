"""Glitch displace

gl-transitions, Matt DesLauriers, MIT.
"""
from pyshader import *


def displace(tex: float4, coord: float2, dot_depth: float, texture_depth: float, strength: float) -> float2:
    dis = tex * dot_depth + 1.0 - tex * texture_depth
    dx = (dis.x - 1.0 + texture_depth * dot_depth) * strength
    dy = (dis.y - 1.0 + texture_depth * dot_depth) * strength
    return coord + float2(dx, dy)


def ease1(x: float) -> float:
    if x == 0.0 or x == 1.0:
        return x
    if x < 0.5:
        return 0.5 * pow(2.0, 20.0 * x - 10.0)
    return -0.5 * pow(2.0, 10.0 - x * 20.0) + 1.0


def ease2(x: float) -> float:
    return x if x == 1.0 else 1.0 - pow(2.0, -10.0 * x)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    color1 = tex_out(uv)
    color2 = tex_in(uv)
    d1 = tex_in(displace(color1, uv, 0.33, 0.7, 1.0 - ease1(t)))
    d2 = tex_out(displace(color2, uv, 0.33, 0.5, ease2(t)))
    gray = float3(dot(min(d2, d1).rgb, float3(0.299, 0.587, 0.114)))
    d2 = float4(gray, 1.0) * 2.0
    color1 = mix(color1, d2, smoothstep(0.0, 0.5, t))
    color2 = mix(color2, d1, smoothstep(1.0, 0.5, t))
    return mix(color1, color2, ease1(t))
