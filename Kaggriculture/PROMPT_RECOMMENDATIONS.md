# Concise Goal prompt recommendations

These are proposals for review, **not edits to shared policy or the original
Goal**. The [original specification](design/GOAL_original.md) already contains
useful rules about family-level conclusions, expected information value and
deployment validation. Some failures were execution gaps, not missing rules.

## Three targeted replacements

| Existing clause or ambiguity | Observed behavior | Proposed short wording | How to test the change |
|---|---|---|---|
| `validation` and `experiment_loop` prescribe OOF, folds, lockbox fractions and generic promotion stages | This was sequential competitive control; route labels, action accuracy and whole-game strength answered different questions | **Define the independent unit, deployment action and final metric first. Use only validation steps that test this task; name any proxy and its limit.** | The first experiment identifies the real unit and outcome without inventing irrelevant folds or treating a proxy threshold as the objective. |
| `family_policy` correctly says one failed configuration does not reject a family, but a restricted wrapper can still stand in for the family in practice | Near-perfect market-only BC reproduced a weak teacher; full-action learning remained a distinct unresolved formulation | **When a trial fails, state what it could control, what imposed its ceiling, and which materially different formulation remains untested.** | A decision record distinguishes optimizer failure from action/representation limits; an incomplete external artifact is not labeled evidence against its method. |
| `model_selection` emphasizes stable grouped validation, while field freshness arrives in late competition-specific overrides | Fresh seeds and repeated local gains did not ensure current opponent coverage | **At meaningful decisions, compare evaluation coverage with the current deployment population and compare the next incremental step with the best feasible alternative.** | The next action can change when gains concentrate in an obsolete subgroup, without a fixed attempt count, mandatory method family or arbitrary gate. |

These lines should replace overlapping prose, not accumulate as another
checklist. They do not prescribe Transformers, RL, imitation, a worker count,
an iteration quota or a numerical promotion threshold.

## A compact cross-competition core

> Optimize the actual final objective under the task's rules and deployment
> constraints. Choose experiments by expected decision value and cost. Validate
> on independent, relevant units; distinguish proxy gains from end-to-end gains.
> Diagnose failed implementations and formulations without prematurely rejecting
> a family. Reassess when new evidence changes the likely ceiling or deployment
> distribution. Preserve a reproducible finalist, verify the official target
> explicitly, and respect user pauses.

Keep task-specific metrics, legal data sources, deadlines and reproduction
commands in the local project record rather than expanding this core for every
competition.

## Fixes that are not prompt changes

The original Goal already says only final Gold is success. The legacy monitor's
Gold-or-Silver status predicate was an implementation mismatch; it calls for a
target-predicate check, not another paragraph about winning. Likewise, empty
consultation attachments, stale data indexes, nonportable temporary prototypes
and GPU faults need concrete tool/data/resource fixes. This closeout keeps
the Goal paused and explicitly records Silver as unmet; no broader policy
was silently changed.
