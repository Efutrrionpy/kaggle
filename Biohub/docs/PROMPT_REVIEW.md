# Research Design Review

The original and revised research specifications are preserved in
[ORIGINAL_DESIGN.md](../prompts/ORIGINAL_DESIGN.md) and
[CURRENT_DESIGN.md](../prompts/CURRENT_DESIGN.md).
This appendix records research-process lessons; the main model and result
analysis is in [the research report](../RESEARCH_HISTORY.md).

## Lessons from the experiments

**Evaluate the complete prediction pipeline.** Five-frame features and pair
residuals improved local objectives without consistently improving tracking
graphs. Future model selection should trace which scored events a representation
changes, including division recovery, ownership conflicts, and lost continuations.

**Match validation claims to upstream exposure.** Excluding movies from a
residual head does not isolate a detector or crop model already trained on them.
Complete-pipeline grouping matters more than the label applied to a small head split.

**Prioritize discriminating experiments.** The original specification already
called for lightweight prototypes and method openness. Added numerical vetoes
and extensive preparation sometimes delayed useful model comparisons. A failed
configuration should motivate diagnosis rather than permanent rejection of a family.

**Use attributable external evidence.** The leading solutions offered concrete
alternatives in supervision, candidate coverage, and learned-score/decoder
integration. Incomplete search or inaccessible page rendering was insufficient
evidence that methods had not been disclosed.

The final specification revision emphasized these behaviors without prescribing
a model family. No controlled prompt ablation was performed, so it does not
establish that wording changes would have improved the competition result.
