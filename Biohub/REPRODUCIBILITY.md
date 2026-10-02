# Biohub Reproducibility

## Published implementation

[src/csv_overlay.py](src/csv_overlay.py) implements the submitted collective-motion
refinement: a 12 μm search radius, up to eight predecessor candidates, and
32 neighboring support pairs for robust median motion. It changes eligible
ordinary continuation edges without adding nodes or modifying existing divisions.

The data-free checks use synthetic graphs:

```sh
python3 tools/verify_archive.py
python3 -m venv .repro-venv
.repro-venv/bin/pip install -r requirements-test.txt
PYTHONDONTWRITEBYTECODE=1 .repro-venv/bin/python -m pytest tests -p no:cacheprovider -v
```

To apply the refinement to a legally obtained baseline prediction:

```sh
.repro-venv/bin/python src/csv_overlay.py baseline.csv replay.csv --report replay_receipt.json
```

The output destination must not already exist. The recorded visible replay
matched the selected motion output exactly; its measurements are in
[reproduction_checks.json](results/reproduction_checks.json).

## Neural models

| Model | Checkpoint source |
|---|---|
| Primary temporal 3D U-Net / node Transformer | [Tracking support pack, 50 epochs](https://www.kaggle.com/datasets/pilkwang/biohub-tracking-support-pack-50ep-v1) |
| Secondary temporal 3D U-Net / node Transformer | [Seed 314159 checkpoint](https://www.kaggle.com/datasets/pilkwang/biohub-temporal-unet3d-seed314159-v1) |
| Auxiliary DeepCenter model | [3D U-Net center prior](https://www.kaggle.com/datasets/pilkwang/biohub-deepcenter-unet3d-center-prior-v1) |

Exact checkpoint sizes and hashes are in
[final_artifacts.json](results/final_artifacts.json). These identify the
recorded versions rather than whichever version a dataset currently serves.
The neural pipeline was adapted from
[nusrati/0-940](https://www.kaggle.com/code/nusrati/0-940).

The accepted notebook versions were
`efnutrrionpy/biohub-nusrati0940-private-replay-v1/1` and
`efnutrrionpy/biohub-fixed-collective-motion-v1/1`.
These notebooks were private, so downloading them requires the owner's access.
Their full source and external components are not reproduced in this repository.

## Environment and scope

The accepted motion run used a Kaggle T4 with Python 3.12.13. Its overlay
dependencies were NumPy 2.0.2, SciPy 1.16.3, and Polars 1.42.0, recorded in
[requirements-overlay.txt](requirements-overlay.txt). This is the overlay
environment, not a complete specification of Torch, CUDA, and the neural notebook.

Full notebook inference took 1,454.3 seconds on the visible run, including
44.4 seconds for the overlay. It produced 234,368 rows and changed 20 edges.
Visible-output parity and runtime do not reproduce the official hidden-data score.

The published code reproduces the motion component and synthetic checks.
Complete training and inference also require the original neural source,
checkpoints, and competition data. [Source attribution](THIRD_PARTY_NOTICES.md)
documents those dependencies and their distribution boundaries.
