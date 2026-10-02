# Kaggriculture Reproducibility

## Submitted policies

`strategies/` contains both submitted controllers, their policy parameters,
and all inference dependencies. Inference uses the Python standard library.
The reconstruction tool checks both archive members and the original compressed
submission hashes:

```sh
python3.11 tools/verify.py
python3.11 tools/rebuild_submissions.py --output /tmp/kaggriculture-rebuilt
python3.11 tools/recompute_tables.py
```

Run these commands from this competition folder. The output directory must
not already exist. Exact compressed-byte reproduction used CPython 3.11.15
and zlib 1.3.1; different gzip implementations may produce different archive
bytes even when member files match. Recorded checks are in
[archive_checks.json](results/archive_checks.json).

## Inference interface

Each input line contains an official observation and configuration; each
output line is an action JSON object:

```sh
python3.11 -I -S strategies/flex_service/main.py < requests.jsonl > actions.jsonl
python3.11 -I -S strategies/adaptive_milk/main.py < requests.jsonl > actions.jsonl
```

Generate observations through your own local simulation. Each controller
resets its instance at step 0 and should run in a separate process.
The original experiments used `kaggle-environments==1.32.7`:

```sh
python3.11 -m venv /tmp/kaggriculture-env
/tmp/kaggriculture-env/bin/pip install kaggle-environments==1.32.7
```

The official verification episodes were 115743049 for FlexService and
115611747 for AdaptiveMilk. [Deployment checks](results/deployment_checks.json)
record action parity and runtime measurements.

## Experimental results

The published per-cell tables contain generated research outcomes.
`tools/recompute_tables.py` recalculates world/opponent/seat aggregates.
The complete original comparisons additionally require the fixed experiment
plans, opponent implementations, and engine configuration. Some opponent
assets cannot be redistributed and are represented by source fingerprints in
[research_sources.json](manifests/research_sources.json).

Rebuilding the submitted policies and recalculating result tables are supported
by this repository. Re-running every original opponent comparison requires
the original assets. Sources and licenses are described
[here](SOURCES_AND_LICENSES.md).
