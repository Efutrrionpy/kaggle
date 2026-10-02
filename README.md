# Kaggle Research Reports

Three applied research studies in geological sequence prediction, cell tracking,
and competitive resource management.

| Competition | Principal models and methods | Final Private leaderboard rank | Official score |
|---|---|---|---|
| [ROGII — Wellbore Geology Prediction](ROGII/README.md) | CatBoost, Particle Filter / HMM alignment, robust stratigraphic projection | **444th out of 6,191 teams — Bronze medal** | Private RMSE **8.889** |
| [Biohub — Cell Tracking during Development](Biohub/README.md) | Temporal 3D U-Nets, node Transformers, DeepCenter, ILP tracking, collective-motion refinement | **1,714th out of 4,020 teams** | Best selected Private score **0.91051** |
| [Kaggriculture](Kaggriculture/README.md) | Demonstration-derived policies, state-conditioned economic routing, resource-constrained service planning | **Pending official finalization**¹ | Public ratings: FlexService **2409.8**; AdaptiveMilk **2163.7**¹ |

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

¹ Kaggriculture had no confirmed final rank in the saved official observation on
**2026-10-02 04:26 UTC**. The reported values are Public skill ratings, not ranks.
