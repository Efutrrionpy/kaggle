![Kaggle portfolio: 0 gold, 1 silver, 1 bronze; 2 medals across 3 competitions. Kaggriculture silver, ROGII bronze, Biohub no medal.](assets/research-cover.svg)

Three applied machine-learning studies: geological sequence prediction,
3D cell tracking and competitive resource planning. Explore the methods,
official results, reproducible components and recorded resource use.

| Competition | Final Private result | Method | Study |
|---|---|---|---|
| **Kaggriculture · Silver** | **246 / 10,148** · **4644.3** BT score | Demonstration-derived programs + economic routing + service planning | [Methods](Kaggriculture/RESEARCH.md) · [Results](Kaggriculture/RESULTS.md) · [Costs](Kaggriculture/COSTS.md) |
| **ROGII · Bronze** | **444 / 6,191** · **8.889** RMSE ↓ | CatBoost + geological projection + HMM alignment | [Methods and results](ROGII/README.md) |
| **Biohub · No medal** | **1,714 / 4,020** · **0.91051** score ↑ | Temporal 3D U-Nets + node Transformers + graph optimization | [Methods](Biohub/README.md) · [Results](Biohub/FINAL_RESULTS.md) · [Costs](Biohub/COSTS.md) |

**Medal tally: 0 Gold · 1 Silver · 1 Bronze.** Two awards across three
competitions; each competition is counted once, not once per submission.
The unmedaled Biohub entry does not add to the award count.
[Underlying result records](assets/portfolio-results.json) were reconciled on
22 October 2026. Metrics have different meanings and are not compared across studies.

## Kaggriculture — competitive planning

Two deterministic controllers turn public demonstration programs into
state-responsive production, investment and service decisions. FlexService
explicitly accounts for wages, cash flow, feed and delivery. On one prospective
local panel it scored **677 / 768** points versus **622 / 768** for AdaptiveMilk;
the final Private score was **4644.3**, with a Silver medal.

Both exact submitted inference closures are included. Four documented
confirmation batches used **18 CPU workers**, running **7,936 games in 3.715
batch wall-hours** in total. This is a measured subset, not lifetime compute.
Assistant usage and missing monetary totals are separately labeled in the
[cost report](Kaggriculture/COSTS.md).

[Read the study →](Kaggriculture/README.md) · [Reproduce](Kaggriculture/REPRODUCE.md) · [Code](Kaggriculture/strategies/)

## ROGII — wellbore geology prediction

A **290-feature CatBoost regressor** combined with physical path estimates and
HMM alignment predicts unseen well tails. The final blend achieved **8.889
Private RMSE**, improving on a candidate with the stronger Public score.
The published code covers the core alignment, projection, validation and
ensemble operations; it is not a complete reproduction of the original score.
A project-wide resource-cost total is **untracked in this archive**.

[Read the study →](ROGII/README.md) · [Methodology](ROGII/docs/methodology.md) · [Code](ROGII/src/rogii/)

## Biohub — cell tracking during development

Experiments combined **temporal 3D U-Nets, node Transformers and graph
optimization** to reconstruct cell lineages. The best selected Private score
was **0.91051**. Improvements in intermediate objectives did not consistently
improve complete graphs; the motion variant improved Public but reduced
Private performance. One preserved visible notebook run took **24.24 minutes
on a Kaggle T4**, including its motion refinement; this is not total training
time. [Biohub's cost report](Biohub/COSTS.md) separately records assistant
usage and untracked project payments.

[Read the study →](Biohub/README.md) · [Final results](Biohub/FINAL_RESULTS.md) · [Code](Biohub/src/csv_overlay.py)

---

Official outcomes are separated from local validation. Cost records distinguish
observed execution and cached model input from waiting, estimates and actual
payments; unavailable totals are labeled rather than inferred.
