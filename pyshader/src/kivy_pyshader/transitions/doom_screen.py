"""Doom screen

gl-transitions, Zeh Fernando, MIT.
"""
from pyshader import *

BARS = 40
AMPLITUDE = 1.0
NOISE = 0.5
FREQUENCY = 0.5
DRIP_SCALE = 0.5


def rand(num: float) -> float:
    return fract(mod(num * 67123.313, 12.0) * sin(num * 10.3) * cos(num))


def wave(num: float) -> float:
    fn = num * FREQUENCY * 0.1 * float(BARS)
    return cos(fn * 0.5) * cos(fn * 0.13) * sin((fn + 10.0) * 0.3) / 2.0 + 0.5


def drip(num: float) -> float:
    return sin(num / float(BARS - 1) * 3.141592) * DRIP_SCALE


def pos(num: float) -> float:
    w = wave(num) if NOISE == 0.0 else mix(wave(num), rand(num), NOISE)
    return w + (0.0 if DRIP_SCALE == 0.0 else drip(num))


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    bar = floor(uv.x * float(BARS))
    phase = t * (1.0 + pos(bar) * AMPLITUDE)
    if phase + uv.y < 1.0:
        return tex_out(float2(uv.x, uv.y + phase))
    return tex_in(uv)
