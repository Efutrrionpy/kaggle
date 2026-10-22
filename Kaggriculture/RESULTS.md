# Kaggriculture Results

## Official submissions

**Final Private: 246th of 10,148 teams, Silver, score 4644.3.** The official API reports a locked,
verified final leaderboard; its medal certificate agrees on rank, medal and
team count. Evidence was retrieved on **2026-10-22 at 08:48 UTC**.

| Controller | Submission | Submitted UTC | Public skill | Final Private BT | Measured maximum callback |
|---|---:|---|---:|---:|---:|
| **FlexService** | **56705674** | 2026-09-30 11:08:58 | **2341.9** | **4644.3** | ≤ 0.1051 s |
| AdaptiveMilk | 56698261 | 2026-09-30 05:29:02 | 2250.9 | 4628.8 | ≤ 0.0491 s |

These are the latest two complete, active submissions and the exact pair used
for final evaluation. FlexService is the better final submission and determines
the team's rank. Its **Public rank is 211**, distinct from the **Private rank
246**. No separate team rank is assigned here to AdaptiveMilk.

The last Gold row is rank **30**, score **5099.6**: our gap was **455.3 Private
score points**. This difference is not a calibrated win-probability or medal
confidence estimate. Full sanitized evidence: [final result](results/final_result_20261022.json).

Across all **118** submission records, the highest *currently stored* historical
Public value is **2879.8**, for inactive submission **55446189** on August 12
(a public Suda replay/terminal adaptation). That is neither an all-time peak
claim nor evidence that it would beat the finalists: the field and scoring
phase changed. It was not selected for the final tournament.

Submission closed on **2026-09-30 23:59 UTC**. The published timeline scheduled
further games from October 1 to approximately October 15, with API deadline
October 14 at 23:59 UTC. The organizer announced the conclusion on **October 21**.
The final BT fit uses games between finally active agents **across the whole
competition**, not only post-deadline games; games against deactivated agents
are excluded. A team's score is its better active agent and ties count as half
wins. These points follow the [organizer recap](https://www.kaggle.com/competitions/kaggriculture/discussion/751368)
and staff clarifications on [eligible episodes](https://www.kaggle.com/competitions/kaggriculture/discussion/732931)
and [team score/ties](https://www.kaggle.com/competitions/kaggriculture/discussion/739410).
Public skill and Private BT numbers must not be compared as one scale.

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

Uncertainty was grouped by initial seed rather than treating both seats and related
opponents as independent. Gains concentrated against one policy ancestor are
reported as such. The [research report](RESEARCH.md) details the mechanisms.

## Cost of selected final comparisons

These are measured completed batch wall times, including all comparison arms,
not cumulative project cost or isolated inference latency. Each used 18 spawned
workers with one numerical thread per worker; no completed games were rerun for
this report. [Exact records](results/measured_batch_costs.json).

| Batch | All-arm games | Wall time |
|---|---:|---:|
| AdaptiveMilk confirmation | 2,112 | 56.3 min |
| FlexService confirmation | 2,304 | 62.3 min |
| NativeDeadlines confirmation | 2,176 | 60.3 min |
| Committed first confirmation | 1,344 | 44.1 min |

These four batches total **7,936 games / 3.715 wall-hours**. Full-project
compute and monetary costs were not completely tracked. The [cost report](COSTS.md)
separately documents assistant model/cache usage, waiting and coverage limits.

## Supporting data

- [Verified final result](results/final_result_20261022.json)
- [Historical October 2 observation](results/official_status.json), retained as history rather than current status
- [Deployment measurements](results/deployment_checks.json)
- [Grouped and per-cell experiment results](results/)
- [Submitted-policy manifests](manifests/final_submissions.json)

Official sources: [leaderboard](https://www.kaggle.com/competitions/kaggriculture/leaderboard),
[evaluation](https://www.kaggle.com/competitions/kaggriculture/overview/evaluation),
and [timeline](https://www.kaggle.com/competitions/kaggriculture/overview/timeline).
