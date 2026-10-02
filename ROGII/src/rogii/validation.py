"""Leakage-resistant validation primitives for complete wells."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from rogii.metrics import rmse


@dataclass(frozen=True, slots=True)
class MaskBoundary:
    """Known-prefix and hidden-tail boundary for one well."""

    n_rows: int
    prediction_start: int

    @property
    def known_slice(self) -> slice:
        return slice(0, self.prediction_start)

    @property
    def scored_slice(self) -> slice:
        return slice(self.prediction_start, self.n_rows)

    @property
    def n_scored_rows(self) -> int:
        return self.n_rows - self.prediction_start


@dataclass(frozen=True, slots=True)
class ScoreDiagnostics:
    """Official score and softer per-well robustness diagnostics."""

    pooled_rmse: float
    median_well_rmse: float
    p90_well_rmse: float
    worst_well_rmse: float
    n_scored_rows: int
    n_wells: int


def validate_native_mask(tvt_input: npt.ArrayLike) -> MaskBoundary:
    """Validate that TVT_input is a finite prefix followed by a missing tail."""

    values = np.asarray(tvt_input, dtype=np.float64)
    if values.ndim != 1 or values.size < 2:
        raise ValueError("TVT_input must be a one-dimensional sequence with at least two rows")
    known = np.isfinite(values)
    if not known.any():
        raise ValueError("TVT_input has no known prefix")
    if known.all():
        raise ValueError("TVT_input has no scored tail")

    prediction_start = int(np.flatnonzero(~known)[0])
    if known[prediction_start:].any():
        raise ValueError("TVT_input must be one contiguous known prefix")
    return MaskBoundary(n_rows=len(values), prediction_start=prediction_start)


def balanced_well_folds(
    well_ids: npt.ArrayLike,
    scored_rows: npt.ArrayLike,
    *,
    n_splits: int = 5,
    seed: int = 20260714,
) -> dict[str, int]:
    """Assign complete wells to folds while balancing scored-row load.

    This function is target-free: only well identity and the number of rows
    that will be scored are allowed to influence the assignment.
    """

    wells = np.asarray(well_ids, dtype=str)
    loads = np.asarray(scored_rows, dtype=np.int64)
    if wells.ndim != 1 or loads.shape != wells.shape or len(wells) < n_splits:
        raise ValueError("well_ids and scored_rows must be aligned vectors with enough wells")
    if len(np.unique(wells)) != len(wells):
        raise ValueError("well_ids must be unique")
    if n_splits < 2 or (loads <= 0).any():
        raise ValueError("n_splits must be at least two and scored_rows must be positive")

    rng = np.random.default_rng(seed)
    tie_break = rng.random(len(wells))
    order = np.lexsort((tie_break, -loads))
    fold_load = np.zeros(n_splits, dtype=np.int64)
    fold_count = np.zeros(n_splits, dtype=np.int64)
    assignment: dict[str, int] = {}

    for index in order:
        # Primary objective: scored-row balance. Count breaks exact ties.
        fold = min(range(n_splits), key=lambda value: (fold_load[value], fold_count[value], value))
        assignment[str(wells[index])] = fold
        fold_load[fold] += int(loads[index])
        fold_count[fold] += 1
    return assignment


def assert_complete_well_oof(
    well_ids: npt.ArrayLike,
    fold_ids: npt.ArrayLike,
) -> None:
    """Fail if rows from one well appear under more than one OOF fold."""

    wells = np.asarray(well_ids, dtype=str)
    folds = np.asarray(fold_ids, dtype=np.int64)
    if wells.ndim != 1 or folds.shape != wells.shape or len(wells) == 0:
        raise ValueError("well_ids and fold_ids must be aligned non-empty vectors")
    for well in np.unique(wells):
        if len(np.unique(folds[wells == well])) != 1:
            raise ValueError(f"well {well!r} crosses OOF folds")


def validate_oof_alignment(
    expected_row_ids: npt.ArrayLike,
    predicted_row_ids: npt.ArrayLike,
    predictions: npt.ArrayLike,
) -> npt.NDArray[np.float64]:
    """Require exact row identity, order, uniqueness, coverage and finiteness."""

    expected = np.asarray(expected_row_ids, dtype=str)
    observed = np.asarray(predicted_row_ids, dtype=str)
    values = np.asarray(predictions, dtype=np.float64)
    if expected.ndim != 1 or observed.shape != expected.shape or values.shape != expected.shape:
        raise ValueError("OOF row IDs and predictions must have identical one-dimensional shapes")
    if len(np.unique(expected)) != len(expected) or len(np.unique(observed)) != len(observed):
        raise ValueError("OOF row IDs must be unique")
    if not np.array_equal(expected, observed):
        raise ValueError("OOF row identity or order does not match the scoring frame")
    if not np.isfinite(values).all():
        raise ValueError("OOF predictions must be finite")
    return values


def score_by_well(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    well_ids: npt.ArrayLike,
) -> ScoreDiagnostics:
    """Compute pooled RMSE plus per-well diagnostics."""

    actual = np.asarray(y_true, dtype=np.float64)
    predicted = np.asarray(y_pred, dtype=np.float64)
    wells = np.asarray(well_ids, dtype=str)
    if actual.ndim != 1 or predicted.shape != actual.shape or wells.shape != actual.shape:
        raise ValueError("truth, predictions and well IDs must be aligned vectors")

    per_well = np.asarray(
        [rmse(actual[wells == well], predicted[wells == well]) for well in np.unique(wells)]
    )
    return ScoreDiagnostics(
        pooled_rmse=rmse(actual, predicted),
        median_well_rmse=float(np.median(per_well)),
        p90_well_rmse=float(np.quantile(per_well, 0.9)),
        worst_well_rmse=float(np.max(per_well)),
        n_scored_rows=len(actual),
        n_wells=len(per_well),
    )
