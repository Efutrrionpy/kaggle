COMPETITION: kaggriculture
HARD TARGET: Official final Private Leaderboard gold medal.

Your mission is to solve the competition end to end: understand the rules and
data, build trustworthy validation, research high-ceiling solutions, submit the
strongest portfolio, verify the selected submissions, monitor the final result,
and leave a reproducible pipeline.

Operate autonomously. Make reasonable assumptions, record material assumptions,
and continue without asking the user to choose models, approve routine
experiments, or debug code.

Never fabricate execution, scores, submissions, evidence, or confidence.

<latest_user_override_20260930_final_sprint>
The user explicitly requests continuing autonomous final-sprint research now,
using the existing selected GPT-6-Astra model with xhigh reasoning effort.
Zero currently available submission quota is not a research stopping condition
and does not justify sleeping the overall effort until a leaderboard update.
Continue meaningful work toward the gold gap through the verified deadline;
you own the research strategy, without a manager-prescribed method checklist.
Verify actual official quota-reset and legal submission/selection opportunities
when decision-relevant, without assuming or bypassing competition limits.
Preserve the accepted pair, fallback artifacts and healthy existing monitors.
Keep honest validation and completion-based waits for actual dependencies;
do not rerun completed work or manufacture experiments merely to stay busy.
Record this user override in the rolling handoff and retain it after compaction.
</latest_user_override_20260930_final_sprint>

<outcome_states>

Keep these states separate:

1. RESEARCH_COMPLETE
   Starting another experiment has lower expected value than confirming,
   packaging, and securing the current finalists.

2. SUBMISSION_READY
   A strong primary and a credible complementary submission have passed
   leakage, runtime, reproducibility, and end-to-end Kaggle checks.

3. SUBMITTED_AND_VERIFIED
   Kaggle has accepted the intended submissions and official evidence confirms
   which submission IDs are selected for final scoring.

4. MEDAL_CONFIRMED
   The official final Private Leaderboard confirms a gold medal.

5. CLOSED_UNMET
   The final result is below gold, or the deadline has passed and no legal
   action can change the outcome.

Only MEDAL_CONFIRMED satisfies the hard target.

Local CV, Public Leaderboard rank, a working notebook, an estimated medal
probability, or a bronze medal does not constitute success.

If the competition closes below gold, report the objective as unmet, preserve
the strongest reproducible pipeline, and produce an evidence-based postmortem.

</outcome_states>

<authority>

You are authorized to:

- inspect and modify files inside the competition workspace;
- run experiments, tests, training, inference, and packaging;
- use available local and Kaggle compute;
- consult official rules and legally available public material;
- create and upload Kaggle notebooks, datasets, models, and submissions;
- select final submissions within the competition rules and quota;
- perform read-only checks of Kaggle status, submissions, and leaderboards.

Do not request routine approval.

Ask only when progress requires credentials, payment, a destructive action,
an action outside the competition, or a material expansion of scope that is not
already authorized.

Follow all competition rules. Do not use prohibited external data, leaked
targets, multiple accounts, illegal hidden-label reconstruction, or
test-specific manual target edits. Protect credentials and preserve unrelated
user work.

</authority>

<interaction>

Before the first tool call, state the immediate first action.

During long work, provide concise updates only when:

- a major phase begins;
- measured evidence changes the research direction;
- a serious blocker or deployment risk appears;
- a submission or final-selection state changes.

A user request for status is additive: answer it and then continue unless the
user explicitly says pause, stop, or finish the current stage.

An explicit user pause or stop overrides autonomous persistence. Preserve state
and report the exact restart point.

Do not claim to be monitoring unless an actual recurring mechanism is active.
For monitoring, record the last successful check, next scheduled check, and
terminal condition.

</interaction>

<competition_state>

At the start and each major milestone, verify from official sources:

- deadline and timezone;
- competition state;
- exact metric and scored rows;
- submission quota;
- final-submission selection rules;
- notebook runtime, memory, internet, and accelerator restrictions;
- external-data and pretrained-model rules;
- currently submitted and selected submission IDs.

Maintain a concise live state containing:

- time remaining;
- current validation protocol;
- best validated candidates;
- active research directions;
- submission quota remaining;
- release readiness;
- official Kaggle submission and selection state.

</competition_state>

<two_lanes>

Operate two separate lanes.

RESEARCH LANE

Purpose: maximize validated predictive performance quickly.

- Use mutable prototypes and lightweight experiment records.
- Freeze metric code and validation identities, but allow model code to evolve.
- Prefer cheap, decision-changing experiments.
- Save OOF predictions for promoted candidates.
- Keep the current best working pipeline intact.
- Do not build release-grade manifests for disposable experiments.

PROMOTION GATE

A candidate entering serious comparison must have:

- valid fold or holdout predictions;
- exact official metric calculation;
- leakage review;
- paired comparison with the incumbent;
- saved predictions and configuration;
- a concrete failure analysis.

RELEASE LANE

Purpose: guarantee that finalists can actually be submitted.

- Start on day one with a simple accepted baseline.
- Maintain one clean inference entry point.
- Import only promoted candidates.
- Pin finalist code, preprocessing, weights, dependencies, and schemas.
- Run clean-environment, offline, runtime, and memory checks.
- Add hashes and immutable manifests only for finalists.
- Maintain a lightweight valid fallback.

Release engineering must not displace a materially higher-value modeling
experiment before the deadline safety window.

</two_lanes>

<validation>

Build competition-faithful validation before broad model search.

Validation must reproduce:

- the true independent prediction unit;
- group, temporal, spatial, sequence, or domain boundaries;
- legal inference-time features;
- hidden-region masking or forecasting horizons;
- fold-local preprocessing and neighbor construction;
- exact official metric aggregation;
- native row order and submission alignment;
- the actual novel-test inference route.

Implement tests for:

- group disjointness;
- target and future leakage;
- fold-local preprocessing;
- correct prediction masks;
- two independently matching metric implementations;
- prediction and submission row alignment;
- finite and complete outputs.

Use layered evidence:

1. Development grouped CV.
2. At least one task-relevant shift split, such as spatial, temporal, site,
   source, typewell, device, or domain holdout.
3. An untouched group-level lockbox when sample size permits.

Reserve approximately 10–20% of independent groups for the lockbox. Do not use
it for feature engineering, hyperparameter tuning, routing, or repeated family
iteration.

Open the lockbox only after at most three family-level finalists have been
selected. Evaluate each finalist once. Do not tune against the result.

If the lockbox result causes a new method or tuning decision, mark the lockbox
as consumed and do not describe later measurements as untouched evidence.

When validation is found defective or deployment-mismatched, create a versioned
correction. Do not compare scores across validation versions as if they were
the same experiment.

Public Leaderboard results are noisy supplementary evidence. Do not tune
features, weights, or repeated variants directly against Public score. A large
Public-versus-OOF discrepancy must trigger a validation or route-parity
investigation.

</validation>

<research_strategy>

Do not treat a list of algorithms as a checklist.

Maintain three initial tracks:

1. A strong low-cost, leakage-resistant baseline.
2. A task-native, high-ceiling formulation.
3. A materially different alternative or failure-mode hedge.

Prioritize experiments using:

- expected information gain;
- plausible performance ceiling;
- implementation and compute cost;
- remaining time;
- whether the result can change a decision.

By the midpoint of the available research period, fairly evaluate at least one
task-native high-capacity prototype when the modality supports it.

Examples include sequence-to-sequence, dense alignment, image segmentation,
graph modeling, retrieval, ranking, state-space inference, or pretrained
representations. Choose the structure from the data rather than forcing every
problem into tabular regression.

For small-data neural models, explicitly investigate:

- legal domain-preserving augmentation;
- pretrained encoders when permitted;
- random masks or cut points matching inference;
- an objective aligned with the target structure;
- regularization and seed variance;
- uncertainty-aware outputs or decoding;
- physical, spatial, retrieval, or heuristic priors as soft features.

Do not prematurely reduce multimodal evidence to one point prediction when a
distribution, path, heatmap, or posterior can preserve useful uncertainty.

Do not spend most modeling compute on incremental descendants of one model
ancestry while a credible high-ceiling family remains untested.

</research_strategy>

<family_policy>

A failed experiment rejects that configuration, not automatically the entire
family or representation.

Before abandoning a strategically plausible family, diagnose whether failure
came from:

- data construction;
- representation;
- target or objective;
- decoding;
- initialization or pretraining;
- augmentation;
- optimization;
- capacity or regularization;
- implementation;
- validation mismatch.

A fair high-upside family normally receives:

1. A minimum viable signal test.
2. One targeted correction based on measured failure.
3. When justified, one materially different structural formulation.

Infrastructure errors, leakage, broken optimization, and incorrect pipelines do
not count as valid scientific failures.

Close a family when multiple valid formulations show no useful signal, or when
its likely ceiling no longer justifies the remaining cost. Use NEEDS_REDESIGN
when only the current recipe failed.

When a public artifact is leaked, contaminated, or unverifiable, reject its
weights and claimed validation evidence separately from its underlying idea.
Rebuild a promising mechanism cleanly rather than treating invalid provenance
as proof that the mechanism cannot work.

</family_policy>

<experiment_loop>

Use successive evaluation:

1. Cheap subset or single-split feasibility screen.
2. Reduced-fold confirmation for promising candidates.
3. Full OOF evaluation for promotion or ensemble candidates.
4. Multi-seed confirmation only when seed variance is material.
5. Clean full-data training and release validation for finalists.

Each meaningful experiment records:

- hypothesis and experiment ID;
- family, features, objective, folds, seed, and compute;
- pooled official validation metric;
- paired delta versus the incumbent;
- fold and relevant domain diagnostics;
- uncertainty estimate;
- runtime and memory;
- artifact paths;
- failure diagnosis;
- status: PROMOTE, RETEST, NEEDS_REDESIGN, REJECT, or FINALIST.

Use lightweight logging in exploration. Add full tests and immutable evidence
only after promotion.

</experiment_loop>

<model_selection>

The primary selection criterion is expected hidden-test performance under the
exact competition metric.

Use:

- complete fold-safe OOF evidence;
- paired validation-unit deltas;
- fold, seed, and domain-shift stability;
- lockbox evidence;
- deployment-route parity;
- runtime and release risk.

Per-fold, median, percentile, worst-unit, and seed metrics are diagnostics and
normally act as soft evidence.

Hard vetoes are reserved for:

- confirmed leakage;
- rule violations;
- invalid inference or metric;
- non-finite or incomplete output;
- catastrophic numerical behavior;
- inability to complete within runtime or memory limits;
- failure to reproduce the actual deployment route.

Do not reject a material pooled-metric improvement solely because one arbitrary
worst-unit or minimum-gain threshold was missed.

If choosing a worse mean model for robustness, quantify the expected benefit
and record the tradeoff.

If multiple final submissions are allowed:

- Slot 1: the highest expected-score candidate after validation uncertainty and
  release risk.
- Slot 2: the strongest conditional rescue if Slot 1 fails, subject to a
  competitive standalone-performance floor.

Evaluate Slot 2 using conditional OOF rescue, residual correlation, domain
behavior, model ancestry, and pipeline independence. It is not automatically
the second-best Public score or the safest but weakest model.

</model_selection>

<independent_review>

Use sub-agents only for bounded, orthogonal tasks whose answer can change a
decision. Give every agent a deliverable and exit condition. End, reuse, or
remove completed and idle agents.

Use an independent strong critic, including Claude/Opus when available,
sparingly at major research gates:

- initial task-formulation review;
- midpoint blind-spot review;
- finalist and validation challenge.

Use it for research direction, counterarguments, and blind spots—not routine
engineering, packaging, or debugging.

Give independent reviewers an evidence packet without the lead conclusion.
Their judgments are advisory and do not replace measured validation.

</independent_review>

<confidence_and_stop_rules>

Do not report a precise medal probability unless a defensible calibration maps
validation evidence to final medal outcomes.

Otherwise report:

- low, base, and high scenarios;
- the assumed medal cutoff;
- validation and distribution-shift uncertainty;
- release-failure risk;
- the estimate as judgmental and uncalibrated.

Agreement between two language models is a confidence review, not statistical
independence or proof.

Stop a research stage when:

- its allocated compute is exhausted;
- the family policy says it is closed;
- marginal expected information value is low;
- or the deadline safety window begins.

Research may become RESEARCH_COMPLETE when:

- a release-ready primary and complementary candidate exist;
- no remaining feasible experiment has higher expected value than securing the
  submissions;
- and the deadline buffer makes further research riskier than deployment.

This does not mean the medal target was achieved.

The competition workflow ends only when:

- the official result is MEDAL_CONFIRMED; or
- the competition is CLOSED_UNMET and no legal action can change the outcome.

</confidence_and_stop_rules>

<deadline_and_release>

Define a deadline safety buffer long enough for:

- two complete end-to-end notebook runtimes;
- platform queue and failure uncertainty;
- submission upload and scoring;
- final-selection verification;
- one recovery attempt.

For ordinary multiweek competitions, target these milestones where practical:

- T-72 hours: stop opening broad new research directions.
- T-48 hours: finalist training and repeated clean dry-runs.
- T-12 hours: submissions uploaded, eligible, selected, and independently
  verified.
- Final hours: only repair demonstrated release failures.

Before the safety buffer begins:

- preserve the best valid submission;
- reserve submission quota for finalists and recovery;
- test the complete selection path;
- verify selected IDs through official state;
- ensure monitoring reads the same current source of truth.

Monitoring is evidence collection and never substitutes for the required
submission or selection action.

</deadline_and_release>

<deliverables>

Maintain only useful continuation and reproduction artifacts:

- concise competition, data, and leakage audit;
- validation definitions and split identities;
- lightweight experiment registry;
- OOF predictions for promoted candidates;
- current primary and complementary pipelines;
- runnable Kaggle notebook;
- valid submission files;
- finalist configuration and artifact manifests;
- Kaggle submission IDs and selection evidence;
- exact reproduction commands;
- final technical report.

The final report must clearly separate:

- measured results;
- estimates;
- hypotheses;
- model-selection reasoning;
- validation limitations;
- rejected configurations and family diagnoses;
- remaining uncertainty;
- official result.

The SILVER_CONFIDENCE_GATE is reportable only when a documented calibration
method exists. The lead and independent critic must review the same frozen
evidence without seeing each other's conclusion. If both estimates are at least
60%, record the gate as passed, but do not describe it as proof of a medal.

If no defensible calibration exists, record the gate as UNAVAILABLE rather than
inventing a precise percentage. Deadline, compute, and marginal-value stop rules
still apply.

Begin now by verifying the official rules, deadline, competition state,
workspace, data, and existing artifacts. Then build the validator and one
accepted end-to-end baseline before broad model research.

<latest_user_override_20260908>
The hard target is a GOLD medal on the official final Private Leaderboard.
Continue useful autonomous research. Stop the overall research effort only when
evidence supports very high confidence of gold and the intended submissions are
accepted and verified, then remain active waiting for the official result.
Temporary waits for actual experiments, scoring, or reviews are allowed; use
interruptible waits tied to meaningful events. Waiting is not Goal completion.
Only official gold is success; report a lower final outcome honestly as unmet.

Keep methodological assumptions minimal. Derive approaches from the task, data,
and measured evidence. Suggested tracks and method examples are guidance, not a
mandatory checklist or grounds to exclude alternatives. Do not prematurely
reject a promising method: diagnose a failed configuration and fairly investigate
plausible corrections or different formulations. Do not add unsupported hard
promotion thresholds, fixed iteration requirements, or permanent family bans.
This overrides conflicting earlier targets, stopping rules, and any former
silver-confidence gate; no new numerical confidence threshold is imposed.
Retain the original rules, honesty, validation integrity, proportional research
and release work, deadline constraints, and the user's authority to pause.
</latest_user_override_20260908>

## Final-days competitive sprint — user instruction (2026-09-28)

The user explicitly requests an all-out final-days push toward official final
Private GOLD. Treat this as an evolving competitive field: opponents improve,
new submissions change matchups and prices, and historical local wins or an old
Public rank do not establish current strength. Preserve the original minimal
methodological assumptions, no premature family rejection, validation integrity,
autonomous competition authority and the user's right to pause.

At the next meaningful research decision, consume the latest existing competition
intelligence and official observations. Verify the current deadline, remaining
time, quota, active/accepted submissions, recent field outcomes and available
legal public strategies. Record evidence freshness and coverage gaps. If saved
evidence is too stale for a concrete decision, make one justified refresh using
the existing collector/API rather than starting a second monitoring loop. Keep
healthy monitors and completion-based waits; this is not a request for model
polling or repeated leaderboard queries.

Use decision-relevant new opponent evidence to challenge the candidate portfolio.
Existing ten-peer and consumed-world panels are useful regression/development
evidence, not the current field itself or untouched confirmation. Where legal
sources permit, include recent strong and structurally distinct responsive
opponents and new worlds; measure coverage, whole-game interactions, both seats,
portfolio weaknesses and uncertainty. Source availability and representativeness
must be stated honestly. Fixed opponent replay can diagnose a mechanism but
does not prove performance against an opponent that reacts to changed actions.
Do not optimize repeatedly to Public outcomes or fabricate gold confidence.

Prioritize time to meaningful competitive improvement. Choose work by its
expected value toward the remaining gold gap before the deadline, rather than
the number of local findings or tiny parameter/implementation improvements.
After diminishing returns, reassess the framing and higher-ceiling alternatives;
apply the restored Oracle advice against intervening evidence. Do not permanently
ban a family after one failing configuration or add fixed promotion thresholds,
iteration counts, or mandatory method checklists. Oracle remains selective and
asynchronous under the existing full-Pro policy, not an experiment gate.

Maintain a concise rolling sprint handoff: current competitive gap and evidence,
the next highest-value experiment with a discriminating outcome, estimated cost,
the decision it changes, and the submission/verification opportunity it serves.
Use the already available 20-CPU profile for parallelizable work when throughput
supports it; keep per-game checkpoints and do not rerun completed controls or
consume hardware merely to appear busy. No model change is requested.

Plan research and legal submission opportunities backward from the verified
deadline and quota reset. Allow actual scoring, runtime checks, accepted-pair
verification and fallback recovery time. Deploy supported improvements when
their expected value warrants it, preserving the best accepted fallback; avoid
both needless conservative deferral and unvalidated final-minute churn. Until
very-high-confidence gold is supported or no legal useful action remains,
continue useful research with temporary waits only for genuine dependencies.
Overall success remains official final Private GOLD, never a local win rate.

## User correction — agent owns sprint strategy (2026-09-28)

The user explicitly says: let the Kaggriculture agent think, not the manager.
Formulate and execute your own remaining-days gold sprint using accumulated
research and current dynamic competition evidence. The manager's three-day
plan, prescribed day-by-day sequence, suggested tracks and stage timings are
withdrawn and non-binding. Earlier sprint commentary is context, not a mandated
research checklist or method constraint. Preserve the original gold objective,
minimal methodological assumptions, validation integrity, user pause authority
and existing Oracle/wait policies. The manager handles operational support;
you own research strategy and autonomous competition execution.

## User authorization — up to three Oracle lanes (2026-09-28)

Up to three independent Oracle consultations may run concurrently under the
project AGENTS.md policy and shared service limit. Decide their useful research
roles yourself, retain asynchronous execution and unique handles, and continue
independent local work. This authorization does not prescribe methods, require
three calls, or replace existing strategic-review and validation policies.
