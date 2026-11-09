"""Circle open

gl-transitions, gre, MIT.
"""
from pyshader import *

SMOOTHNESS = 0.3
OPENING = True
CENTER = float2(0.5, 0.5)
SQRT_2 = 1.414213562373


def main(uv: float2, t: float, tex_in: Texture, tex_out: Texture) -> float4:
    x = t if OPENING else 1.0 - t
    m = smoothstep(-SMOOTHNESS, 0.0, SQRT_2 * distance(CENTER, uv) - x * (1.0 + SMOOTHNESS))
    return mix(tex_out(uv), tex_in(uv), 1.0 - m if OPENING else m)
