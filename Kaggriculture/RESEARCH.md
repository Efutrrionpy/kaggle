# Kaggriculture Research Report

## 1. Problem formulation

The simulation compares bank balances after 720 turns. Players share market
and shop effects, while workers, crops, animals, feed, storage, and transport
create coupled timing constraints. Increasing production can benefit the
opponent more than the acting player; estimated profit is useful only when
the associated work, funding, and deliveries are feasible.

We compared policies in matched world/opponent/seat cells and examined complete
game outcomes alongside worker actions, material flows, and both players'
cash balances. A new world block was used for confirmation after development.
The world was the primary grouping unit for uncertainty analysis.

## 2. Learned selectors and market optimization

Early models selected among branches of an existing production policy.
A **Ridge regression** selector learned compatible branch choices from
development games. In a new 32-world, 128-cell comparison, the fixed policy
scored **95 points**, while early and late selection scored **83 and 95**.
The late selector gained two outcomes and lost two, providing no net advantage.

We also tested **Ridge and ExtraTrees** at the first divergence between strong
policies, using 92 legal current-state features. World-OOF scores were
**120 / 152 and 122 / 152**. Holding out an entire cohort reduced them to
**113 and 115**, below the fixed candidate's **118**. Selection performance
was sensitive to how the evaluation distribution was separated.

Market-control experiments used **CEM** to search parameters through complete
games. Initial candidates sold feed that was needed later or created inventory
that displaced incoming milk. Correcting these constraints improved the
implementation, but did not establish a strong policy. A later J_3 candidate
scored **93 / 128**, against **89 / 128** for the control; the world-grouped
interval crossed zero and performance against Yarn5 decreased from 43 to 39
points out of 64.

## 3. Current-state service and competitive effects

We next modeled service decisions from actual inventory and animal state.
A small development comparison improved from **26 / 32 to 27 / 32**, but
confirmation on eight new worlds scored **46 / 64**, against **47 / 64**
for the original policy.

The added service generated more eggs, yet in activated cases the acting
player's income increased by roughly 20–25 while the opponent gained 53–59.
This demonstrated why local production gains must be evaluated through shared
markets and relative end-game wealth.

## 4. Demonstration-derived programs and resource feedback

The later policy family used complete physical programs compiled from
publicly downloadable demonstrations. At each turn, it projected the acting
player's worker effects, supplied required materials, labor, and land, and
sold available surpluses. Historical actions became offline policy parameters;
runtime decisions used the player's currently visible state.

We extended this representation with common openings, state-dependent entry
conditions, shop-to-program routing, and later animal-investment choices.
The demonstrations came from public episodes of submission 56614976; they
were not the author's private controller code. Related descendants were
treated as correlated opponents rather than independent strong policies.

## 5. Submitted controllers

### AdaptiveMilk

AdaptiveMilk preserved the established opening and used economic forecasts
at later investment decisions to choose animal exposure. The forecasts used
visible prices and farm state, with approximate expectations for unrevealed
shops. They did not read hidden world seeds or future observations.

On **32 new worlds × 11 opponents × 2 seats**, AdaptiveMilk scored
**636 / 704 points**, compared with **595** for EconomicFirst and **501**
for FeedDebt. Its total comprised 635 wins, two draws, and 67 losses.

### FlexService

FlexService evaluated complete paid service tours on an existing farm.
The calculation included marginal wages, feed reserves, incremental animal
production, transport and delivery, and nonlinear market value. A service
route had to remain compatible with existing crop and retirement commitments.

On **32 new worlds × 12 opponents × 2 seats**, FlexService scored
**677 / 768**, compared with **622** for AdaptiveMilk and **548** for FeedDebt.
The official submissions were FlexService 56705674 and AdaptiveMilk 56698261.

Portfolio analysis identified a trade-off: an after-the-fact best-of-two
diagnostic favored Flex + Feed at **728 / 768**, compared with **683 / 768**
for Flex + Adaptive. This diagnostic is an unattainable per-game selection
upper bound, not a reproduction of the official two-submission rating system.

## 6. Native scheduling and longer cash-flow horizons

**NativeDeadlines** rearranged the work of already-paid workers within limited
windows while preserving necessary physical tasks. On 32 new worlds against
17 opponents in both seats, it won **1055 / 1088** cells, versus **1037** for
FlexService: 20 recoveries and two regressions.

Both regressions occurred in one world. Additional feeding at turn 115
removed a wheat sale at turn 120. By turn 168, the candidate held 32 cash
instead of 62; seven workers required 33, so one could not be hired. The
original feasibility forecast ended at turn 143 and missed this commitment.

**Committed** extended the funding horizon to the next unresolved investment
decision. Across two non-overlapping 32-world blocks with seven opponents,
it won **843 / 896**, versus **832** for Flex, with 11 recoveries and no
regressions. All 11 recoveries were against the earlier LateFlock policy;
against the other six opponents, both scored **733 / 768**.

**CareTrade** allowed one scheduled care action to be exchanged for additional
feeding, accounting for both effects. It recovered two development outcomes,
but on 32 new worlds scored **418 / 448**, identical to Committed, with mean
final-balance difference lower by 28.88. This configuration was not promoted.

These variants were local research results and were not part of the submitted
pair. Committed's measured maximum callback was 6.878 seconds, substantially
higher than the submitted controllers, adding a deployment cost to its narrow gain.

## 7. Results and limitations

The saved official observation on **2026-10-02 04:26 UTC** reported Public
ratings of **2409.8 for FlexService** and **2163.7 for AdaptiveMilk**.
Final ranking remained pending during post-submission evaluation.

The study collected 6,297 complete official replays spanning 2,782 opponent
teams and 5,543 submissions. These counts do not represent that many
independent worlds or executable opponent controllers. Local panels contained
related policies and lacked sufficient coverage of recent leading responsive
opponents. High local scores therefore did not establish equivalent field strength.

The strongest measured progression came from expanding narrow selectors into
complete production programs with actual material, labor, and funding feedback.
The remaining limitation was generalization across changing opponents and
markets. [Results](RESULTS.md) preserves matched comparisons;
[reproduction](REPRODUCE.md) explains which submitted policies can be rebuilt.
