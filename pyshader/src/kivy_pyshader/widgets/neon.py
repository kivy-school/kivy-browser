"""Neon sign

A neon tube along a shape, lighting the brick wall it hangs on and
flickering like an old sign. Toggled, it stutters on and off; pressed, it
surges. stdlib `light` (neon, flicker, tonemap_aces).
"""
from pyshader import *
import pyshader.stdlib.fragment.light as light
from pyshader.stdlib.fragment.random import hash11

from forms import form, within, panel


def wall(p: float2) -> float3:
    row = floor(p.y * 10.0)
    brick = fract(float2(p.x * 5.0 + 0.5 * mod(row, 2.0), p.y * 10.0))
    mortar = step(0.06, brick.x) * step(0.1, brick.y)
    return float3(0.16, 0.1, 0.08) * (0.35 + 0.65 * mortar)


def main(uv: float2, time: float, resolution: float2, shape: float, morph: float, pressed: float,
         tint: float4) -> float4:
    p = within(uv, resolution)
    d = form(p, shape)
    seed = shape + tint.r * 7.0
    # Switching, the tube catches and drops out until it holds.
    lit = step(hash11(floor(time * 20.0) + seed * 13.0), clamp(morph, 0.0, 1.0))
    surge = 1.0 + 2.0 * (1.0 - clamp(pressed, 0.0, 1.0))
    c = light.neon(d, tint.rgb, 0.012, 0.03) * lit * surge * light.flicker(time, seed, 0.35)
    glass = tint.rgb * 0.25 * (1.0 - smoothstep(0.004, 0.008, abs(d)))
    rgb = light.tonemap_aces(wall(p) * (0.15 + 6.0 * c) + c + glass)
    return panel(uv, resolution, rgb, tint)
