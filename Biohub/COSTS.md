# Biohub: recorded resources and costs

This is a **partial measured-usage account, not a project invoice**.
It combines an existing main-thread token snapshot with saved execution
measurements. Unknown payments and missing compute totals are **untracked,
not zero**. No training or benchmark was rerun to create this account.

## Model interaction usage

The sanitized local controller index (`native-request-v2`) covers the main
thread from **2026-07-29 09:50:43 UTC through 2026-10-22 11:16:07.687 UTC**.
The recorder was established on October 2 and backfilled earlier history.
The period includes research and subsequent analysis/reporting, not just the
competition window. Subordinate-agent and advisor coverage is incomplete;
current open work and later activity are outside the fixed snapshot.

| Interaction model | Input, including cache | Cached subset | Output, including reasoning | Total tokens |
|---|---:|---:|---:|---:|
| gpt-5.6-sol | 4,326,404,554 | 4,262,205,568 | 6,902,781 | 4,333,334,862 |
| gpt-6-astra | 736,751,313 | 714,758,016 | 3,737,181 | 740,488,494 |
| gpt-6-sol | 212,111,588 | 206,895,872 | 1,226,624 | 213,338,212 |
| gpt-6.1-sol | 30,400,412 | 28,392,832 | 227,113 | 30,627,525 |
| **Total** | **5,305,667,867** | **5,212,252,288** | **12,093,699** | **5,317,789,093** |

There were **31,641 recorded request-token events**. Input includes **93,415,579
uncached tokens**; output includes **3,739,522 reasoning tokens**. Cache and
reasoning are subsets, not additional counts. Two initial events report only a
total, leaving **27,527 tokens unattributed to input/output**; this explains the
table's total reconciliation. Repeated cached context dominates the volume:
these are not billions of distinct text tokens or neural-training examples.

The index uses native per-request counters rather than adding cumulative
counters; this snapshot has no cumulative-difference fallback events.
[Machine-readable aggregate and accounting semantics](results/resource_usage.json).

## Execution, allocation and waiting are different

| Existing record | Measurement | Scope |
|---|---:|---|
| Selected visible notebook, Kaggle NVIDIA T4 | **1,454.32 s / 24.24 min** | One execution; includes **44.38 s** overlay, not an additional run |
| Preserved motion-component replay, one CPU allocation | **13.72 s**, peak RSS **375,256 KiB** | Visible predictions; no labels or upstream neural inference |
| Completed main-thread turns | **399.28 h** wall time | Includes **295.65 h** of direct tool waits; excludes unclosed turns |
| Narrow scheduler subset | **1,098.048 allocated CPU-core-seconds**, **0.153 s** queue wait | 99 CPU closeout jobs on October 2 only |

Notebook/process elapsed time includes I/O and is not GPU-active or CPU-busy
time. Tool waits may include awaited computation, queues or idle intervals;
the remaining **103.64 h** of turn wall time is also **not verified model
compute**. Allocation duration is not measured CPU utilization. None of these
partial records establishes total research CPU/GPU hours, training time,
all waiting time or electricity use; those totals remain **untracked**.

The visible-run source is [final artifacts](results/final_artifacts.json);
the separate CPU replay source is [reproduction checks](results/reproduction_checks.json).

## Monetary cost

Project-attributable **actual payments, subscription allocation and cloud
charges are untracked**. No API-list-price estimate is presented, and API
prices are not treated as subscription charges. Hardware ownership and an
execution duration do not establish electricity or depreciation costs.
The public package contains only the sanitized aggregates, not private usage
databases, transcripts, billing records or account identifiers.
