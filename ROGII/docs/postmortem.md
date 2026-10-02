# Postmortem

## Outcome

F57 finished with Private RMSE **8.889**, rank **444 of 6,191**, and a Bronze
medal. Silver ended at rank 309 and RMSE 8.581, leaving a 0.308 gap.

This is a successful Bronze result and an unsuccessful Silver objective. Both
statements matter: the project demonstrated strong end-to-end research and
deployment, while missing its stated performance target.

## What worked

### 1. Validation reflected Private better than Public

F57 moved from 8.5186 internal OOF to 8.889 Private, a gap of 0.370. Its Public
score was 7.502, a much larger and optimistic gap of 1.387. The same-ID Public
candidate scored 6.449 Public but collapsed to 9.565 Private.

The complete-well split, fit-only transforms and refusal to tune against the
three overlapping visible fixtures were directionally correct.

### 2. Physics and learned models were complementary

Particle filtering and HMMs represented path continuity and GR/typewell
matching. The U projection encoded a smoother geological coordinate. V71
supplied high-dimensional nonlinear learning. Their fixed ensemble was more
competitive than any one classical component.

### 3. Release reliability was treated as part of modeling

The primary notebook passed offline execution, deterministic visible replay,
novel-well routing, row-order checks and a 200-well hidden-shape stress. The
best validated model was therefore available for final scoring.

## What did not work

### 1. The high-capacity structured model arrived too late

The problem can be formulated as dense alignment between horizontal-well and
typewell representations. The project explored this family late through an SDF
regression recipe with random initialization, only three effective channels,
weak augmentation and repeated identical samples. Its raw OOF RMSE of 34.705
rejected that recipe; it did not fairly reject dense alignment as a family.

The correct response should have been targeted redesign: pretrained encoder,
dense posterior or heatmap objective, uncertainty-aware decoding, PF/XY as soft
channels and physically legal augmentation.

### 2. Research and release work were not separated early enough

Late work accumulated manifests, one-shot locks, monitors and hard promotion
gates. These improved auditability but consumed time that could have funded
another high-ceiling modeling iteration.

### 3. Some robustness gates produced Type-II errors

Worst-well and arbitrary minimum-gain thresholds sometimes vetoed genuine
pooled improvements. Robustness should influence expected hidden score and
conditional hedge value, but only leakage, invalid inference, non-finite output
or release failure should normally act as absolute vetoes.

### 4. One lockbox was reused too often

Five frozen folds made comparisons reproducible, but dozens of decisions on
the same folds create family-level meta-overfit. A truly untouched group-level
lockbox should have been opened only for a small number of finalists.

## What changes next time

1. Build a leakage-resistant baseline and one accepted submission immediately.
2. Split work into a fast research lane and a hardened release lane.
3. Reserve at least 30% of early modeling compute for a task-native,
   high-capacity representation.
4. Reject configurations rather than entire high-upside families; allow up to
   three materially different, valid attempts.
5. Keep development CV, distribution-shift stresses and a one-use lockbox.
6. Use paired uncertainty and soft robustness penalties instead of arbitrary
   single-well hard gates.
7. Choose the second final slot by conditional rescue value and failure-mode
   diversity, not Public rank.

## Interview takeaway

The strongest claim is not “I tried 95 experiments.” It is:

> I recognized that the visible leaderboard was structurally misleading,
> built a legal complete-well evaluation system, combined sequence alignment,
> physical coordinates and learned models, deployed the resulting ensemble
> under offline constraints, and used the Private result to distinguish a
> validation success from a research-portfolio failure.
