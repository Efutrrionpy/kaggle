"""Target-free robust projection in the physical U = TVT + Z coordinate."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]


def robust_polynomial_values(
    x: npt.ArrayLike,
    y: npt.ArrayLike,
    *,
    degree: int = 4,
    iterations: int = 4,
) -> FloatArray:
    """Fit an iteratively reweighted polynomial and return fitted values."""

    xx = np.asarray(x, dtype=np.float64)
    yy = np.asarray(y, dtype=np.float64)
    if xx.ndim != 1 or yy.shape != xx.shape or len(xx) == 0:
        raise ValueError("x and y must be aligned non-empty vectors")
    if not np.isfinite(xx).all() or not np.isfinite(yy).all():
        raise ValueError("x and y must be finite")
    if degree < 0 or iterations < 0:
        raise ValueError("degree and iterations must be non-negative")
    if len(xx) < degree + 2:
        return yy.copy()

    coefficients = np.polyfit(xx, yy, degree)
    for _ in range(iterations):
        residual = yy - np.polyval(coefficients, xx)
        scale = float(np.median(np.abs(residual)) * 1.4826 + 1.0e-6)
        weights = 1.0 / (1.0 + np.square(residual / (2.0 * scale)))
        coefficients = np.polyfit(xx, yy, degree, w=weights)
    return np.polyval(coefficients, xx).astype(np.float64)


def project_stratigraphic_u(
    base_tvt: npt.ArrayLike,
    md: npt.ArrayLike,
    z: npt.ArrayLike,
    *,
    last_known_md: float,
    last_known_tvt: float,
    last_known_z: float,
    degree: int = 4,
    iterations: int = 4,
    projection_weight: float = 0.75,
) -> tuple[FloatArray, FloatArray]:
    """Smooth one hidden-tail prediction in U-space and convert it back to TVT."""

    base = np.asarray(base_tvt, dtype=np.float64)
    md_values = np.asarray(md, dtype=np.float64)
    z_values = np.asarray(z, dtype=np.float64)
    if base.ndim != 1 or md_values.shape != base.shape or z_values.shape != base.shape:
        raise ValueError("base_tvt, md and z must be aligned one-dimensional vectors")
    if len(base) == 0 or not np.isfinite(np.c_[base, md_values, z_values]).all():
        raise ValueError("base_tvt, md and z must be non-empty and finite")
    if not 0.0 <= projection_weight <= 1.0:
        raise ValueError("projection_weight must be in [0, 1]")

    anchors = np.asarray([last_known_md, last_known_tvt, last_known_z], dtype=np.float64)
    if not np.isfinite(anchors).all():
        raise ValueError("last-known anchor must be finite")

    horizon = max(float(md_values[-1] - last_known_md), 1.0e-6)
    normalized_md = (md_values - last_known_md) / horizon
    anchor_u = last_known_tvt + last_known_z
    delta_u = base + z_values - anchor_u
    fitted_delta_u = robust_polynomial_values(
        normalized_md,
        delta_u,
        degree=degree,
        iterations=iterations,
    )
    projected = anchor_u + fitted_delta_u - z_values
    candidate = (1.0 - projection_weight) * base + projection_weight * projected
    if not np.isfinite(candidate).all():
        raise ValueError("projection produced non-finite predictions")
    return candidate, projected
