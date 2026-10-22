# Biohub: models, results and measured resources

**Final Private rank: 1,714 / 4,020 teams. Best selected Private score:
0.91051. Medal: none.** [Official result evidence](FINAL_RESULTS.md).

## Approach and contribution

The deployed baseline combined two public temporal 3D U-Net / node-Transformer
checkpoint variants, a DeepCenter localization prior, bidirectional/harmonic
association fusion, ILP, and graph repair. It adapted
[nusrati/0-940](https://www.kaggle.com/code/nusrati/0-940); checkpoint origins
and sharing limits are in [source attribution](THIRD_PARTY_NOTICES.md).

The original fixed collective-motion component estimated local displacement
from up to 32 neighboring support pairs and reconsidered ordinary continuation
edges within a 12 μm radius, using up to eight predecessor candidates.
It retained nodes and protected division edges.
The [implementation](src/csv_overlay.py) and synthetic tests are published;
external notebook source and weights are not redistributed.

| Submitted pipeline | Public | Private | Outcome |
|---|---:|---:|---|
| Baseline replay / threshold hedge | 0.94094 | **0.91051** | Selected; best Private |
| Fixed collective-motion variant | **0.94218** | 0.90743 | Selected; higher Public did not transfer |
| Later native / learned-division / dense route | 0.938 | 0.904 | Not selected; three-decimal saved scores |

## Scientific comparisons

| Method | Existing measurement | What it established |
|---|---|---|
| Threshold / collective motion | On 32 development movies, threshold 0.26→0.12 changed graph score 0.921257→0.922107; fixed motion scored 0.922096 | Small, panel-sensitive postprocessing gains; not hidden-data proof |
| NCC continuation | Same 32-movie comparison: 0.922096→0.924246, with lost division events | Direct image evidence helped continuation, but topology and division recall also mattered |
| Native temporal training | On 12 checkpoint-unfitted movies, epoch-5 native/fork-NCC/no-fork NCC: 0.645376/0.679688/0.690039; epoch 20: 0.654290/0.686770/0.696590 | NCC consistently helped this recipe; longer training added limited gain |
| Learned pair residual | Fitting NLL 2.107995→1.225944, but graph score 0.933228→0.919667 and division FP 12→121 | Better local scores changed child ownership and could hurt the final graph |
| Joint ownership model | Four fitting movies improved 0.921203→0.937003; 15 head-training-excluded movies fell 0.970864→0.927121 | Fitting improvement did not establish transfer |
| Five-frame encoder / masked-change self-supervision | Regularized two-fold AUC 0.966829→0.968346; one SSL fold NLL 0.358785→0.353003 | Learned temporal signals, with mixed low-FP behavior; not official graph gains |
| Full learned / dense route | Exposed 199-movie graph readout 0.914208→0.918756→0.922988 | Dense stage improved on H, but the official submission was weaker than the selected baseline |
| K500→K1000 candidate expansion | Added 8,988 H roots / 8,260 dense roots; score remained 0.920656263046, TP5/FP9/FN38 | Extra coverage changed some edges but recovered no additional scored events |

The [31-row result table](results/research_results.csv) preserves evaluation
populations and recorded source identifiers. The central observation is a gap
between learning a useful signal and changing the right globally selected
events. Node populations, supervision coverage, ownership and lineage topology
all affect that conversion; these comparisons do not isolate a single cause.

## Context and validation limits

Published final leading solutions used expanded division supervision and
related-cell occupancy/identity
([1st](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/1st-place-solution)),
joint detection/motion/uncertainty/descriptors
([2nd](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/2nd-place-solution)),
separate detection/flow/matching/division models
([3rd](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/3rd-place-solution)),
learned division-aware ILP costs
([4th](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/4th-place-solution)),
and multitask linking/pretraining/confidence-aware ILP
([5th](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/5th-place-3d-u-net-transformer-linker-multi-s)).
Their reported Private scores were 0.954–0.977. These are saved author-reported
comparisons, not independently reproduced improvements or an additive recipe.

Many local movies had upstream detector, crop or model-selection exposure.
Excluding a movie from residual-head fitting did not make the whole pipeline
clean OOF. Panels and detector nodes differed, so scores across rows cannot be
ranked as if measured on one untouched test set. Visible CSV parity and runtime
do not reproduce the hidden Private evaluation.

## Resources and costs

Existing records show a **1,454.32 s visible notebook execution on a Kaggle T4**,
including **44.38 s** motion refinement. A separate preserved CPU replay took
**13.72 s** and matched the selected visible output exactly. These are specific
execution-wall measurements, not total GPU-active time or training expenditure.

The fixed main-thread accounting snapshot contains **5,317,789,093 model
interaction tokens**, including **5,212,252,288 cached-input tokens**, from
July 29 through October 22, 2026 UTC. It includes later analysis/reporting.
Recorded terminal-turn wall time and tool waits are not compute-time estimates.
Actual project-attributable payments, full training compute and electricity
remain **untracked**, not zero. [Cost scope, model breakdown and limitations](COSTS.md).

[Reproduction](REPRODUCIBILITY.md) documents what is runnable from this public
package and which neural assets/data must be obtained separately.
