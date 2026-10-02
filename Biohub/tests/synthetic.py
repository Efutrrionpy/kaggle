"""Label-free shape and tie fixtures; never change the frozen motion policy."""
import hashlib
import time


def fixture(ns, count, frames=2, mode='line'):
    np, pl = ns['np'], ns['pl']
    rows = []
    side = int(np.ceil(count ** (1 / 3)))
    for t in range(frames):
        for i in range(count):
            if mode == 'dense':
                z, y, x = (i // (side * side)) * 3, ((i // side) % side) * 3, (i % side) * 3 + t
            else:
                z, y, x = 0, 0, i * (8 if mode == 'residual_ties' else 40) + t
                if mode == 'duplicates' and i == 1:
                    x = t
            rows.append(dict(row_type='node', node_id=t * count + i, t=t, z=z, y=y, x=x, source_id=-1, target_id=-1))
    for t in range(1, frames):
        for i in range(count):
            rows.append(dict(row_type='edge', node_id=-1, t=-1, z=-1, y=-1, x=-1, source_id=(t - 1) * count + i, target_id=t * count + i))
    return pl.DataFrame(rows)


def run_fixtures(ns, scaling=False):
    np = ns['np']
    points = np.array([[-1., 0., 0.], [1., 0., 0.], [0., -1., 0.], [0., 1., 0.], [-1., 0., 0.]])
    queries = np.array([[0., 0., 0.], [-1., 0., 0.]])
    distances, indices = ns['nearest'](ns['cKDTree'](points), queries)
    cases = [(32, 2, 'line'), (33, 2, 'line'), (40, 2, 'duplicates'), (40, 2, 'residual_ties')]
    if scaling:
        cases += [(128, 4, 'dense'), (512, 4, 'dense'), (2048, 4, 'dense'), (4096, 4, 'dense'), (64, 100, 'line')]
    result = {}
    for count, frames, mode in cases:
        name = f'{mode}-{count}x{frames}'
        rows = fixture(ns, count, frames, mode)
        started = time.monotonic()
        edges, changes, diagnostic = ns['motion_arrays'](name, rows, ns['FIXED_CONFIG'])
        elapsed = time.monotonic() - started
        # All original parents are occupied, so this fixed rule must abstain.
        expected = rows.filter(ns['pl'].col('row_type') == 'edge').select('source_id', 'target_id').to_numpy()
        if changes or not np.array_equal(edges, expected):
            raise RuntimeError('Synthetic occupied-parent invariant failed: ' + name)
        if not scaling:
            again, changes_again, diagnostic_again = ns['motion_arrays'](name, rows, ns['FIXED_CONFIG'])
            if not np.array_equal(edges, again) or changes != changes_again or diagnostic != diagnostic_again:
                raise RuntimeError('Synthetic determinism failure: ' + name)
        result[name] = {'nodes': count * frames, 'cells_per_frame': count, 'frames': frames,
                        'elapsed_seconds': elapsed, **diagnostic,
                        'edge_sha256': hashlib.sha256(edges.astype('<i8').tobytes()).hexdigest()}
    if result['line-32x2']['supported_queries'] != 0 or result['line-33x2']['supported_queries'] != 33:
        raise RuntimeError('Synthetic32-support boundary changed')
    return {'status': 'PASS_SYNTHETIC_INVARIANTS', 'raw_nearest_indices': indices.tolist(),
            'raw_nearest_distances': distances.tolist(), 'cases': result,
            'caution': 'Raw tie choices are recorded, not replaced by a new policy. Scaling cases are not a hidden-data bound.'}
