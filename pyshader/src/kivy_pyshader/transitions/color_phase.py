"""Color phase

gl-transitions, gre, MIT.
"""
from pyshader import *

FROM_STEP = float4(0.0, 0.2, 0.4, 0.0)
TO_STEP = float4(0.6, 0.8, 1.0, 1.0)


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    return mix(tex_out(uv), tex_in(uv), smoothstep(FROM_STEP, TO_STEP, float4(t)))
