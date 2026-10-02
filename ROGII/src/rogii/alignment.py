"""Inference-legal Gamma Ray/typewell particle-filter alignment.

This is a compact reference implementation of the mechanism used during the
project. The production version used a larger multi-seed feature bank and
compiled kernels; this version favors readability and a synthetic-data demo.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from rogii.validation import validate_native_mask


@dataclass(frozen=True, slots=True)
class ParticleFilterConfig:
    """Particle-filter hyperparameters."""

    n_particles: int = 256
    n_seeds: int = 4
    seed: int = 20260714
    initial_u_spread: float = 4.5
    momentum: float = 0.998
    rate_noise: float = 0.002
    position_noise: float = 0.02
    resample_position_noise: float = 0.10
    resample_rate_noise: float = 0.001
    resample_fraction: float = 0.5
    observation_sigma: float | None = None

    def __post_init__(self) -> None:
        if self.n_particles < 16 or self.n_seeds < 1:
            raise ValueError("n_particles must be at least 16 and n_seeds must be positive")
        if self.initial_u_spread < 0 or self.rate_noise < 0 or self.position_noise < 0:
            raise ValueError("noise and spread values must be non-negative")
        if not 0.0 < self.resample_fraction <= 1.0:
            raise ValueError("resample_fraction must be in (0, 1]")
        if self.observation_sigma is not None and self.observation_sigma <= 0:
            raise ValueError("observation_sigma must be positive")


def _vector(values: npt.ArrayLike, *, name: str, allow_nan: bool = False) -> np.ndarray:
    result = np.asarray(values, dtype=np.float64)
    if result.ndim != 1 or len(result) == 0:
        raise ValueError(f"{name} must be a non-empty vector")
    if allow_nan:
        if np.isinf(result).any():
            raise ValueError(f"{name} must not contain infinity")
    elif not np.isfinite(result).all():
        raise ValueError(f"{name} must be finite")
    return result


def _prepare_typewell(
    tvt: npt.ArrayLike,
    gr: npt.ArrayLike,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    tvt_values = _vector(tvt, name="typewell_tvt", allow_nan=True)
    gr_values = _vector(gr, name="typewell_gr", allow_nan=True)
    if gr_values.shape != tvt_values.shape:
        raise ValueError("typewell_tvt and typewell_gr must be aligned")
    valid = np.isfinite(tvt_values) & np.isfinite(gr_values)
    if valid.sum() < 10:
        raise ValueError("the typewell needs at least ten finite rows")

    order = np.argsort(tvt_values[valid], kind="stable")
    sorted_tvt = tvt_values[valid][order]
    sorted_gr = gr_values[valid][order]
    unique_tvt, inverse = np.unique(sorted_tvt, return_inverse=True)
    if len(unique_tvt) != len(sorted_tvt):
        sums = np.bincount(inverse, weights=sorted_gr)
        counts = np.bincount(inverse)
        sorted_gr = sums / counts
        sorted_tvt = unique_tvt
    return sorted_tvt, sorted_gr


def _fill_missing(values: np.ndarray, *, fallback: float) -> np.ndarray:
    result = values.copy()
    finite = np.isfinite(result)
    if not finite.any():
        result.fill(fallback)
        return result
    rows = np.arange(len(result), dtype=np.float64)
    result[~finite] = np.interp(rows[~finite], rows[finite], result[finite])
    return result


def _initial_u_rate(md: np.ndarray, z: np.ndarray, tvt_input: np.ndarray, stop: int) -> float:
    start = max(0, stop - 30)
    delta_md = np.diff(md[start:stop])
    delta_u = np.diff(tvt_input[start:stop] + z[start:stop])
    valid = np.isfinite(delta_md) & np.isfinite(delta_u) & (delta_md > 0)
    return float(np.median(delta_u[valid] / delta_md[valid])) if valid.sum() >= 3 else 0.0


def _systematic_resample(weights: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    positions = (rng.random() + np.arange(len(weights))) / len(weights)
    return np.searchsorted(np.cumsum(weights), positions, side="left")


def particle_filter_tvt(
    *,
    md: npt.ArrayLike,
    z: npt.ArrayLike,
    gr: npt.ArrayLike,
    tvt_input: npt.ArrayLike,
    typewell_tvt: npt.ArrayLike,
    typewell_gr: npt.ArrayLike,
    config: ParticleFilterConfig | None = None,
) -> npt.NDArray[np.float64]:
    """Predict the hidden TVT tail using only inference-time information.

    Particles track ``U = TVT + Z`` while the observation likelihood compares
    horizontal-well GR with typewell GR in TVT space. Known prefix values are
    copied exactly into the returned vector.
    """

    config = config or ParticleFilterConfig()
    md_values = _vector(md, name="md")
    z_values = _vector(z, name="z")
    gr_values = _vector(gr, name="gr", allow_nan=True)
    inputs = _vector(tvt_input, name="tvt_input", allow_nan=True)
    if not (md_values.shape == z_values.shape == gr_values.shape == inputs.shape):
        raise ValueError("horizontal-well inputs must be aligned")
    if not (np.diff(md_values) > 0).all():
        raise ValueError("md must be strictly increasing")

    boundary = validate_native_mask(inputs)
    reference_tvt, reference_gr = _prepare_typewell(typewell_tvt, typewell_gr)
    horizontal_gr = _fill_missing(gr_values, fallback=float(np.mean(reference_gr)))

    prefix_expected = np.interp(inputs[boundary.known_slice], reference_tvt, reference_gr)
    prefix_residual = horizontal_gr[boundary.known_slice] - prefix_expected
    sigma = config.observation_sigma
    if sigma is None:
        robust_sigma = 1.4826 * float(
            np.median(np.abs(prefix_residual - np.median(prefix_residual)))
        )
        sigma = float(np.clip(robust_sigma, 10.0, 60.0))

    initial_u = float(
        inputs[boundary.prediction_start - 1] + z_values[boundary.prediction_start - 1]
    )
    initial_rate = _initial_u_rate(md_values, z_values, inputs, boundary.prediction_start)
    seed_predictions = np.empty((config.n_seeds, boundary.n_scored_rows), dtype=np.float64)

    for seed_index in range(config.n_seeds):
        rng = np.random.default_rng(config.seed + seed_index)
        position_u = initial_u + config.initial_u_spread * rng.standard_normal(config.n_particles)
        rate_u = initial_rate + 0.01 * rng.standard_normal(config.n_particles)
        weights = np.full(config.n_particles, 1.0 / config.n_particles)
        previous_md = float(md_values[boundary.prediction_start - 1])

        for output_index, row in enumerate(range(boundary.prediction_start, len(md_values))):
            md_step = max(float(md_values[row] - previous_md), 1.0e-6)
            rate_u = config.momentum * rate_u + config.rate_noise * rng.standard_normal(
                config.n_particles
            )
            position_u += rate_u * md_step + config.position_noise * rng.standard_normal(
                config.n_particles
            )

            particle_tvt = position_u - z_values[row]
            particle_tvt = np.clip(particle_tvt, reference_tvt[0] - 100, reference_tvt[-1] + 100)
            position_u = particle_tvt + z_values[row]
            expected_gr = np.interp(particle_tvt, reference_tvt, reference_gr)
            standardized = (horizontal_gr[row] - expected_gr) / sigma
            log_weight = -0.5 * np.minimum(standardized * standardized, 600.0)
            log_weight -= np.max(log_weight)
            weights *= np.exp(log_weight)
            weight_sum = float(np.sum(weights))
            weights = (
                weights / weight_sum if weight_sum > 0 else np.full_like(weights, 1 / len(weights))
            )

            seed_predictions[seed_index, output_index] = float(np.sum(weights * particle_tvt))
            effective_n = 1.0 / float(np.sum(weights * weights))
            if effective_n < config.resample_fraction * config.n_particles:
                selected = _systematic_resample(weights, rng)
                position_u = position_u[
                    selected
                ] + config.resample_position_noise * rng.standard_normal(config.n_particles)
                rate_u = rate_u[selected] + config.resample_rate_noise * rng.standard_normal(
                    config.n_particles
                )
                weights.fill(1.0 / config.n_particles)
            previous_md = float(md_values[row])

    prediction = inputs.copy()
    prediction[boundary.scored_slice] = np.mean(seed_predictions, axis=0)
    if not np.isfinite(prediction).all():
        raise ValueError("particle filter produced non-finite predictions")
    return prediction
