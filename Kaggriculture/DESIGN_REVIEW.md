# Research Design Review

The [original specification](design/GOAL_original.md) provides the historical
research context. This appendix summarizes lessons from the measured experiments.

**Evaluate interaction, not isolated profit.** Shared markets allowed a
production improvement to benefit the opponent more. Complete games and
both-player accounting were necessary to identify this effect.

**Hold out world cohorts and diversify opponents.** Ridge and ExtraTrees
performed better on within-world OOF than on separate cohorts. Committed's
11 recovered wins were concentrated against one policy ancestor. Neither
result supported broad field generalization.

**Expand the decision horizon when constraints propagate.** NativeDeadlines
passed an immediate feasibility check but lost a later worker hire. Extending
cash-flow reasoning to the next investment decision corrected the tested mechanism.

**Compare implementable portfolios.** Per-game best-of-two selection is an
upper-bound diagnostic, not an available deployment rule. Submitted portfolio
choices must be evaluated under the competition's actual selection mechanism.

The strongest results came from complete production policies with material
and funding feedback. The remaining research gap was broader responsive-opponent
coverage and generalization beyond related policy families.
