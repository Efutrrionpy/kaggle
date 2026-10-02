# Biohub Results

## Official evaluation

| Final competition result | Outcome |
|---|---|
| Final Private leaderboard rank | **1,714th out of 4,020 teams** |
| Best selected Private score | **0.91051** |
| Medal | None |

The rank is the team's final placement, based on its best selected submission.
The saved leaderboard displayed the score as 0.910; the submission readback
retained five-decimal precision.

| Pipeline | Submission | Public | Private | Selection |
|---|---:|---:|---:|---|
| Temporal U-Net / Transformer baseline replay | 55998516 | 0.94094 | **0.91051** | Selected |
| Baseline + collective-motion refinement | 56071433 | **0.94218** | 0.90743 | Selected |
| Native / learned-division / dense route | 56593643 | 0.938 | 0.904 | Unselected; scores at saved three-decimal precision |

The first two pipelines used the public temporal tracking baseline and
DeepCenter support described in [reproducibility](REPRODUCIBILITY.md).
The motion variant improved Public but reduced Private performance.

## Local experiments

| Comparison | Population | Metric | Control → candidate |
|---|---|---|---:|
| Division threshold 0.26 → 0.12 | 32 movies | Reference graph score | 0.921257 → 0.922107 |
| Motion → NCC continuation | 32 movies | Reference graph score | 0.922096 → 0.924246 |
| Learned pair residual | 30 fitting movies | Conditional NLL | 2.107995 → 1.225944 |
| Same pair residual | 30 fitting movies | Reference graph score | 0.933228 → 0.919667 |
| Joint ownership transfer | 15 movies excluded from head training | Reference graph score | 0.970864 → 0.927121 |
| Regularized five-frame encoder | Two folds | Weighted AUC | 0.966829 → 0.968346 |
| Baseline → H + dense / center | 199 movies | Reference graph score | 0.914208 → 0.922988 |
| Cross-fitted residual-strength selection | 120 movies | Reference graph score | 0.930606 → 0.930157 |
| K500 → K1000 candidate roots | 18 selected failure movies | Reference graph score | 0.920656 → 0.920656 |

Lower NLL is better; higher graph score and AUC are better. The populations and
upstream exposure differ across rows. Local scores use the released reference
metric and do not substitute for the official hidden-data evaluation.

The full [research report](RESEARCH_HISTORY.md) explains model changes,
division false positives, selection transfer, and comparisons with the leading
solutions. The machine-readable [experiment table](results/research_results.csv)
includes the original source-record identifiers.

## Evidence

- [Official leaderboard](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/leaderboard): saved Private observation from 2026-10-01.
- [Official evidence summary](results/official_evidence.json): ranking and source metadata.
- [Model and submission references](results/final_artifacts.json): selected artifacts, precise submission scores, checkpoint sources, and hashes.
