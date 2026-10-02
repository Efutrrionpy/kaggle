"""Competition metric helpers.

The official score is pooled pointwise RMSE over every scored row. Averaging
per-well RMSE values would give short and long wells equal weight and is not
the competition metric.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import numpy.typing as npt

ArrayLike1D = Sequence[float] | npt.NDArray[np.generic]


def _finite_vector(values: ArrayLike1D, *, name: str) -> npt.NDArray[np.float64]:
    try:
        array = np.asarray(values, dtype=np.float64)
    except (TypeError, ValueError) as error:
        raise TypeError(f"{name} must contain numeric values") from error
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{name} must be a non-empty one-dimensional vector")
    if not np.isfinite(array).all():
        raise ValueError(f"{name} must contain only finite values")
    return array


def rmse(y_true: ArrayLike1D, y_pred: ArrayLike1D) -> float:
    """Return numerically stable pointwise RMSE."""

    actual = _finite_vector(y_true, name="y_true")
    predicted = _finite_vector(y_pred, name="y_pred")
    if actual.shape != predicted.shape:
        raise ValueError("y_true and y_pred must have identical shapes")

    absolute_error = np.abs(actual - predicted)
    scale = float(np.max(absolute_error))
    if scale == 0.0:
        return 0.0
    normalized = absolute_error / scale
    return float(scale * np.sqrt(np.mean(normalized * normalized)))
