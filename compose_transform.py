from typing import NamedTuple
import math
from fontTools.misc.transform import Transform


class DecomposedTransform(NamedTuple):
    x: float
    y: float
    rotation: float
    scaleX: float
    scaleY: float
    skewX: float
    skewY: float
    tCenterX: float
    tCenterY: float


def composeTransform(
    x: float,
    y: float,
    rotation: float,
    scaleX: float,
    scaleY: float,
    skewX: float,
    skewY: float,
    tCenterX: float,
    tCenterY: float,
) -> Transform:
    """Compose a decomposed transform into an Affine transform."""
    t = Transform()
    t = t.translate(tCenterX, tCenterY)
    t = t.translate(x, y)
    t = t.rotate(math.radians(rotation))
    t = t.scale(scaleX, scaleY)
    t = t.skew(-math.radians(skewX), math.radians(skewY))
    t = t.translate(-tCenterX, -tCenterY)
    return t


def decomposeTransform(transform: Transform) -> DecomposedTransform:
    """Decompose an Affine transformation matrix into components."""
    # Adapted from an answer on
    # https://math.stackexchange.com/questions/13150/extracting-rotation-scale-values-from-2d-transformation-matrix
    a, b, c, d, x, y = transform
    delta = a * d - b * c

    rotation = 0
    scaleX = scaleY = 0
    skewX = skewY = 0

    # Apply the QR-like decomposition.
    if a != 0 or b != 0:
        r = math.sqrt(a * a + b * b)
        rotation = math.acos(a / r) if b > 0 else -math.acos(a / r)
        scaleX, scaleY = (r, delta / r)
        skewX, skewY = (math.atan((a * c + b * d) / (r * r)), 0)
    elif c != 0 or d != 0:
        s = math.sqrt(c * c + d * d)
        rotation = math.pi / 2 - (
            math.acos(-c / s) if d > 0 else -math.acos(c / s)
        )
        scaleX, scaleY = (delta / s, s)
        skewX, skewY = (0, math.atan((a * c + b * d) / (s * s)))
    else:
        # a = b = c = d = 0
        pass

    return DecomposedTransform(
        x,
        y,
        math.degrees(rotation),
        scaleX,
        scaleY,
        -math.degrees(skewX),
        math.degrees(skewY),
        0,
        0,
    )
