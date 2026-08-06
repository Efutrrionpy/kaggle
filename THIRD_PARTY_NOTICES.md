# Third-party and competition-material notice

The internal competition workspace evaluated public Kaggle notebooks and
adapted some public mechanisms, including parts of the production V71 feature
path and an HMM smoother. The exact notebook-version redistribution licenses
were not established during this publication pass.

Therefore this repository does **not** contain:

- downloaded Kaggle notebook source;
- vendor snapshots or hash-pinned extracts from public kernels;
- production V71 CatBoost models or its public-derived feature code;
- the public-derived exact HMM implementation;
- external neural decoder or feature-packing implementations.

The README describes these components only to explain the scientific lineage
of the final ensemble. The source under `src/rogii/` is a compact, independently
curated reference subset focused on validation, Particle Filter alignment,
physical projection, metrics and fixed composition.

Kaggle, the competition host, ROGII, and public notebook authors retain their
respective rights. This repository is an independent participant case study
and is not an official Kaggle or ROGII publication.
