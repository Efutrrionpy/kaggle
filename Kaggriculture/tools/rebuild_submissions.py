"""Rebuild the two exact published agents; never upload or replace output."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import zlib

ROOT = Path(__file__).resolve().parents[1]

def digest(data): return hashlib.sha256(data).hexdigest()

def rebuild(output):
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for item in json.loads((ROOT/'manifests/final_submissions.json').read_text())['submissions']:
        folder = ROOT/item['source_directory']
        manifest = json.loads((folder/'package_manifest.json').read_text())
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode='w') as archive:
            for name, expected in sorted(manifest['files'].items()):
                assert Path(name).name == name, name
                content = (folder/name).read_bytes()
                assert digest(content) == expected, name
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = len(content), 0o644, 0
                archive.addfile(info, io.BytesIO(content))
        packed = gzip.compress(buf.getvalue(), mtime=0)
        actual = digest(packed)
        target = output/(item['name']+'.tar.gz')
        with target.open('xb') as f: f.write(packed)
        row = dict(name=item['name'], submission_id=item['submission_id'],
                   archive_sha256=actual, expected_sha256=item['archive_sha256'],
                   exact_match=actual == item['archive_sha256'], bytes=len(packed))
        results.append(row)
        if not row['exact_match']:
            raise RuntimeError(f"Member hashes match, but gzip bytes differ for {item['name']}; "
                               f"Python={sys.version.split()[0]}, zlib={zlib.ZLIB_RUNTIME_VERSION}. "
                               "Do not label this file as the exact official upload.")
    print(json.dumps(dict(status='PASS', python=sys.version.split()[0],
                          zlib=zlib.ZLIB_RUNTIME_VERSION, results=results), indent=2))

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    rebuild(parser.parse_args().output)
