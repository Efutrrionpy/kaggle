# Kaggle Research Reports

Three applied research studies in geological sequence prediction, cell tracking,
and competitive resource management.

| Competition | Principal models and methods | Competition result |
|---|---|---|
| [ROGII — Wellbore Geology Prediction](ROGII/README.md) | CatBoost, Particle Filter / HMM alignment, robust stratigraphic projection | **Private RMSE 8.889 · 444 / 6,191 · Bronze** |
| [Biohub — Cell Tracking during Development](Biohub/README.md) | Temporal 3D U-Nets, node Transformers, DeepCenter, ILP tracking, collective-motion refinement | **Best selected Private score 0.91051 · 1,714 / 4,020** |
| [Kaggriculture](Kaggriculture/README.md) | Demonstration-derived policies, state-conditioned economic routing, resource-constrained service planning | **Public ratings 2409.8 / 2163.7; final ranking pending**¹ |

## Research findings

**ROGII:** Combining a 290-feature CatBoost model with physical path smoothing
and HMM alignment reduced the final internal estimate to 8.5186 RMSE. The
Private result favored this ensemble over a candidate with a better Public score.

**Biohub:** Learned spatiotemporal features supported a deployable tracking
pipeline. NCC, learned division residuals, five-frame encoders, and
self-supervised features were evaluated; improvements in local objectives did
not consistently improve complete tracking graphs or official scores.

**Kaggriculture:** Full production programs with current-state material and
cash-flow feedback outperformed narrower market selectors in local comparisons.
The submitted FlexService policy scored 677 / 768 points on a prospective
world/opponent/seat panel, against 622 for AdaptiveMilk on that same panel.

Each report describes the models, evaluation protocol, experimental results,
and reproducibility scope. Official results and local estimates are reported
separately; scores from different competitions or validation panels are not
directly comparable.

¹ Kaggriculture ratings are from the saved official observation on
**2026-10-02 04:26 UTC**, not a final medal result.
