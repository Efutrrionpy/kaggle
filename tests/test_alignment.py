import numpy as np

from rogii.alignment import ParticleFilterConfig, particle_filter_tvt


def _synthetic_inputs() -> dict[str, np.ndarray]:
    typewell_tvt = np.linspace(995.0, 1025.0, 301)
    typewell_gr = 70 + 15 * np.sin(typewell_tvt / 1.7)
    md = np.arange(70, dtype=np.float64)
    true_tvt = 1_000.0 + 0.15 * md
    z = 11_000.0 - 0.1 * md
    gr = np.interp(true_tvt, typewell_tvt, typewell_gr)
    tvt_input = np.full(len(md), np.nan)
    tvt_input[:25] = true_tvt[:25]
    return {
        "md": md,
        "z": z,
        "gr": gr,
        "tvt_input": tvt_input,
        "typewell_tvt": typewell_tvt,
        "typewell_gr": typewell_gr,
    }


def test_particle_filter_is_deterministic_finite_and_prefix_safe() -> None:
    inputs = _synthetic_inputs()
    config = ParticleFilterConfig(n_particles=32, n_seeds=2, observation_sigma=4.0)
    first = particle_filter_tvt(**inputs, config=config)
    second = particle_filter_tvt(**inputs, config=config)
    np.testing.assert_array_equal(first, second)
    np.testing.assert_array_equal(first[:25], inputs["tvt_input"][:25])
    assert np.isfinite(first).all()


def test_missing_horizontal_gr_has_a_finite_fallback() -> None:
    inputs = _synthetic_inputs()
    inputs["gr"][30:40] = np.nan
    result = particle_filter_tvt(
        **inputs,
        config=ParticleFilterConfig(n_particles=32, n_seeds=1, observation_sigma=4.0),
    )
    assert np.isfinite(result).all()
