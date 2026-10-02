import numpy as np
import pytest

from rogii.metrics import rmse


def test_rmse_matches_known_value() -> None:
    assert rmse([0.0, 0.0], [3.0, 4.0]) == pytest.approx(np.sqrt(12.5))


def test_rmse_rejects_nonfinite_and_misaligned_inputs() -> None:
    with pytest.raises(ValueError):
        rmse([1.0], [1.0, 2.0])
    with pytest.raises(ValueError):
        rmse([1.0, np.nan], [1.0, 2.0])


def test_rmse_handles_large_finite_residuals_without_square_overflow() -> None:
    result = rmse([0.0, 0.0], [1.0e200, 1.0e200])
    assert result == pytest.approx(1.0e200)
