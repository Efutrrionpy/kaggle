# Kaggriculture: methods and experiments

**Silver · 246 / 10,148 teams · final Private score 4644.3.**
The best submitted controller, **FlexService**, combines demonstration-derived
production programs with state-responsive economic and service planning.
**AdaptiveMilk**, the second final controller, scored 4628.8.
[Official results](RESULTS.md) · [Resource use](COSTS.md) · [Reproduction](REPRODUCE.md).

## Final system

Kaggriculture is a 720-turn farming simulation scored by end-game bank balance.
Players interact through shared markets and shops. Labor, feeding, crops,
storage and transport create coupled timing and cash-flow constraints.

The final controllers are deterministic Python programs, not end-to-end neural
models. Complete physical programs were compiled from four public demonstration
episodes of submission 56614976, plus a common-opening episode. These supply
offline action/resource parameters, not the donor's private controller code.
At inference, our own feedback modules project worker effects from visible
state, supply materials, fund labor and land, and sell available surpluses.
Routing and investment logic adapt the program to the current farm and market.

**AdaptiveMilk** evaluates later animal investments using visible prices,
inventory and farm state, with approximate expectations for unrevealed shops.
It does not access hidden world seeds or future observations.

**FlexService** adds complete paid service tours: marginal wages, feed reserves,
incremental production, transport/delivery and nonlinear market value. A tour
must remain compatible with existing crop and retirement commitments.

Both archives include all inference dependencies and run using the Python
standard library. Selected official-engine primitives retain Apache-2.0
attribution. Our contribution is the feedback, investment routing, policy
composition and payable service planner—not the underlying public demonstrations
or engine. [Sources and licenses](SOURCES_AND_LICENSES.md).

## Measured comparisons

Candidate and control share the same initial-seed/opponent/seat panel within
each row. A win is 1 point and a draw 0.5; rows with different panels are not
directly comparable.

| Candidate | Panel | Candidate points | Matched control |
|---|---|---:|---:|
| AdaptiveMilk | 32 new seeds × 11 opponents × 2 seats | **636 / 704** | EconomicFirst 595; FeedDebt 501 |
| FlexService | 32 new seeds × 12 opponents × 2 seats | **677 / 768** | AdaptiveMilk 622; FeedDebt 548 |
| NativeDeadlines | 32 new seeds × 17 opponents × 2 seats | **1055 / 1088** | FlexService 1037 |
| Committed funding horizon | 64 new seeds × 7 opponents × 2 seats | **843 / 896** | FlexService 832 |
| CareTrade | 32 new seeds × 7 opponents × 2 seats | 418 / 448 | Committed 418 |

Only AdaptiveMilk and FlexService were submitted as the final pair.
An after-the-fact per-game best-of-two diagnostic favored Flex + Feed
(728 / 768) over Flex + Adaptive (683 / 768), but this is an unattainable selection
upper bound. Official team rating uses the better active agent, not a per-game
oracle. [Per-cell and grouped evidence](results/) accompanies the summaries.

### Scheduling and funding experiments

NativeDeadlines reorders already-paid workers within bounded windows. It
recovered 20 outcomes and introduced two losses in one world. Extra feeding at
turn 115 removed a wheat sale at turn 120; the forecast ended at 143 and missed
a turn 168 hire requiring 33 cash when only 32 remained, versus 62 for the
baseline. [Saved causal trace](results/native_deadlines_confirmation_20260930_regression_mechanism.json).

Committed extends the funding horizon to the next unresolved investment.
Its 11 additional wins all occurred against the earlier LateFlock policy;
against the other six opponents, candidate and control both scored 733 / 768.
CareTrade, which exchanges a scheduled care action for feeding, added no
prospective wins. Committed's maximum measured callback was 6.878 seconds,
considerably slower than the submitted policies.

## Alternative models and negative results

| Approach | Observed result | Scope of the finding |
|---|---|---|
| 209-feature NumPy MLP; two-route selection | 29 / 48 held-out points vs 36 / 48 for the existing selector | Only two fixed routes were available |
| Market-only behavior cloning; six SELL heads | 99.71% held-out row accuracy; both clone and exact teacher lost 0–8 to the mirror | Fixed worker logistics limit what learning can improve |
| Conservative three-gate imitation router | All gates abstained; paired outcomes unchanged after initial and expanded-calibration studies | No active intervention was evaluated |
| Ridge branch selector | 83 / 128 early or 95 / 128 late vs 95 / 128 baseline | Late selection gained two outcomes and lost two |
| Ridge / ExtraTrees at first policy divergence | World-OOF 120 / 152 and 122 / 152; cohort-held-out 113 and 115 vs fixed 118 | Performance depended on the held-out distribution |
| Cross-entropy method market search | J_3 scored 93 / 128 vs 89 / 128; grouped interval crossed zero | Gain was uncertain and opponent-dependent |
| Current-state extra service | Confirmation 46 / 64 vs 47 / 64 despite increased production | Shared-market effects can benefit the opponent more |

In activated extra-service cases, the acting player's income rose by roughly
20–25 while the opponent gained 53–59. Production is therefore not a sufficient
proxy for competitive outcome. The [early model summaries](results/early_model_comparisons.json)
retain measurements and limitations; some early temporary prototypes are not
available as complete executable closures.

## Validation and field comparison

Full games used responsive local opponents and both seats. Uncertainty was
grouped by initial seed; related policy lineages and the two seats are not
independent observations. Confirmation blocks used previously unused seeds.

The native 1.32.7 engine consumes weed draws only for empty tiles before
drawing shops from the same per-day random stream. Changed actions can thus
change later shops even with an identical initial seed. These are valid
native-engine games, but not identical future shop realizations for causal
attribution.

Fresh seeds did not ensure coverage of recent leading responsive opponents.
The final Gold cutoff was 5099.6 at rank 30, **455.3 Private score points above
FlexService**. High local points did not translate into comparable field strength.

The [final top-ten comparison](LEADING_SOLUTIONS.md) summarizes seven available
primary accounts. Their full-action learned policies could absorb new complete
behaviors; several emphasized recent imitation rather than enormous self-play
budgets. Our route/market learners are not equivalent tests of that action space.
The accounts differ in their use of RL, rules and planning, so they do not imply
a single universally superior method. The counterfactual result of training a
full controller within this project's resources remains unknown.

## Runtime and resource footprint

The submitted policies' maximum measured callbacks were **0.1051 s** for
FlexService and **0.0491 s** for AdaptiveMilk, with exact official-action parity.
Four recorded final confirmation batches comprised **7,936 all-arm games**,
using 18 CPU workers and totaling **3.715 hours of batch execution wall time**.
These are measured subsets, not the entire project's compute bill.
[Costs and coverage](COSTS.md) separates assistant tokens, cached input,
execution, waiting and untracked monetary expenditure.
