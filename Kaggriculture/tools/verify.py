"""Offline public package integrity and syntax verification."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

if __name__=='__main__':
    expected={}
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        path=ROOT/name
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        assert path.is_file() and not path.is_symlink(),name
        assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,name
        expected[name]=digest
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS'}
    assert actual==set(expected),(actual-set(expected),set(expected)-actual)
    for name in expected:
        p=ROOT/name
        if p.suffix=='.py':ast.parse(p.read_text(),filename=name)
        if p.suffix=='.json':json.loads(p.read_text())
    print(json.dumps(dict(status='PASS',files=len(expected),scope='Hashes, complete file allowlist, Python syntax and JSON parsing; not a medal or licensing certificate.')))
