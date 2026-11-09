"""Zoom in circles

gl-transitions, dycm8009, MIT.
"""
from pyshader import *


def zoom(p: float2, amount: float) -> float2:
    return 0.5 + (p - 0.5) * amount


def main(uv: float2, t: float, resolution: float2, tex_in: Texture, tex_out: Texture) -> float4:
    ratio = resolution.x / resolution.y
    r = 2.0 * ((uv - 0.5) * float2(1.0, 1.0 / ratio))
    pro = t / 0.8
    z = pro * 0.2
    k = 0.0
    if pro > 1.0:
        z = 0.2 + (pro - 1.0) * 5.0
        k = clamp((t - 0.8) / 0.07, 0.0, 1.0)
    p = uv
    d = length(r)
    if d >= 0.5 + z:
        if d < 0.8 + z * 1.5:
            p = zoom(uv, 1.0 - 0.15 * pro)
            k *= 0.5
        elif d < 1.2 + z * 2.5:
            p = zoom(uv, 1.0 - 0.2 * pro)
            k *= 0.2
        else:
            p = zoom(uv, 1.0 - 0.25 * pro)
    return mix(tex_out(p), tex_in(p), k)
