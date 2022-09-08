from typing import NamedTuple
import math
from fontTools.misc.transform import Transform


class DecomposedTransform(NamedTuple):
    x: float
    y: float
    rotationAngle: float
    scaleX: float
    scaleY: float
    skewAngleX: float
    skewAngleY: float
    transformationCenterX: float
    transformationCenterY: float


def composeTransform(
    x: float,
    y: float,
    rotationAngle: float,
    scaleX: float,
    scaleY: float,
    skewAngleX: float,
    skewAngleY: float,
    transformationCenterX: float,
    transformationCenterY: float,
) -> Transform:
    """Compose a decomposed transform into an Affine transform."""
    t = Transform()
    t = t.translate(x + transformationCenterX, y + transformationCenterY)
    t = t.rotate(rotationAngle)
    t = t.scale(scaleX, scaleY)
    t = t.skew(skewAngleX, skewAngleY)
    t = t.translate(-transformationCenterX, -transformationCenterY)
    return t


def decomposeTransform(transform: Transform) -> DecomposedTransform:
    """Decompose an Affine transformation matrix into components."""
    a, b, c, d, x, y = transform
    delta = a * d - b * c

    rotationAngle = 0
    scaleX = scaleY = 0
    skewAngleX = skewAngleY = 0

    # Apply the QR-like decomposition.
    if a != 0 or b != 0:
        r = math.sqrt(a * a + b * b)
        rotationAngle = math.acos(a / r) if b > 0 else -math.acos(a / r)
        scaleX, scaleY = (r, delta / r)
        skewAngleX, skewAngleY = (math.atan((a * c + b * d) / (r * r)), 0)
    elif c != 0 or d != 0:
        s = math.sqrt(c * c + d * d)
        rotationAngle = math.pi / 2 - (
            math.acos(-c / s) if d > 0 else -math.acos(c / s)
        )
        scaleX, scaleY = (delta / s, s)
        skewAngleX, skewAngleY = (0, math.atan((a * c + b * d) / (s * s)))
    else:
        # a = b = c = d = 0
        pass

    return DecomposedTransform(
        x, y, rotationAngle, scaleX, scaleY, skewAngleX, skewAngleY, 0, 0
    )
