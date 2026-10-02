"""Fixed model composition used by the final F57 candidate."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def f57_blend(
    v71_tvt: npt.ArrayLike,
    u_projection_tvt: npt.ArrayLike,
    raw_hmm_tvt: npt.ArrayLike,
) -> npt.NDArray[np.float64]:
    """Return F57 = 0.50 V71 + 0.45 U-projection + 0.05 raw HMM.

    The weights were frozen before Private evaluation. This helper publishes
    the composition, not the omitted production CatBoost weights or artifacts.
    """

    components = [
        np.asarray(v71_tvt, dtype=np.float64),
        np.asarray(u_projection_tvt, dtype=np.float64),
        np.asarray(raw_hmm_tvt, dtype=np.float64),
    ]
    if any(component.ndim != 1 for component in components):
        raise ValueError("all F57 components must be one-dimensional")
    if len({component.shape for component in components}) != 1 or not len(components[0]):
        raise ValueError("all F57 components must be aligned non-empty vectors")
    if not all(np.isfinite(component).all() for component in components):
        raise ValueError("all F57 components must be finite")
    return 0.50 * components[0] + 0.45 * components[1] + 0.05 * components[2]
