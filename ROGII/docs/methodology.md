# Methodology

## Problem formulation

For each horizontal well, the inference inputs included:

- measured depth (`MD`) and trajectory coordinates (`X`, `Y`, `Z`);
- Gamma Ray (`GR`), including legally visible future-tail values;
- a contiguous known prefix in `TVT_input`;
- a paired typewell containing `TVT` and `GR`.

The target was TVT for the rows after the known prefix. The official metric was
pointwise RMSE pooled across all scored rows, not mean per-well RMSE.

Training-only formation surfaces and hidden target values were prohibited from
inference features.

## Data audit

| Dataset component | Scale |
|---|---:|
| Horizontal wells | 773 |
| Horizontal rows | 5,092,255 |
| Known-prefix rows | 1,308,266 |
| Native hidden-tail rows | 3,783,989 |
| Typewell rows | 1,567,045 |
| Visible test wells | 3 |
| Visible scored rows | 14,151 |

Horizontal MD advanced in exact one-foot increments. Typewell sampling was
often 0.5 feet but was not universally regular. GR was heavily missing,
including roughly 1.20 million training-tail rows, so every inference path
needed a deterministic finite fallback.

The decisive audit finding was that all three visible test horizontal/typewell
sequences exactly overlapped training on legal inputs. Methods that memorized
or replayed these fixtures could dominate the Public leaderboard without
generalizing to novel hidden wells.

## Frozen complete-well validation

The primary protocol, `native-well-v1`, used five complete-well folds and seed
`20260714`.

Folds were created using only well identity and native scored-row counts. The
greedy assignment balanced scoring load at approximately 756,000 rows per
fold. Targets, formation labels and geometry values did not affect assignment.

For each held-out well:

1. expose its complete legal trajectory and GR;
2. expose only the native finite `TVT_input` prefix;
3. score only its native missing tail;
4. fit every learned preprocessing step on fit wells;
5. build spatial neighbors and target-derived structures from fit wells only;
6. persist OOF predictions keyed by `(well_id, row_index)`.

Every promoted OOF artifact had to provide one finite prediction for every
scored key, with no duplicate, missing or extra rows.

### Defensive tests

- complete-well fold disjointness;
- exact OOF coverage and row order;
- native prefix/tail mask validation;
- target and forbidden-column poisoning invariance;
- independent metric implementations;
- non-finite GR and prediction fallback tests;
- fit-only neighbor and preprocessing checks.

Later experiments added target-free spatial/typewell clusters and contiguous
XY-PC1 blocks to simulate novel-region shift. These stresses were supporting
evidence, not a claim that their distributions exactly matched Private data.

## Model families

### Continuation baselines

Carry-forward and local polynomial/geometry extrapolation established a
leakage-resistant floor. They were weak but essential for debugging scoring,
alignment and deployment.

### Particle Filter alignment

The typewell provides GR as a function of stratigraphic TVT. The horizontal
well provides GR along MD. A state-space tracker propagated multiple candidate
paths through the hidden tail and weighted them by the likelihood of observed
horizontal GR under the paired typewell curve.

The state used `U = TVT + Z`, which removed much of the trajectory-induced
movement from TVT. Multiple seeds and likelihood temperatures supplied both
predictions and uncertainty/agreement features.

### Spatial and residual models

Fold-isolated neighboring wells supplied local surface and formation priors.
Gradient-boosted trees learned residual corrections from trajectory, GR,
alignment and uncertainty features. Nested folds were used where a learned
combiner consumed upstream OOF predictions.

### Robust U projection

The strongest target-free physics transform took a base hidden-tail path,
converted it to `U = TVT + Z`, fit a robust degree-four curve along normalized
tail MD, and blended 75% projected path with 25% base path.

### V71

V71 was a query-local CatBoost model over 290 inference-legal features: 121
base features and 169 additional alignment, paired-typewell, self-diagnostic,
trajectory, spatial and GR features. Held-out fold or cluster models were used
for OOF; an all-773 model served genuinely novel hidden IDs.

The production implementation incorporated public-notebook-derived mechanisms
whose redistribution terms were not established, so it is described but not
republished here.

### F57

The final fixed blend was:

```text
0.50 V71 + 0.45 U projection + 0.05 raw HMM
```

V71 contributed local learned capacity, U projection supplied a smooth
physics-based hedge, and the small HMM leg preserved an alternative continuous
path estimate.

## Deployment

The code competition executed notebooks offline with a nine-hour limit. The
release path therefore required:

- deterministic dependency and artifact loading;
- inference for approximately 200 novel wells;
- full-data routing for unseen IDs;
- exact sample-submission order and schema;
- finite output under missing GR;
- runtime and memory margin;
- local hidden-shape stress and remote visible replay.

The final primary completed Kaggle execution and the 200-well local stress.
This established operational reliability, not hidden-geology accuracy.
