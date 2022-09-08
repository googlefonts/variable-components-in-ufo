import math
from fontTools.misc.transform import Transform
import pytest
from decompose_transform import (
    composeTransform,
    decomposeTransform,
    DecomposedTransform,
)


def transformEqual(t1, t2):
    return all(math.isclose(v1, v2, abs_tol=1e-09) for v1, v2 in zip(t1, t2))


def decomposedTransformEqual(t1, t2):
    return all(
        math.isclose(v1, v2, abs_tol=1e-09)
        for v1, v2 in zip(t1._asdict().values(), t2._asdict().values())
    )


test_data = [
    (
        DecomposedTransform(0, 0, 0, 1, 1, 0, 0, 0, 0),
        Transform(1, 0, 0, 1, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, 0, 2, 1, 0, 0, 1, 0),
        Transform(2, 0, 0, 1, -1, 0),
    ),
    (
        DecomposedTransform(0, 0, 0, 2, 1, 0, 0, 0, 1),
        Transform(2, 0, 0, 1, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, 0, 1, 2, 0, 0, 0, 1),
        Transform(1, 0, 0, 2, 0, -1),
    ),
    (
        DecomposedTransform(0, 0, -180, 1, 1, 0, 0, 0, 0),
        Transform(-1, 0, 0, -1, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, 90, 1, 1, 0, 0, 0, 0),
        Transform(0, 1, -1, 0, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, 0, 1, 1, 45, 0, 0, 0),
        Transform(1, 0, -1, 1, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, 0, 1, 1, 0, 45, 0, 0),
        Transform(1, 1, 0, 1, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, 45, 1, 1, 0, 0, 0, 0),
        Transform(
            0.7071067811865476,
            0.7071067811865475,
            -0.7071067811865475,
            0.7071067811865476,
            0.0,
            0.0,
        ),
    ),
    (
        DecomposedTransform(0, 0, 45, 2, 1, 0, 0, 0, 0),
        Transform(
            1.4142135623730951,
            1.414213562373095,
            -0.7071067811865475,
            0.7071067811865476,
            0.0,
            0.0,
        ),
    ),
    (
        DecomposedTransform(100, 150, 5, 4, 3, 20, 0, 0, 0),
        Transform(
            3.984778792366982,
            0.34862297099063266,
            -1.71180809879978,
            2.8616957098531968,
            100.0,
            150.0,
        ),
    ),
]


@pytest.mark.parametrize("decomposed, composed", test_data)
def test_composeTransform(decomposed, composed):
    t = composeTransform(**decomposed._asdict())
    assert transformEqual(composed, t), tuple(t)


@pytest.mark.parametrize("decomposed, composed", test_data)
def test_decomposeTransform(decomposed, composed):
    dec = decomposeTransform(composed)
    if (
        decomposed.skewAngleY
        or decomposed.transformationCenterX
        or decomposed.transformationCenterY
    ):
        # decomposition can be done multiple ways:
        # 1. it will prefer skewAngleY == 0
        # 2. transformationCenterX and transformationCenterY are lost
        assert not decomposedTransformEqual(decomposed, dec)
    else:
        assert decomposedTransformEqual(decomposed, dec)


@pytest.mark.parametrize("decomposed, composed", test_data)
def test_compose_decompose(decomposed, composed):
    t1 = composeTransform(**decomposed._asdict())
    dec = decomposeTransform(t1)
    t2 = composeTransform(**dec._asdict())
    assert transformEqual(t1, t2)
    assert transformEqual(composed, t1)
    assert transformEqual(composed, t2)
