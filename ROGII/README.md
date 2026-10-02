# ROGII Wellbore Geology Prediction — Bronze Medal Case Study

[![CI](https://github.com/Efutrrionpy/kaggle/actions/workflows/ci.yml/badge.svg)](https://github.com/Efutrrionpy/kaggle/actions/workflows/ci.yml)

An AI-assisted machine-learning research project for the Kaggle competition
[ROGII — Wellbore Geology Prediction](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction).
The task was to predict the hidden tail of `TVT` (True Vertical Thickness) for
horizontal wells from trajectory data, Gamma Ray logs, a known `TVT_input`
prefix, and a paired typewell.

## Result

| Measure | Result |
|---|---:|
| Private RMSE (lower is better) | **8.889** |
| Private rank | **444 / 6,191** |
| Percentile | **Top 7.2%** |
| Medal | **Bronze** |
| Silver cutoff | 8.581 at rank 309 |
| Gap to silver | 0.308 RMSE |
| Frozen F57 internal OOF | 8.5186 |

The silver target was not achieved. The final selected primary, **F57**, was
nevertheless the best account submission on the Private leaderboard. Its OOF
to Private gap was `+0.370`, substantially smaller than the Public-to-Private
gap, so the validation design was useful even though the candidate pool did
not reach the required ceiling.

## Why this problem was difficult

- The training set contained **773 horizontal wells and 5,092,255 rows**.
- Only the prefix of each well's `TVT_input` was known; the remaining
  **3,783,989 rows** formed native hidden tails for validation.
- Rows inside one well are highly dependent. Random row splits leak both
  sequence state and well identity.
- Spatial neighbors and paired typewells can also transmit labels unless every
  learned transform and neighbor structure is built inside each fold.
- The visible test fixture contained only three wells, and their legal input
  sequences exactly overlapped training sequences. This made the Public
  leaderboard an unusually weak proxy for novel hidden wells.
- The final notebook had to run offline under Kaggle's nine-hour limit on an
  unseen cohort of roughly 200 wells.

## Validation first

The primary protocol was a frozen five-fold, complete-well OOF design:

1. Keep every well entirely inside one fold.
2. Balance folds by scored-row load, without reading targets.
3. Expose only the legal `TVT_input` prefix and inference-time covariates.
4. Fit preprocessing, spatial neighbors, residual models and model selection
   only on fit wells.
5. Join predictions by `(well_id, row_index)` and require exact OOF coverage.
6. Score pooled row-level RMSE, while treating per-well median, P90 and worst
   error as diagnostics.

The public implementation of the critical contracts is in
[`src/rogii/validation.py`](src/rogii/validation.py). The full research process
also used poisoning invariance, prediction-mask, ID/order and finite-output
tests.

## Modeling path

```text
carry-forward baseline
        ↓
GR/typewell Particle Filter alignment
        ↓
spatial geology + residual boosting
        ↓
robust projection in U = TVT + Z
        ↓
290-feature query-local CatBoost (V71)
        ↓
F57 fixed ensemble
```

The two most important mechanisms were:

### 1. Typewell alignment

Particles tracked the smoother coordinate `U = TVT + Z`. At every horizontal
well station, candidate particle paths were converted back to TVT and scored
against the paired typewell's Gamma Ray curve. The readable reference version
is in [`src/rogii/alignment.py`](src/rogii/alignment.py).

### 2. Stratigraphic U projection

Direct TVT paths inherit well-trajectory movement. Transforming them to
`U = TVT + Z` produces a coordinate closer to geological surface elevation.
The hidden-tail base path was robustly smoothed with an iteratively reweighted
degree-four polynomial, then converted back with `TVT = U - Z`.

See [`src/rogii/projection.py`](src/rogii/projection.py).

### Final composition

The final fixed candidate was:

```text
F57 = 0.50 × V71 + 0.45 × U projection + 0.05 × raw HMM path
```

The composition is published in [`src/rogii/ensemble.py`](src/rogii/ensemble.py).
The production V71 CatBoost artifacts and public-notebook-derived components
are deliberately omitted from this repository.

## Experiment progression

| Stage | Best representative | OOF RMSE |
|---|---|---:|
| Minimal baseline | Last-known TVT carry-forward | 15.9099 |
| Geometry | Robust trajectory continuation | 15.2872 |
| Sequence alignment | Particle Filter/typewell GR | 12.8638 |
| Spatial geology | Fold-isolated surface prior | 12.1402 |
| Classical ensemble | PF + spatial + XGBoost residual | 11.1502 |
| Nested pipeline | Fixed nested blend | 10.6803 |
| Physical projection | Robust `U = TVT + Z` projection | 10.5418 |
| Sequence correction | Exact HMM/U blend | 10.0325 |
| Final candidate | F57 | **8.5186** |

Scores are not directly comparable across every exploratory protocol; the
table reports the frozen score associated with each promoted stage. F57's
`8.5186` was an explicitly labeled **hybrid cross-fit**: its V71 leg was
cluster-excluded, while its U/HMM leg used native complete-well OOF. It should
not be presented as a fully leave-cluster-out score for the entire pipeline.

The longer history is in [`docs/experiment_timeline.md`](docs/experiment_timeline.md).

## Public leaderboard trap

The account's best Public candidate scored **6.449**, better than F57's Public
score of **7.502**. It was not selected because its score was driven by the
three same-ID/overlapping visible wells and it lacked credible novel-well OOF
evidence. Its eventual Private score was **9.565**, versus **8.889** for F57.

This was the clearest project-level example of why leaderboard feedback should
be treated as weak distribution-shift evidence rather than a tuning set.

## Repository layout

```text
src/rogii/                   # readable reference implementations
examples/synthetic_demo.py  # data-free end-to-end mechanism demo
tests/                       # validation and numerical contracts
docs/methodology.md          # data, validation and model design
docs/experiment_timeline.md # promoted and rejected directions
docs/postmortem.md           # what worked, what failed, what changes next
docs/interview_story_zh-TW.md
```

## Quick start

From the repository root, enter this competition folder first:

```bash
cd ROGII
```

The competition data is not required for the synthetic demo.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
python examples/synthetic_demo.py
```

## What is intentionally not published

- Kaggle competition data or labels;
- trained CatBoost, neural-network and HMM artifacts;
- final submission CSV files and prediction caches;
- downloaded public notebooks or source with unverified redistribution terms;
- Kaggle credentials, browser state, operational receipts and screenshots;
- the 73 GB internal research workspace and one-off release machinery.

This repository is a curated technical case study, not a one-command
reproduction of the final Private score. Competition data must be obtained
from Kaggle under the competition rules.

## Postmortem in one paragraph

The strongest part of the project was validation: F57's internal estimate
generalized much better than the visible leaderboard implied. The main failure
was research allocation. A late random-initialized SDF experiment—with weak
inputs and little meaningful augmentation—was allowed to stand in for the
broader high-capacity dense-alignment family. Too much late-stage effort also
went into hard gates, manifests and release governance. A future attempt would
separate research and release lanes, keep an untouched group-level lockbox,
and test a task-native dense posterior model with pretrained encoders and
physics-preserving augmentation in the first half of the competition.

## AI-assisted research disclosure

This was an **AI-assisted ML research project**. The project owner set the
objective, validation standard, experiment priorities, model-selection rules
and final accountability. Codex agents implemented and executed a substantial
part of the code, tests and Kaggle operations. Claude Opus was used selectively
as a research critic to challenge hypotheses and identify blind spots; it was
not treated as experimental evidence.
