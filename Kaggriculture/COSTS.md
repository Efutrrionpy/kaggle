# Resource use and costs

These figures come from existing execution receipts and a read-only usage
snapshot taken on **22 October 2026 at 11:16 UTC**. No experiments were rerun
to produce cost figures. The sources have different coverage; do not add them
as if they were a complete, non-overlapping project bill.

## Recorded simulation work

Four completed confirmation batches on **30 September 2026** used **18 CPU
workers**, each with one numerical-library thread. The two final inference
policies themselves use only the Python standard library; no GPU is required.

| Batch | Games, all comparison arms | Execution wall time |
|---|---:|---:|
| AdaptiveMilk confirmation | 2,112 | 56.3 min |
| FlexService confirmation | 2,304 | 62.3 min |
| NativeDeadlines confirmation | 2,176 | 60.3 min |
| Committed first confirmation | 1,344 | 44.1 min |
| **Recorded subset** | **7,936** | **3.715 h** |

These are whole-batch execution times, including process/I/O overhead, not
sampled busy-CPU time or scheduler waiting before execution. Multiplying by
18 gives **66.87 reserved worker-hours**, not measured core utilization.
The exact CPU SKU was not recorded in these receipts. Earlier experiments,
other confirmation blocks and the complete project compute total are not
covered by this table. [Exact timings and result fingerprints](results/measured_batch_costs.json).

## Assistant-model usage

The existing controller's `native-request-v2` aggregate covers the **main
Kaggriculture assistant transcript from 11 August to 22 October 2026**.
It includes research, maintenance, monitoring and closeout—not research alone.
Token history was backfilled when accounting was installed on October 2.
Other agent/subagent transcripts and separate advisor usage are not included
unless present in this main transcript.

| Request-level quantity | Recorded tokens |
|---|---:|
| Input, including cache reads | 6,239,807,630 |
| Cached input, a subset of input | 6,106,877,184 |
| Uncached input | 132,930,446 |
| Output | 18,925,233 |
| Reasoning output, a subset of output | 5,761,432 |
| **Input + output** | **6,258,732,863** |

Repeated context and cache reads are counted on each request. These are not
billions of unique generated words or uncached tokens. Cached input is
**97.87% of recorded input**; neither cache nor reasoning is added twice.

| Recorded assistant model | Uncached input | Cached input | Output |
|---|---:|---:|---:|
| `gpt-5.6-sol` | 52,153,793 | 3,373,762,048 | 5,985,682 |
| `gpt-6-astra` | 80,776,653 | 2,733,115,136 | 12,939,551 |

These are assistant model labels from the usage records, **not the farming
controllers**. The snapshot reported no cumulative-token fallback events or
incomplete breakdown events. Its small unindexed transcript tail and later
requests are excluded; no all-agent lifetime total is claimed.

## Execution versus waiting

Recorded closed assistant turns total **536.71 elapsed hours**, including
**336.53 hours while tool calls were pending**. Tool-pending time can contain
simulation, network activity or deliberate waiting. It is a subset of elapsed
time, not an additional cost. The remainder is not a measurement of inference
compute either; neither quantity is GPU-hours or billed model-hours.

Separately, the scheduler recorded **10.09 allocated CPU core-hours** and
**0.264 seconds of queue waiting** over 61 observed jobs from **October 2–22**.
That post-competition subset must not substitute for September's research
compute. Reserved core-time is not busy-core telemetry. There are **no attributed
GPU hardware observations** in this accounting table: full-project GPU time
is **untracked**, not zero. Shared hardware power totals are not assigned to
this project.

## Monetary expenditure

| Category | Attributable amount |
|---|---|
| Actual model/API payments | **Untracked** |
| Subscription cost allocated to this competition | **Untracked** |
| Local electricity and hardware cost | **Untracked** |
| External compute expenditure | **Untracked** |

No project-level payment ledger or defensible subscription allocation is
available. API list prices would not establish actual subscription payments,
so no synthetic dollar total is presented. Missing observations must not be
interpreted as free compute.

[Machine-readable snapshot](results/resource_use_20261022.json) records exact
coverage, accounting definitions and source fingerprints without private
session identifiers, local home paths or billing details.
