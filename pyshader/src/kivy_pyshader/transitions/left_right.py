"""Left right

gl-transitions, zhmy, MIT.
"""
from pyshader import *

BLACK = float4(0.0, 0.0, 0.0, 1.0)


def in_bounds(p: float2) -> bool:
    return all(float2(0.0) < p) and all(p < float2(1.0))


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    size = mix(1.0, 3.0, t * 0.2)
    spto = (uv - 0.5) * size + 0.5
    spfr = uv - float2(1.0 - t, 0.0)
    if in_bounds(spfr):
        return tex_in(spfr)
    if in_bounds(spto):
        return tex_out(spto) * (1.0 - t)
    return BLACK
