"""Gear button

One more tooth on every press, back to the fewest after the most; the gear
turns a step as its teeth change. stdlib `gear`.
"""
from pyshader import *
from pyshader.stdlib.fragment.shapes import gear
from pyshader.stdlib.fragment.easing import back_out

from forms import centered


def turn(p: float2, angle: float) -> float2:
    c = cos(angle)
    s = sin(angle)
    return float2(c * p.x - s * p.y, s * p.x + c * p.y)


def main(uv: float2, resolution: float2, teeth: float, last_teeth: float, pressed: float, tint: float4) -> float4:
    p = centered(uv, resolution)
    k = back_out(pressed)
    q = turn(p, k * PI / teeth) + 0.5
    shape = mix(gear(q, float2(0.5), last_teeth, 0.46), gear(q, float2(0.5), teeth, 0.46), clamp(k, 0.0, 1.0))
    hole = 1.0 - smoothstep(0.09, 0.1, length(p))
    shade = 0.8 + 0.4 * (0.5 - length(p))
    return float4(tint.rgb * shade, tint.a * shape * (1.0 - hole))
