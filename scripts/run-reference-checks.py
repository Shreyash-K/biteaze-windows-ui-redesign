#!/usr/bin/env python3
"""Full reference-only gate payload. Run under the shared timed gate for publication."""
import json
import subprocess
import sys
import time
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / 'artifacts'
ARTIFACTS.mkdir(exist_ok=True)
steps = [
    ('package-integrity', [sys.executable, 'scripts/validate-package.py'], 'hash every distributed file; parse all coverage, PNG and PDF records'),
    ('reference-layouts', ['node', 'scripts/validate-reference.cjs'], 'one Chromium instance; all 72 states at three sizes'),
    ('demo-interactions', ['node', 'scripts/validate-interactions.cjs'], 'one Chromium page; all 29 declared demo checks'),
    ('pdf-rebuild', [sys.executable, 'scripts/build-design-book.py'], 'embed all 98 PNGs and local fonts into the 104-page review book'),
]
results = []
started = time.perf_counter()
for name, command, mechanism in steps:
    before = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, check=False)
    results.append({'step': name, 'exit_code': result.returncode,
                    'seconds': round(time.perf_counter() - before, 3), 'mechanism': mechanism})
    if result.returncode:
        break

passed = len(results) == len(steps) and all(r['exit_code'] == 0 for r in results)
if passed:
    layout = json.loads((ARTIFACTS / 'reference-validation.json').read_text())
    interactions = json.loads((ARTIFACTS / 'interaction-validation.json').read_text())
    passed = (layout['state'] == 'PASS' and layout['observations'] == 216
              and interactions['count'] == 29
              and all(c['state'] == 'PASS' for c in interactions['checks'])
              and len(PdfReader(ARTIFACTS / 'pdf/Biteaze-Windows-UI-Reference.pdf').pages) == 104)
report = {'scope': 'FULL reference-package validation only; no app implementation or native qualification',
          'state': 'PASS' if passed else 'FAIL', 'seconds': round(time.perf_counter() - started, 3), 'steps': results}
(ARTIFACTS / 'full-reference-gate.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
sys.exit(0 if passed else 1)
