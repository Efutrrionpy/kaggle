# Kaggriculture final top ten

The table uses the **verified final Private leaderboard**, retrieved on
**22 October 2026**, not ranks in provisional article titles. Scores are final
Bradley–Terry values. The organizer [announced the conclusion on October 21](https://www.kaggle.com/competitions/kaggriculture/discussion/751368).
[Compact official rows](results/top_ten_20261022.json) preserve the observation.

| Rank | Team | Final score | Substantive primary account located |
|---:|---|---:|---|
| 1 | M & M & P & Q | 5890.3 | [Author preview](https://www.kaggle.com/competitions/kaggriculture/discussion/745073), [source and method README](https://github.com/msdsm/kaggriculture-1st-solution) |
| 2 | Victor @ Tufa Labs | 5823.4 | Not located; [author profile](https://www.kaggle.com/vmerckle) |
| 3 | DSM | 5580.3 | [Author writeup](https://www.kaggle.com/competitions/kaggriculture/writeups/kaggriculture-3rd-place-dsm-solution), [repository](https://github.com/seven320/kaggriculture-3rd-place-solution) |
| 4 | Farmcore | 5487.4 | [Author writeup](https://www.kaggle.com/competitions/kaggriculture/writeups/farmcore-a-one-pass-transformer-trained-on-what-t), [repository](https://github.com/B3tMy3x/farmcore-kaggriculture) |
| 5 | 有辣条有权 | 5473.7 | [Author writeup](https://www.kaggle.com/competitions/kaggriculture/writeups/its-sft-all-the-way-down), [method and code guide](https://github.com/definitelynotrussellkirk-bit/kaggriculture-sft/blob/main/HOW-IT-WORKS.md) |
| 6 | CDE | 5465.0 | Not located; authors [christofhenkel](https://www.kaggle.com/christofhenkel), [arc144](https://www.kaggle.com/arc144), [crodoc](https://www.kaggle.com/crodoc) |
| 7 | DECEM | 5459.9 | [Author discussion](https://www.kaggle.com/competitions/kaggriculture/discussion/745367), [repository](https://github.com/Decem-Y/kaggriculture-bc) |
| 8 | itwastony | 5395.7 | Not located; [author profile](https://www.kaggle.com/itwastony) |
| 9 | tetsuya & yuanzhe & guoqin | 5338.7 | [Author writeup](https://www.kaggle.com/competitions/kaggriculture/writeups/from-reinforcement-learning-to-a-final-bc-agent) |
| 10 | KawattaTaido | 5334.0 | [Author writeup](https://www.kaggle.com/competitions/kaggriculture/writeups/10th-place-bc-ppo-on-a-single-rtx-5090), [repository](https://github.com/KawattaTaido/kaggriculture-release) |

## What the published methods say

These are author-reported methods and measurements, not experiments rerun for
this closeout. No third-party weights or complete writeups are copied here.

**1 — Alternating learning and planning.** MMPQ alternated BC and self-play PPO
using public replays and demonstrations from its heuristic planner. The final
architecture is a 10.23M-parameter, 12-block Transformer. One final agent combines
learned actions with resource-conflict repairs and a final-day search controller;
the other uses sequential masks in training and inference. Its reported lineage
includes about 8.29 million self-play games. The team also reports reaching first
place with a standalone heuristic planner: its result does not support a blanket
rejection of planning. [Preview](https://www.kaggle.com/competitions/kaggriculture/discussion/745073),
[implementation overview](https://github.com/msdsm/kaggriculture-1st-solution).

**3 — Full-action BC to PPO, with targeted interventions.** DSM's 10.4M
Transformer outputs primitive worker actions and autoregressive market orders.
Critic warmup, per-decision PPO clipping and an antisymmetric critic were
important to making learning work. Targeted post-processing and training-time
interventions added gains; broad worker overrides often harmed the policy.
The reported project compute, about 17,400 A100 GPU-hours for surviving training
logs, is far outside a single-consumer-GPU comparison. Its warning that cloned
rival opponents overstated local strength is relevant to our coverage problem.
[DSM account](https://www.kaggle.com/competitions/kaggriculture/writeups/kaggriculture-3rd-place-dsm-solution).

**4 — Better labels before more RL.** Farmcore reconstructs what the engine
actually executed instead of cloning requested orders that can be clipped or
discarded. Its Transformer drafts a whole turn and corrects the joint decisions.
Broad pretraining, single-team fine-tuning and averaging related checkpoints
produced its pure-BC finalists. Relabeling plus a feed guard changed one comparison
from 3/24 to 23/24 wins against the previous best; this is a combined change, not
an isolated estimate of label quality. The authors report roughly 5.5 A100-hours
for the final model. [Farmcore account](https://www.kaggle.com/competitions/kaggriculture/writeups/farmcore-a-one-pass-transformer-trained-on-what-t).

**5 — Autoregressive full-turn imitation and recent winners.** The two final
models were a 54.6M Transformer and a 7.25M typed-graph model. Worker commands
and ordered market actions are generated sequentially, with state updated for
earlier decisions in the turn. Training emphasized recent strong winning seats,
including opponents that beat the author's agents, followed by short late
fine-tunes. An earlier macro formulation consumed two weeks without becoming
the chosen solution. This is evidence about that implementation, not a proof
against macro policies. [Writeup](https://www.kaggle.com/competitions/kaggriculture/writeups/its-sft-all-the-way-down),
[technical guide](https://github.com/definitelynotrussellkirk-bit/kaggriculture-sft/blob/main/HOW-IT-WORKS.md).

**7 — Refreshing teachers instead of incremental RL.** DECEM's 8.2M entity
Transformer conditions on team, version and outcome. Recency-weighted pretraining
is followed by newest-day and specialist fine-tuning. Both finalists use BC
with small inventory-preservation rules, not PPO. The author reports about
50 minutes for pretraining on one RTX 5090. Examining actual loss margins made
another small RL gain less valuable than refreshing teachers. Recorded-opponent
forks were central to selection, but they do not establish responsive-field
validation. [DECEM account](https://www.kaggle.com/competitions/kaggriculture/discussion/745367).

**9 — Switching away from the original RL emphasis.** This team's final
18.4M Transformer/CNN was a BC policy with normalized executed-action labels,
history features and sequential resource accounting. Its final mixture weighted
MMPQ trajectories at 70%. Although RL established a viable starting direction,
late BC changes improved faster, and the final continuation was selected from
complete games rather than imitation loss alone. The report explicitly notes
uncertainty before its one final submission. [Ninth-place account](https://www.kaggle.com/competitions/kaggriculture/writeups/from-reinforcement-learning-to-a-final-bc-agent).

**10 — Recent BC plus bounded-scale PPO.** KawattaTaido trained a 21.8M policy
from 2,380 recent episodes, then used about 19 hours of PPO on one RTX 5090.
Target-tile actions, quantity-based market decisions and execution-aware masks
were central. The opponent mixture included historical policies and recorded
rivals; the latter needed aligned randomness and fills to avoid artificial
collapse. They remain open-loop opponents. Width gains emerged after PPO, not
reliably in BC loss—a warning against judging a component at the wrong downstream
stage. [Tenth-place account](https://www.kaggle.com/competitions/kaggriculture/writeups/10th-place-bc-ppo-on-a-single-rtx-5090).

## Consequential differences from our approach

Our finalists compiled a few demonstrated physical schedules and improved
their feedback, investment and service decisions. The seven available leading
accounts describe full-action learned policies that could absorb new complete
behaviors. Their varied use of RL, pure BC and rules does not support a single
prescription such as “always use PPO.” The plausible missed opportunity was a
fair full-controller learning trial, not a larger version of our six-sell-head
or binary-route learner. Its counterfactual performance within our actual
constraints remains unknown.

Data freshness was an explicit update mechanism in several leading systems.
Our replay archive and fresh seeds did not ensure current responsive-opponent
coverage; all eleven wins gained by Committed were against an older internal
ancestor. This is a measured limit of our evaluation scope, not a claim that
equal-sized replay collections should produce equal-ranked agents.

Execution semantics also mattered: within-turn inventory, partial fills and
order timing changed the meaning of a target or intervention. Our exact
official-path reproduction was worth retaining. The fifth-place guide's
independent-random-stream comparison exposes another distinction: matching a
native initial seed does not freeze subsequent shops after policies change
weed draws. A modified RNG can support causal diagnosis but is not proof of
native-engine parity. [Guide](https://github.com/definitelynotrussellkirk-bit/kaggriculture-sft/blob/main/HOW-IT-WORKS.md).

## Search limits

For ranks 2, 6 and 8, the official solution-link field was empty. We inspected
both pages of the competition's 39 “solution” search results, additional forum
name/rank queries, exact-name web searches, and official public-notebook lists
for every member of those teams. Those notebook queries returned no entries.
GitHub repository queries for known/same handles also returned no match;
profile pages were empty application shells or unavailable to the text reader.
These are unresolved searches as of October 22, not evidence that no code exists or
that the teams will never publish. No method is assigned to them. An unrelated
provisional “10th place” article was not substituted for the actual final top ten.
