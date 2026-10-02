"""Small, label-free regression checks for the frozen motion rule."""
import importlib.util
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from synthetic import run_fixtures

SPEC = importlib.util.spec_from_file_location(
    "overlay_numerical_tests", Path(__file__).parents[1] / "src/csv_overlay.py"
)
overlay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(overlay)


def test_support_boundary_occupied_parents_and_ties():
    report = run_fixtures(vars(overlay), scaling=False)
    assert report["status"] == "PASS_SYNTHETIC_INVARIANTS"
    assert report["cases"]["line-32x2"]["supported_queries"] == 0
    assert report["cases"]["line-33x2"]["supported_queries"] == 33


@pytest.mark.parametrize("kind", ["indegree", "outdegree", "dangling", "duplicate_nodes"])
def test_invalid_core_graph_is_rejected(kind):
    rows = [
        dict(row_type="node", node_id=i, t=int(i >= 3), z=0, y=0, x=i,
             source_id=-1, target_id=-1)
        for i in range(6)
    ]
    pairs = [(0, 3), (1, 3)] if kind == "indegree" else [(0, 3), (0, 4), (0, 5)]
    if kind == "dangling":
        pairs = [(99, 3)]
    if kind == "duplicate_nodes":
        rows[1]["node_id"] = 0
        pairs = [(0, 3)]
    rows.extend(dict(row_type="edge", node_id=-1, t=-1, z=-1, y=-1, x=-1,
                     source_id=p, target_id=c) for p, c in pairs)
    with pytest.raises(RuntimeError):
        overlay.motion_arrays("synthetic", pl.DataFrame(rows), overlay.FIXED_CONFIG)


def test_core_has_no_ground_truth_argument():
    import inspect
    assert list(inspect.signature(overlay.motion_arrays).parameters) == ["stem", "rows", "cfg"]
    assert list(inspect.signature(overlay.apply_motion_csv).parameters) == ["source", "destination"]
