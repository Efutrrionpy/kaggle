import numpy as np
import pytest

from rogii.ensemble import f57_blend


def test_f57_uses_frozen_weights() -> None:
    result = f57_blend([10.0, 20.0], [20.0, 30.0], [30.0, 40.0])
    np.testing.assert_allclose(result, [15.5, 25.5])


def test_f57_rejects_bad_components() -> None:
    with pytest.raises(ValueError):
        f57_blend([1.0], [1.0, 2.0], [1.0])
    with pytest.raises(ValueError):
        f57_blend([1.0], [np.nan], [1.0])
