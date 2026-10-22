# Kaggriculture Research Report

**Final result: Silver, 246 / 10,148 teams, Private Bradley–Terry score 4644.3.**
FlexService was the best of our final two submissions; AdaptiveMilk scored
4628.8. The original Gold objective was unmet. [Official evidence and dates](RESULTS.md)
replace the earlier provisional observations without changing the submitted code.

The final system was a demonstration-derived production program with our own
state-responsive resource and service planning, not a trained end-to-end model.
The main research limitation was how far that representation and the available
opponent panel could support generalization to the final field.

## 1. Problem formulation

The simulation compares bank balances after 720 turns. Players share market
and shop effects, while workers, crops, animals, feed, storage, and transport
create coupled timing constraints. Increasing production can benefit the
opponent more than the acting player; estimated profit is useful only when
the associated work, funding, and deliveries are feasible.

We compared policies in matched initial-seed/opponent/seat cells and examined complete
game outcomes alongside worker actions, material flows, and both players'
cash balances. A new world block was used for confirmation after development.
The initial seed was the primary grouping unit for uncertainty analysis.

## 2. Learned selectors and market optimization

### August: restricted learners and a real representation limit

An August 20 NumPy MLP selected between two fixed routes using 209 current-state
features. Its 48 held-out decisions produced **29/48 match points**, versus
**36/48** for the existing selector. Rejecting that trained selector was
supported; it did not test whether learning a complete controller was viable.

The August 23 market-only BC correction recovered its teacher almost perfectly:
held-out exact-row accuracy **99.71%**, and rollout money **99.85%** of the
teacher against a pass opponent. Yet both clone and exact teacher lost **0–8**
to the mirror opponent. Only six SELL heads were trainable; worker logistics
and the route were fixed. The retained diagnosis correctly said full-action
redesign was needed. More PPO on that interface was not justified. An incomplete
external BC packet was also reasonably rejected because it lacked a usable
observation encoder and decoder—not because imitation had been disproved.

A separate conservative imitation router abstained everywhere after a
1,232-game study and a 1,744-game calibration correction. Fresh paired outcomes
were exactly unchanged. That yielded a useful diagnosis of this gated recipe,
but also consumed substantial evaluation without testing a policy that acted
differently. These [decision records](results/early_research_decisions.json)
are compact historical evidence; some early raw prototypes lived in temporary
directories, so they do not establish clean-clone reproduction of every trial.

### September: branch selection and market search

Later models selected among branches of an existing production policy.
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
The demonstrations came from four public donor episodes of submission
56614976 plus a common-opening episode. They were compiled action/resource
parameters, not the author's private controller code. We implemented the
feedback, investment routing and payable service planning; selected official
engine primitives were reused with Apache-2.0 attribution. Earlier research
also evaluated or adapted public controllers. Neither those baselines nor the
public demonstrations are claimed as original inventions. See
[source provenance and licenses](SOURCES_AND_LICENSES.md).

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

The final Private result was **4644.3 / rank 246 / Silver** for FlexService.
AdaptiveMilk's **4628.8** was slightly lower. Their final stored Public skill
ratings were **2341.9** and **2250.9**; the Public team rank was 211.
The official Gold cutoff was rank 30 at 5099.6. The old October 2 pending snapshot is
retained as historical evidence, not used to describe the current result.

The September 28 inventory recorded 6,297 complete official replays spanning 2,782
opponent teams and 5,543 submissions. These counts do not represent that many
independent worlds or executable opponent controllers. Local panels contained
related policies and lacked sufficient coverage of recent leading responsive
opponents. The shared feature index covered only 3,031 replays and was last
updated September 11; later targeted analyses did use additional records. The gap is
not proof those records were ignored, but collection volume was not evidence
of current executable-opponent coverage. High local scores did not establish
equivalent field strength.

Same-seed pairing also needs precise interpretation. The native 1.32.7 engine
draws weeds only for empty tiles before drawing shops from the same per-day
RNG. Different actions can therefore change later shops even with the same
initial seed. Our full-game runner used the native engine, not an independent
shop stream. The measured game outcomes remain actual native-engine outcomes;
they do not guarantee identical shop realizations for causal attribution.
Changing the RNG would be a separate variance-reduction diagnostic, not an
automatic replacement for deployment-faithful evaluation.

## 8. What the leading solutions change in the interpretation

The [final top-ten review](LEADING_SOLUTIONS.md) found substantive methods for
seven teams. They used learned full-action policies, with different balances
of replay imitation, RL and rules. Several relied primarily on imitation and
fresh demonstrations rather than enormous self-play budgets. This undermines
any claim that our restricted market/route learners fairly exhausted learning
as a family. It does **not** prove that adopting a Transformer within our
remaining time and implementation constraints would have delivered Gold.

The useful contrast is the update mechanism. Our few compiled programs gained
reliable local feedback and scheduling repairs; leading systems could ingest
new complete behaviors as the field changed. Our last Committed gain was real
but entirely against an older internal ancestor, so a larger local win total
did not address the demonstrated competitive gap. Retaining tested finalists
instead of making an unsupported last-minute replacement was defensible;
staying within a narrow representation for so long deserves a separate review.

The strongest measured progression in our work came from expanding narrow selectors into
complete production programs with actual material, labor, and funding feedback.
The remaining limitation was generalization across changing opponents and
markets. [Transferable lessons](DESIGN_REVIEW.md) distinguish measured process
limitations from hindsight hypotheses. [Prompt recommendations](PROMPT_RECOMMENDATIONS.md)
are proposed edits, not changes to the original Goal or shared policy.
[Reproduction](REPRODUCE.md) explains which exact policies can be rebuilt.
