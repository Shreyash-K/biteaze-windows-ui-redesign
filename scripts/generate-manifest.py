#!/usr/bin/env python3
"""Refresh integrity metadata after intentional reference-package edits."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', 'node_modules', 'artifacts', '__pycache__', '.venv'}


def package_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(part in EXCLUDED for part in p.relative_to(ROOT).parts)
                  and p.name not in {'asset-manifest.json', '.DS_Store'}
                  and p.suffix != '.pyc')


if __name__ == '__main__':
    files = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
              'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in package_files()]
    data = {'schema_version': 1, 'scope': 'All distributed files except this self-referential manifest',
            'files': files, 'file_count': len(files), 'total_bytes': sum(f['bytes'] for f in files)}
    (ROOT / 'asset-manifest.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files': len(files), 'bytes': data['total_bytes']}))
