import numpy as np
import pytest

from rogii.validation import (
    assert_complete_well_oof,
    balanced_well_folds,
    score_by_well,
    validate_native_mask,
    validate_oof_alignment,
)


def test_native_mask_requires_one_contiguous_prefix() -> None:
    boundary = validate_native_mask([100.0, 101.0, np.nan, np.nan])
    assert boundary.prediction_start == 2
    assert boundary.n_scored_rows == 2

    with pytest.raises(ValueError, match="contiguous"):
        validate_native_mask([100.0, np.nan, 102.0, np.nan])


def test_fold_assignment_is_deterministic_and_complete() -> None:
    wells = np.asarray([f"well-{index}" for index in range(15)])
    rows = np.asarray([100, 80, 70, 60, 50] * 3)
    first = balanced_well_folds(wells, rows, n_splits=5)
    second = balanced_well_folds(wells, rows, n_splits=5)
    assert first == second
    assert set(first) == set(wells)
    assert set(first.values()) == set(range(5))


def test_complete_well_oof_rejects_split_well() -> None:
    assert_complete_well_oof(["a", "a", "b"], [0, 0, 1])
    with pytest.raises(ValueError, match="crosses"):
        assert_complete_well_oof(["a", "a", "b"], [0, 1, 1])


def test_oof_alignment_is_exact_and_finite() -> None:
    values = validate_oof_alignment(["a_0", "b_0"], ["a_0", "b_0"], [1.0, 2.0])
    np.testing.assert_array_equal(values, [1.0, 2.0])
    with pytest.raises(ValueError, match="identity"):
        validate_oof_alignment(["a_0", "b_0"], ["b_0", "a_0"], [2.0, 1.0])


def test_pooled_score_differs_from_equal_weight_per_well_average() -> None:
    truth = np.zeros(5)
    prediction = np.asarray([10.0, 0.0, 0.0, 0.0, 0.0])
    wells = np.asarray(["short", "long", "long", "long", "long"])
    diagnostics = score_by_well(truth, prediction, wells)
    assert diagnostics.pooled_rmse == pytest.approx(np.sqrt(20.0))
    assert diagnostics.median_well_rmse == pytest.approx(5.0)
