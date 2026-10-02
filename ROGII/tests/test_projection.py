import numpy as np

from rogii.projection import project_stratigraphic_u, robust_polynomial_values


def test_robust_polynomial_preserves_short_vectors() -> None:
    values = np.asarray([1.0, 2.0, 4.0])
    np.testing.assert_array_equal(robust_polynomial_values([0.0, 0.5, 1.0], values), values)


def test_projection_is_finite_and_respects_weight_endpoints() -> None:
    md = np.arange(10.0, 20.0)
    z = 11_000.0 - 0.1 * md
    base = 1_000.0 + 0.2 * md + np.asarray([0, 0, 0, 8, 0, 0, 0, 0, 0, 0])

    unchanged, projected = project_stratigraphic_u(
        base,
        md,
        z,
        last_known_md=9.0,
        last_known_tvt=1_001.8,
        last_known_z=10_999.1,
        projection_weight=0.0,
    )
    np.testing.assert_allclose(unchanged, base)
    assert np.isfinite(projected).all()

    full, projected_again = project_stratigraphic_u(
        base,
        md,
        z,
        last_known_md=9.0,
        last_known_tvt=1_001.8,
        last_known_z=10_999.1,
        projection_weight=1.0,
    )
    np.testing.assert_allclose(full, projected_again)
    assert abs(full[3] - np.median(full)) < abs(base[3] - np.median(base))
