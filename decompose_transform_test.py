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
        DecomposedTransform(0, 0, -math.pi, 1, 1, 0, 0, 0, 0),
        Transform(-1, 0, 0, -1, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, math.pi / 2, 1, 1, 0, 0, 0, 0),
        Transform(0, 1, -1, 0, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, 0, 1, 1, math.pi / 4, 0, 0, 0),
        Transform(1, 0, 1, 1, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, 0, 1, 1, 0, math.pi / 4, 0, 0),
        Transform(1, 1, 0, 1, 0, 0),
    ),
    (
        DecomposedTransform(0, 0, math.pi / 4, 1, 1, 0, 0, 0, 0),
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
        DecomposedTransform(0, 0, math.pi / 4, 2, 1, 0, 0, 0, 0),
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
        DecomposedTransform(100, 150, 0.1, 4, 3, 0.5, 0, 0, 0),
        Transform(
            3.980016661112103,
            0.3993336665873126,
            1.874792761644827,
            3.203169472169176,
            100.0,
            150.0,
        ),
    ),
]


@pytest.mark.parametrize("decomposed, composed", test_data)
def test_composeTransform(decomposed, composed):
    print(decomposed)
    t = composeTransform(**decomposed._asdict())
    assert transformEqual(composed, t), tuple(t)


@pytest.mark.parametrize("decomposed, composed", test_data)
def test_decomposeTransform(decomposed, composed):
    dec = decomposeTransform(composed)
    if decomposed.skewAngleY:
        # decomposition is ambiguous, and will prefer one with skewAngleY == 0
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
