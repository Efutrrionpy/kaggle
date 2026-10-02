from __future__ import annotations
from collections import Counter
import time
import numpy as np
import polars as pl
from scipy.spatial import cKDTree

FIXED_CONFIG = {'scale_zyx_um': [1.625, 0.40625, 0.40625], 'candidate_radius_um': 12.0, 'max_candidates': 8}

def nearest(tree: cKDTree, points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    distance, index = tree.query(points, k=1)
    return (np.asarray(distance), np.asarray(index, dtype=np.int64))

def motion_arrays(stem: str, rows: pl.DataFrame, cfg: dict):
    started = time.monotonic()
    node_rows = rows.filter(pl.col('row_type') == 'node').sort('node_id')
    edge_rows = rows.filter(pl.col('row_type') == 'edge')
    ids = node_rows['node_id'].to_numpy().astype(np.int64)
    t = node_rows['t'].to_numpy().astype(np.int64)
    xyz = node_rows.select('z', 'y', 'x').to_numpy().astype(np.float64)
    pos = xyz * np.asarray(cfg['scale_zyx_um'])[None, :]
    if len(np.unique(ids)) != len(ids):
        raise RuntimeError(f'Duplicate node IDs: {stem}')
    index = {int(node_id): i for i, node_id in enumerate(ids)}
    edges = edge_rows.select('source_id', 'target_id').to_numpy().astype(np.int64)
    if any((int(a) not in index or int(b) not in index for a, b in edges)):
        raise RuntimeError(f'Dangling edge: {stem}')
    indegree, outdegree = (Counter(edges[:, 1].tolist()), Counter(edges[:, 0].tolist()))
    if max(indegree.values(), default=0) > 1 or max(outdegree.values(), default=0) > 2:
        raise RuntimeError(f'Anchor degree invariant failed: {stem}')
    by_t = {int(frame): np.flatnonzero(t == frame) for frame in np.unique(t)}
    trees = {frame: cKDTree(pos[rows]) for frame, rows in by_t.items()}
    support = {}
    radius = float(cfg['candidate_radius_um'])
    for frame in sorted(by_t):
        if frame - 1 not in by_t:
            continue
        parents, children = (by_t[frame - 1], by_t[frame])
        forward_distance, forward = nearest(trees[frame], pos[parents])
        _, reverse = nearest(trees[frame - 1], pos[children])
        pairs = []
        for local_parent, (distance, local_child) in enumerate(zip(forward_distance, forward, strict=True)):
            if distance <= radius and reverse[int(local_child)] == local_parent:
                p, q = (int(parents[local_parent]), int(children[int(local_child)]))
                pairs.append((p, q))
        if pairs:
            support[frame] = np.asarray(pairs, dtype=np.int64)
    queries = []
    old_parent = {int(child): int(parent) for parent, child in edges}
    for child_id, parent_id in sorted(old_parent.items(), key=lambda row: row[0]):
        child, parent = (index[child_id], index[parent_id])
        if t[child] != t[parent] + 1 or indegree[child_id] != 1 or outdegree[parent_id] != 1:
            continue
        frame = int(t[child])
        if frame - 1 not in trees:
            continue
        local = trees[frame - 1].query_ball_point(pos[child], radius)
        candidates = [int(by_t[frame - 1][int(i)]) for i in local]
        candidates.sort(key=lambda p: (float(np.linalg.norm(pos[child] - pos[p])), int(ids[p])))
        candidates = candidates[:int(cfg['max_candidates'])]
        if parent not in candidates:
            continue
        pairs = support.get(frame)
        motion = None
        used_support = 0
        if pairs is not None:
            excluded_parents = set(candidates)
            keep = (pairs[:, 1] != child) & ~np.isin(pairs[:, 0], list(excluded_parents))
            available = pairs[keep]
            if len(available) >= 32:
                order = np.lexsort((ids[available[:, 1]], np.linalg.norm(pos[available[:, 1]] - pos[child], axis=1)))
                chosen = available[order[:32]]
                motion = np.median(pos[chosen[:, 1]] - pos[chosen[:, 0]], axis=0)
                used_support = 32
        zero_scores = np.asarray([np.linalg.norm(pos[child] - pos[p]) for p in candidates])
        motion_scores = None if motion is None else np.asarray([np.linalg.norm(pos[child] - pos[p] - motion) for p in candidates])
        queries.append({'child': child, 'old_parent': parent, 'candidates': np.asarray(candidates, dtype=np.int64), 'zero_scores': zero_scores, 'motion_scores': motion_scores, 'support': used_support, 'motion': np.zeros(3) if motion is None else motion})

    def choose(arm: str) -> dict[int, int]:
        forward = {}
        reverse = {}
        for qn, query in enumerate(queries):
            scores = query[arm + '_scores']
            if scores is None:
                continue
            ranked = sorted(range(len(scores)), key=lambda j: (float(scores[j]), int(ids[query['candidates'][j]])))
            forward[qn] = int(query['candidates'][ranked[0]])
            for candidate, score in zip(query['candidates'], scores, strict=True):
                key = (float(score), int(ids[query['child']]))
                p = int(candidate)
                if p not in reverse or key < reverse[p][0]:
                    reverse[p] = (key, qn)
        output = {}
        for qn, candidate in forward.items():
            query = queries[qn]
            if candidate != query['old_parent'] and outdegree[int(ids[candidate])] == 0 and (reverse[candidate][1] == qn):
                output[int(ids[query['child']])] = int(ids[candidate])
        return output
    zero_changes, motion_changes = (choose('zero'), choose('motion'))

    def edited(changes: dict[int, int]) -> np.ndarray:
        result = edges.copy()
        for i, (parent_id, child_id) in enumerate(result):
            if int(child_id) in changes:
                result[i, 0] = changes[int(child_id)]
        indeg, outdeg = (Counter(result[:, 1].tolist()), Counter(result[:, 0].tolist()))
        if len(result) != len(edges) or max(indeg.values(), default=0) > 1 or max(outdeg.values(), default=0) > 2:
            raise RuntimeError(f'Edited graph invariant failed: {stem}')
        changed_sources = set(changes.values())
        if any((outdegree[p] != 0 for p in changed_sources)):
            raise RuntimeError(f'Edit used non-free parent: {stem}')
        return result
    zero_edges, motion_edges = (edited(zero_changes), edited(motion_changes))
    return (motion_edges, motion_changes, {'queries': len(queries), 'supported_queries': sum((q['support'] == 32 for q in queries))})

"""I/O layer appended to the mechanically extracted, frozen numerical core."""
import csv
import hashlib
import itertools
import json
import os
from pathlib import Path
import resource
import tempfile

CSV_COLUMNS = ['id', 'dataset', 'row_type', 'node_id', 't', 'z', 'y', 'x', 'source_id', 'target_id']


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def apply_motion_csv(source, destination):
    """Read only a complete prediction CSV; write a new CSV without overwriting."""
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve() or destination.exists():
        raise ValueError('A new, distinct destination is required')
    started = time.monotonic()
    source_hash = file_sha256(source)
    seen, report, count = set(), {}, 0
    with tempfile.TemporaryDirectory(prefix='motion-overlay-', dir=destination.parent) as directory:
        temporary = Path(directory) / 'output.csv'
        with source.open(newline='') as incoming, temporary.open('x', newline='') as outgoing:
            reader = csv.DictReader(incoming)
            if reader.fieldnames != CSV_COLUMNS:
                raise ValueError('Unexpected prediction CSV schema/order')
            writer = csv.DictWriter(outgoing, fieldnames=CSV_COLUMNS, lineterminator='\n')
            writer.writeheader()
            for dataset, group in itertools.groupby(reader, key=lambda row: row['dataset']):
                if not dataset or dataset in seen:
                    raise ValueError('Dataset blocks must be contiguous and nonempty')
                seen.add(dataset)
                rows = list(group)
                for row in rows:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError('Malformed CSV row')
                    if int(row['id']) != count:
                        raise ValueError('Nonsequential row ID')
                    count += 1
                    if row['row_type'] not in ('node', 'edge'):
                        raise ValueError('Unknown row type')
                frame = pl.DataFrame(rows).with_columns([
                    pl.col(key).cast(pl.Int64) for key in ('node_id', 't', 'z', 'y', 'x', 'source_id', 'target_id')
                ])
                nodes = frame.filter(pl.col('row_type') == 'node')
                edges = frame.filter(pl.col('row_type') == 'edge')
                if nodes.height == 0 or nodes['node_id'].n_unique() != nodes.height:
                    raise ValueError('Missing or duplicate nodes')
                if np.any(nodes.select('node_id', 't', 'z', 'y', 'x').to_numpy() < 0):
                    raise ValueError('Negative node identity/time/coordinate')
                pairs = edges.select('source_id', 'target_id')
                if pairs.unique().height != edges.height:
                    raise ValueError('Duplicate edges')
                times = dict(nodes.select('node_id', 't').iter_rows())
                if any(s not in times or t not in times or times[t] != times[s] + 1 for s, t in pairs.iter_rows()):
                    raise ValueError('Invalid or nonadjacent edge')
                motion_edges, changes, diagnostic = motion_arrays(dataset, frame, FIXED_CONFIG)
                # The wrapper may alter only the source_id of existing ordinary edges.
                expected = dict((int(t), int(s)) for s, t in motion_edges)
                if len(expected) != edges.height:
                    raise ValueError('Invalid candidate indegree')
                changed = 0
                for row in rows:
                    if row['row_type'] == 'edge':
                        parent = expected[int(row['target_id'])]
                        changed += int(parent != int(row['source_id']))
                        if parent != int(row['source_id']):
                            row['source_id'] = str(parent)
                    writer.writerow(row)
                if changed != len(changes):
                    raise ValueError('CSV action count differs from core')
                report[dataset] = {'nodes': nodes.height, 'edges': edges.height,
                                   'changed_edges': changed, **diagnostic}
                del rows, frame, nodes, edges, motion_edges, expected, changes
            if not seen:
                raise ValueError('Empty prediction CSV')
        if file_sha256(source) != source_hash:
            raise ValueError('Source changed during processing')
        # Atomic no-clobber publication on the same filesystem.
        os.link(temporary, destination)
    return {'status': 'PASS_FIXED_MOTION_OVERLAY', 'input_sha256': source_hash,
            'output_sha256': file_sha256(destination), 'rows': count,
            'datasets': report, 'changed_edges': sum(r['changed_edges'] for r in report.values()),
            'elapsed_seconds': time.monotonic() - started,
            'process_peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'ground_truth_accessed': False, 'configuration': FIXED_CONFIG}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('destination')
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    if Path(args.report).exists():
        raise ValueError('Report already exists')
    result = apply_motion_csv(args.source, args.destination)
    with Path(args.report).open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
    print(json.dumps(result, sort_keys=True))
