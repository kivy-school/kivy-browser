"""LED ring button

A ring of dimly lit LEDs; a press sends a light once round it from the top,
each LED fading behind it. stdlib `light` (led, led_ring_index,
led_ring_position, tonemap_exposure).
"""
from pyshader import *
import pyshader.stdlib.fragment.light as light

from forms import within, panel

TAIL = 6.0


def main(uv: float2, resolution: float2, count: float, pressed: float, tint: float4) -> float4:
    p = within(uv, resolution)
    head = clamp(pressed, 0.0, 1.0) * (count + TAIL)
    i0 = light.led_ring_index(p, count)
    c = float3(0.0)
    for k in range(3):
        i = mod(i0 + float(k) - 1.0, count)
        # LED 0 is on +x, counting counterclockwise: from the top, clockwise.
        behind = head - mod(count * 0.25 - i, count)
        level = step(0.0, behind) * max(1.0 - behind / TAIL, 0.0)
        c += (0.1 + level * level) * light.led(p - light.led_ring_position(i, count, 0.36), tint.rgb, 0.02, 0.024)
    rgb = light.tonemap_exposure(c + float3(0.03, 0.035, 0.05), 1.3)
    return panel(uv, resolution, rgb, tint)
