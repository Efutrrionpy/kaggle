# Kaggriculture Sources and Licenses

| Material | Origin |
|---|---|
| `strategies/*/engine_core.py` | Selected worker, animal, and hiring primitives from Kaggle Environments 1.32.7; accompanying Apache-2.0 license and notice retained |
| Other submitted Python modules | Project implementations of resource feedback, routing, investment evaluation, and policy composition |
| Action programs, resource targets, and routing parameters | Compiled from publicly downloadable Kaggriculture demonstration episodes of submission 56614976 |
| Experiment tables and research text | Project-generated comparisons and analysis |
| Opponent controllers | Source fingerprints provided; implementations without established redistribution rights are not included |

The demonstrations supplied offline policy parameters, not the original
author's private controller code. Selected episodes and artifact hashes are
listed in [source_provenance.json](manifests/source_provenance.json).
Descendant policies may share an ancestor and should not be treated as
independent opponent families.

The upstream engine is [Kaggle Environments](https://github.com/Kaggle/kaggle-environments).
Each submitted strategy directory includes its engine license and notice.
The project's own material does not relicense those external components.

Competition access and replay use are governed by the
[Kaggriculture rules](https://www.kaggle.com/competitions/kaggriculture/rules).
Full opponent source, raw replay collections, and account credentials are
outside this published research subset.
