# Biohub Research Report

## 1. Problem and model architecture

The task was to reconstruct cell trajectories and divisions from volumetric
microscopy, with performance determined by the complete tracking graph.
We started from a public temporal 3D U-Net / node-Transformer pipeline,
combined two checkpoint variants, incorporated a DeepCenter localization prior,
and assembled associations through bidirectional score fusion, ILP, and graph repair.

The study examined whether motion evidence, learned division configurations,
longer temporal context, and self-supervised representations could improve
this pipeline. The final selected baseline achieved **0.91051 Private**;
the motion variant achieved **0.90743 Private**. The account placed
**1,714th out of 4,020 teams** on the final Private leaderboard.

## 2. Threshold and collective-motion refinement

The initial experiments kept the neural predictions fixed and changed graph
post-processing. On a 32-movie development panel, reducing a division threshold
from 0.26 to 0.12 improved the released-reference graph score from
**0.92125669 to 0.92210655**. The improvement was concentrated in one additional
division true positive; removing that movie reversed the comparison.

Collective-motion refinement estimated local motion using a robust median of
neighboring support pairs, then reconsidered ordinary continuation edges.
The implementation used a 12 μm search radius, up to eight predecessor
candidates, and 32 neighboring support pairs. It preserved the nodes and
protected division edges. The same development panel scored **0.92209576**.

The motion submission completed inference on a Kaggle T4 in approximately
24.2 minutes. The refinement itself took 44.4 seconds and changed 20 edges
in the visible output. Its **0.94218 Public / 0.90743 Private** result was
weaker on Private than the baseline replay's **0.94094 / 0.91051**.

## 3. NCC and native temporal training

Normalized cross-correlation (NCC) supplied direct image evidence for
continuation links. On 32 previously used movies, a continuation-focused
configuration increased graph score from **0.92209576 to 0.92424554**, while
losing division events. This motivated separate tests of native links,
fork-preserving NCC, and NCC without forks.

We trained a native temporal U-Net / Transformer recipe and evaluated 12
movies excluded from that checkpoint's fitting:

| Training checkpoint | Native graph | Fork-preserving NCC | NCC without forks |
|---|---:|---:|---:|
| Epoch 5 | 0.645376 | 0.679688 | 0.690039 |
| Epoch 20 | 0.654290 | 0.686770 | 0.696590 |

NCC consistently improved this recipe, but longer training produced limited
additional benefit and division precision remained weak. These results
characterize the tested recipe, not the ceiling of temporal neural models.
A fork-preserving NCC variant of the stronger deployment pipeline scored
0.942 Public at the saved three-decimal precision, without a visible gain.

## 4. Learned division configurations and ownership

The next models learned division configurations using partial supervision,
pair residuals, and ownership-aware decoding. A pair-residual model reduced
conditional weighted NLL from **2.107995 to 1.225944** on 30 fitting movies.
However, graph score fell from **0.93322792 to 0.91966697**: division true
positives increased from 4 to 7, while false positives increased from 12 to 121.

The mechanism was a mismatch between local scoring and global ownership.
Keeping single-edge potentials fixed did not keep selected edges fixed:
additional division pairs competed for the same children and altered the graph.

A separate ownership experiment improved four fitting movies from
**0.921203 to 0.937003** with joint decoding. On 15 movies excluded from
residual-head training, it instead reduced score from **0.970864 to 0.927121**;
factorized decoding scored **0.932039**. Limited positive examples and a shift
between the training and inference populations remained plausible explanations.

## 5. Five-frame encoders and self-supervision

We evaluated a trainable five-frame encoder against frozen visual features,
then added masked appearance/change self-supervision. The unregularized
encoder overfit its training data. With residual regularization, the pooled
two-fold comparison improved conditional NLL from **0.330700 to 0.327215**
and weighted AUC from **0.966829 to 0.968346**.

This correction changed one scalar per root while leaving intrinsic pair
ordering unchanged, limiting which final decisions it could affect.
Masked-change self-supervision improved one matched fold from
**0.358785 to 0.353003 NLL** and **0.972037 to 0.972670 AUC**, but low-false-positive
performance was mixed. These were intermediate-objective gains rather than
demonstrated improvements in complete tracking graphs.

## 6. Complete-graph evaluation

A later pipeline combined learned division scoring, dense temporal evidence,
and center information. Its saved 199-movie comparison was:

| Stage | Graph score | Division TP | Division FP |
|---|---:|---:|---:|
| Baseline route | 0.91420834 | 24 | — |
| Learned division stage (H) | 0.91875606 | 17 | 41 |
| H + dense / center stage | **0.92298783** | 24 | 33 |

The dense stage improved both score and division precision relative to H.
Relative to the baseline, however, the final route recovered eight different
division events and lost eight existing ones. Detector nodes, coordinates,
averaging, and candidate coverage also changed, so this was not an isolated
representation ablation. The submitted route scored **0.938 Public / 0.904 Private**.

A fixed residual-strength adjustment reached **0.92401391** descriptively on
all 199 movies. Selecting its strength across opposite source/fold groups
instead reduced a 120-movie comparison from **0.93060631 to 0.93015715**.
The full-panel improvement did not establish selection transfer.

Finally, expanding candidate roots from K500 to K1000 on 18 selected failure
movies added 8,988 H roots and 8,260 dense roots. Graph score remained
**0.920656263046**, with division counts unchanged at TP 5, FP 9, FN 38.
Some edges changed, but the added coverage did not recover scored events.

## 7. Comparison with leading solutions

The published top-five Private solutions highlight several alternative ways
to connect supervision and learned representations to graph decisions:

| Private rank / score | Reported approach |
|---|---|
| [Sergio, 1st / 0.977](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/1st-place-solution) | Expanded division supervision; learned related-cell occupancy and identity; greedy decoding |
| [Soheil, 2nd / 0.970](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/2nd-place-solution) | Joint detection, motion, uncertainty, and descriptors; retention of weak candidates |
| [yu4u, 3rd / 0.967](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/3rd-place-solution) | Separate detection, flow, matching, and division models; calibrated support and correctness |
| [Barry, 4th / 0.962](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/4th-place-solution) | Learned division confidence controlling node-level ILP costs and weak-daughter recovery |
| [Tang, 5th / 0.954](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/5th-place-3d-u-net-transformer-linker-multi-s) | Multitask linking, public-data pretraining, and confidence-aware ILP |

These are author-reported methods, not independently reproduced ablations.
The differences suggest that supervision coverage, candidate retention, and
the learned-score/decoder interface mattered more than the choice of solver alone.

## 8. Interpretation and validation limits

The experiments demonstrated useful motion, NCC, and dense-stage signals,
but also repeated gaps between local loss, graph quality, and official transfer.
Many development movies had upstream detector, crop, or model-selection exposure.
Residual-head exclusion therefore did not provide clean whole-pipeline OOF.
Different panels and node populations also prevent direct ranking of all
experimental scores in one table.

The main research finding is that stronger local association or division
scores must change the right globally selected events to improve tracking.
The [experiment table](results/research_results.csv) records the measured
comparisons and their evaluation scope. [Reproducibility](REPRODUCIBILITY.md)
identifies the public models and the implementation available here.
