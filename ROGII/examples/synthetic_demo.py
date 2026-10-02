"""Run the public reference pipeline without Kaggle competition data."""

from __future__ import annotations

import numpy as np

from rogii.alignment import ParticleFilterConfig, particle_filter_tvt
from rogii.ensemble import f57_blend
from rogii.metrics import rmse
from rogii.projection import project_stratigraphic_u
from rogii.validation import validate_native_mask


def main() -> None:
    rng = np.random.default_rng(7)
    typewell_tvt = np.linspace(980.0, 1040.0, 601)
    typewell_gr = 75 + 18 * np.sin(typewell_tvt / 2.7) + 8 * np.sin(typewell_tvt / 0.73)

    md = np.arange(140, dtype=np.float64)
    true_tvt = 998.0 + 0.16 * md + 0.7 * np.sin(md / 18.0)
    z = 11_200.0 - 0.11 * md + 0.15 * np.sin(md / 25.0)
    gr = np.interp(true_tvt, typewell_tvt, typewell_gr) + rng.normal(0, 2.0, len(md))
    gr[65:70] = np.nan

    tvt_input = np.full(len(md), np.nan)
    tvt_input[:45] = true_tvt[:45]
    boundary = validate_native_mask(tvt_input)

    pf = particle_filter_tvt(
        md=md,
        z=z,
        gr=gr,
        tvt_input=tvt_input,
        typewell_tvt=typewell_tvt,
        typewell_gr=typewell_gr,
        config=ParticleFilterConfig(n_particles=256, n_seeds=4),
    )
    projected_tail, _ = project_stratigraphic_u(
        pf[boundary.scored_slice],
        md[boundary.scored_slice],
        z[boundary.scored_slice],
        last_known_md=md[boundary.prediction_start - 1],
        last_known_tvt=tvt_input[boundary.prediction_start - 1],
        last_known_z=z[boundary.prediction_start - 1],
    )
    projected = pf.copy()
    projected[boundary.scored_slice] = projected_tail

    # The public repository omits production V71/HMM artifacts. Reusing the PF
    # path here demonstrates the fixed blend API; it is not a score reproduction.
    illustrative_blend = f57_blend(pf, projected, pf)
    truth = true_tvt[boundary.scored_slice]
    print(f"PF synthetic-tail RMSE:         {rmse(truth, pf[boundary.scored_slice]):.4f}")
    print(f"U-projected synthetic RMSE:     {rmse(truth, projected_tail):.4f}")
    print(
        "Illustrative fixed-blend RMSE: "
        f"{rmse(truth, illustrative_blend[boundary.scored_slice]):.4f}"
    )


if __name__ == "__main__":
    main()
