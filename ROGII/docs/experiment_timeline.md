# Experiment Timeline

The internal registry contained roughly 95 executed runs across about 60
mechanism families. This document keeps only the stages that changed a decision.

## Promoted path

| Stage | Mechanism | OOF RMSE | Decision |
|---|---|---:|---|
| B0 | Last-known TVT carry-forward | 15.9099 | Finite fallback |
| B3 | Geometry/derivative ridge continuation | 15.2872 | Diversity component |
| PF | Multi-seed Particle Filter/typewell alignment | 12.8638 | Promote |
| Spatial | Fold-isolated geology/surface transfer | 12.1402 | Promote |
| Classical ensemble | PF + spatial + XGBoost residual | 11.1502 | Incumbent |
| Nested65 | Nested raw pipeline blended at fixed 65% | 10.6803 | Deployable fallback |
| U projection | Robust quartic smoothing in `U=TVT+Z` | 10.5418 | Promote |
| HMM-U100 | 90% U + 10% exact HMM path | 10.0325 | Strong evidence; release lineage blocked |
| V71 | 290-feature query-local CatBoost | ~8.7–8.8 | Promote |
| F57 | 50% V71 + 45% U + 5% raw HMM | **8.5186** | Final primary |

## Representative rejected directions

| Family | Best observed evidence | Why it stopped |
|---|---:|---|
| Compact TCN | 12.8105 | Small additive signal; tail diagnostics regressed |
| Masked Transformer blend | 10.2761 | Failed held-fold stability gates |
| Small SDF U-Net blend | 10.3372 | Failed held-fold gates |
| GR DTW/Viterbi | 10.3866 | Unstable across wells and horizons |
| Fault-aware surface blend | 10.1159 | Fold-0 robustness failure |
| Sequence-shift posterior | 9.8621 pilot | Source/held-fold instability |
| Prefix router | 10.5570 source folds | Low precision and concentrated rescue |
| Bayesian structural posterior | 7.1313 on 32-well pilot | Posterior collapse and top-well concentration |
| High-capacity SDF | 34.705 raw OOF | Invalid family-level conclusion; weak recipe |

## Model-selection lessons

Several candidates achieved a better mean OOF score but were rejected by
predeclared robustness gates. In hindsight, some gates were too rigid:

- a worst-single-well regression threshold vetoed a large pooled gain;
- a fixed minimum gain of 0.03 rejected an improvement of 0.0273;
- repeated use of the same five folds created meta-overfitting risk;
- failure of one SDF configuration was interpreted too broadly.

Future selection should keep leakage, numerical invalidity and deployment
failure as hard vetoes, while treating ordinary fold/well robustness as soft,
uncertainty-aware evidence.

## Public versus Private

| Candidate | Public | Private | Interpretation |
|---|---:|---:|---|
| F57 | 7.502 | **8.889** | Final primary; best account Private |
| V71 | — | 9.319 | Final conditional hedge |
| Same-ID public stack | **6.449** | 9.565 | Public overlap failure |
| U projection | 9.685 | 10.411 | Conservative but weak |
| Nested65 | — | 10.636 | Strong internal fallback, insufficient ceiling |

The final choice of F57 and V71 was correct among submitted candidates. The
shortfall came primarily from the model portfolio, not the last submission
selection.
