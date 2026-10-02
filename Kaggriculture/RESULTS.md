# Kaggriculture Results

## Official submissions

| Controller | Submission | Public rating¹ | Measured maximum callback |
|---|---:|---:|---:|
| FlexService | 56705674 | **2409.8** | ≤ 0.1051 s |
| AdaptiveMilk | 56698261 | **2163.7** | ≤ 0.0491 s |

¹ Saved official observation: **2026-10-02 04:26 UTC**. Both submissions were
complete; final ranking remained pending. Submission closed on
2026-09-30 23:59 UTC, followed by further official games and ranking evaluation.

The callback figures are measured deployment results, not worst-case guarantees.
Each submitted version reproduced 1,438 actions across both seats of its own
official verification episode using `kaggle-environments==1.32.7`.

## Matched local comparisons

A win contributes 1 point and a draw 0.5. Candidate and control within each
row share a panel; rows with different opponents or worlds are not directly
comparable.

| Experiment | Panel size | Candidate | Control | Main result |
|---|---:|---:|---:|---|
| Ridge branch selection, early / late | 128 | 83 / 95 | 95 | No stable improvement |
| CEM market controller J_3 | 128 | 93 | 89 | Uncertain, opponent-dependent gain |
| Current-state service | 64 | 46 | 47 | More production, weaker competitive outcome |
| AdaptiveMilk | 704 | **636** | EconomicFirst 595; FeedDebt 501 | Promoted |
| FlexService | 768 | **677** | AdaptiveMilk 622; FeedDebt 548 | Promoted |
| NativeDeadlines | 1088 | **1055** | FlexService 1037 | 20 recoveries, two regressions |
| Committed | 896 | **843** | FlexService 832 | 11 recoveries, all against LateFlock |
| CareTrade | 448 | 418 | Committed 418 | No additional recovery |

NativeDeadlines, Committed, and CareTrade were local research variants.
Committed's maximum measured callback was 6.878 seconds, with maximum
per-game cumulative overage of 24.267 seconds in its retained-path checks.
Those measurements cannot be inferred from its faster FlexService parent.

Uncertainty was grouped by world rather than treating both seats and related
opponents as independent. Gains concentrated against one policy ancestor are
reported as such. The [research report](RESEARCH.md) details the mechanisms.

## Supporting data

- [Official observation](results/official_status.json)
- [Deployment measurements](results/deployment_checks.json)
- [Grouped and per-cell experiment results](results/)
- [Submitted-policy manifests](manifests/final_submissions.json)

Official sources: [leaderboard](https://www.kaggle.com/competitions/kaggriculture/leaderboard),
[evaluation](https://www.kaggle.com/competitions/kaggriculture/overview/evaluation),
and [timeline](https://www.kaggle.com/competitions/kaggriculture/overview/timeline).
