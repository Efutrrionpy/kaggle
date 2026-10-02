import csv
import importlib.util
from pathlib import Path

import numpy as np
import pytest

SPEC = importlib.util.spec_from_file_location('overlay_under_test', Path(__file__).parents[1] / 'src/csv_overlay.py')
overlay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(overlay)


def rows(dataset='unseen_movie'):
    return [
        ['0', dataset, 'node', '10', '0', '1', '2', '3', '-1', '-1'],
        ['1', dataset, 'node', '20', '1', '1', '2', '3', '-1', '-1'],
        ['2', dataset, 'node', '30', '0', '1', '2', '4', '-1', '-1'],
        ['3', dataset, 'edge', '-1', '-1', '-1', '-1', '-1', '10', '20'],
    ]


def write(path, data):
    with path.open('x', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(overlay.CSV_COLUMNS)
        writer.writerows(data)


def read(path):
    with path.open(newline='') as stream:
        return list(csv.reader(stream))


def test_no_support_identity_and_determinism(tmp_path):
    source = tmp_path / 'input.csv'
    write(source, rows())
    initial = source.read_bytes()
    reports = [overlay.apply_motion_csv(source, tmp_path / f'out{i}.csv') for i in range(2)]
    assert reports[0]['changed_edges'] == reports[1]['changed_edges'] == 0
    assert (tmp_path / 'out0.csv').read_bytes() == (tmp_path / 'out1.csv').read_bytes() == initial
    assert source.read_bytes() == initial


def test_only_source_field_changes_and_arbitrary_dataset_names(tmp_path, monkeypatch):
    def fixed_edit(stem, table, cfg):
        return np.array([[30, 20]]), {20: 30}, {'queries': 1, 'supported_queries': 1}
    monkeypatch.setattr(overlay, 'motion_arrays', fixed_edit)
    source, destination = tmp_path / 'input.csv', tmp_path / 'output.csv'
    data = rows('never_seen_abc')
    write(source, data)
    result = overlay.apply_motion_csv(source, destination)
    data[-1][-2] = '30'
    assert read(destination) == [overlay.CSV_COLUMNS] + data
    assert result['changed_edges'] == 1


def test_dynamic_multiple_datasets(tmp_path):
    data = rows('unknown_a') + rows('unknown_b')
    for i, row in enumerate(data):
        row[0] = str(i)
    source = tmp_path / 'input.csv'
    write(source, data)
    result = overlay.apply_motion_csv(source, tmp_path / 'out.csv')
    assert set(result['datasets']) == {'unknown_a', 'unknown_b'}
    assert result['rows'] == 8


@pytest.mark.parametrize('defect', ['row_id', 'node_id', 'dangling', 'time', 'negative', 'row_type', 'split_dataset'])
def test_rejects_invalid_input_without_publishing(tmp_path, defect):
    data = rows()
    if defect == 'row_id':
        data[1][0] = '5'
    elif defect == 'node_id':
        data[2][3] = '10'
    elif defect == 'dangling':
        data[-1][-2] = '999'
    elif defect == 'time':
        data[1][4] = '2'
    elif defect == 'negative':
        data[0][5] = '-1'
    elif defect == 'row_type':
        data[1][2] = 'mystery'
    else:
        data += rows('second') + rows()
        for i, row in enumerate(data):
            row[0] = str(i)
    source, destination = tmp_path / 'in.csv', tmp_path / 'out.csv'
    write(source, data)
    original = source.read_bytes()
    with pytest.raises((ValueError, RuntimeError)):
        overlay.apply_motion_csv(source, destination)
    assert not destination.exists()
    assert source.read_bytes() == original


def test_no_overwrite(tmp_path):
    source, destination = tmp_path / 'in.csv', tmp_path / 'out.csv'
    write(source, rows())
    write(destination, rows('existing'))
    old = destination.read_bytes()
    with pytest.raises(ValueError):
        overlay.apply_motion_csv(source, destination)
    with pytest.raises(ValueError):
        overlay.apply_motion_csv(source, source)
    assert destination.read_bytes() == old


def test_no_edge_graph(tmp_path):
    source = tmp_path / 'in.csv'
    write(source, rows()[:3])
    result = overlay.apply_motion_csv(source, tmp_path / 'out.csv')
    assert result['changed_edges'] == 0


def test_existing_division_unchanged_without_support(tmp_path):
    data = rows()
    data[2][4] = '1'
    data.append(['4', 'unseen_movie', 'edge', '-1', '-1', '-1', '-1', '-1', '10', '30'])
    source = tmp_path / 'in.csv'
    write(source, data)
    overlay.apply_motion_csv(source, tmp_path / 'out.csv')
    assert read(source) == read(tmp_path / 'out.csv')
