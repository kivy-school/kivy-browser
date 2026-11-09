"""Page curl

KivyShaderTransitions, Shashi Ranjan, MIT.
"""
from pyshader import *

RADIUS = 0.1


def remap(value: float) -> float:
    return 0.075 + value * (-1.15 - 0.075)


def main(uv: float2, t: float, resolution: float2, tex_in: Texture, tex_out: Texture) -> float4:
    aspect = resolution.x / resolution.y
    direction = float2(0.5, -1.0)
    origin = float2(0.2, 0.0)
    dist = dot(uv - origin, direction) - remap(t)
    line = uv - dist * direction
    if dist > RADIUS:
        c = tex_in(uv)
        c.rgb *= pow(clamp(dist - RADIUS, 0.0, 1.0) * 1.5, 0.2)
        return c
    if dist >= 0.0:
        theta = asin(dist / RADIUS)
        p2 = line + direction * (PI - theta) * RADIUS
        p1 = line + direction * theta * RADIUS
        p = p2 if p2.x <= aspect and p2.y <= 1.0 and p2.x > 0.0 and p2.y > 0.0 else p1
        c = tex_out(p)
        c.rgb *= pow(clamp((RADIUS - dist) / RADIUS, 0.0, 1.0), 0.2)
        return c
    p = line + direction * (abs(dist) + PI * RADIUS)
    return tex_out(p if p.x <= aspect and p.y <= 1.0 and p.x > 0.0 and p.y > 0.0 else uv)
