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
    ('phase2-source-surface-inventory', [sys.executable, 'scripts/validate-phase2-source-surface-inventory.py'], 'all 154 renderer TypeScript paths classified against the embedded hash-only baseline'),
    ('phase2-package-integrity', [sys.executable, 'scripts/validate-phase2-package.py'], 'all 214 states, 174 inventory requirements, source hashes and capture input identities'),
    ('reference-layouts', ['node', 'scripts/validate-reference.cjs'], 'one Chromium instance; all 72 states at three sizes'),
    ('demo-interactions', ['node', 'scripts/validate-interactions.cjs'], 'one Chromium page; all 29 declared demo checks'),
    ('phase2-layouts-and-interactions', ['node', 'scripts/validate-phase2.cjs'], 'three concurrent viewport pages in one Chromium process; all 642 state/size pairs and 112 demo interactions plus 462 action outcomes'),
    ('pdf-rebuild', [sys.executable, 'scripts/build-design-book.py'], 'embed all 98 PNGs and local fonts into the 104-page review book'),
    ('phase2-pdf-rebuild', [sys.executable, 'scripts/build-phase2-book.py'], 'embed every captured Phase 2 PNG and local fonts into the dynamically mapped review book'),
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
    phase2 = json.loads((ARTIFACTS / 'phase2-validation.json').read_text())
    passed = (layout['state'] == 'PASS' and layout['observations'] == 216
              and interactions['count'] == 29
              and all(c['state'] == 'PASS' for c in interactions['checks'])
              and len(PdfReader(ARTIFACTS / 'pdf/Biteaze-Windows-UI-Reference.pdf').pages) == 104
              and phase2['state'] == 'PASS' and phase2['screens'] == 214
              and phase2['observations'] == 642 and len(phase2['interactions']) == 112
              and all(c['state'] == 'PASS' for c in phase2['interactions'])
              and len(phase2['action_outcomes']) == 462 and all(c['state'] == 'PASS' for c in phase2['action_outcomes'])
              and len(PdfReader(ARTIFACTS / 'phase2-pdf/Biteaze-Windows-Phase-2-Reference.pdf').pages) == len(json.loads((ARTIFACTS / 'phase2-pdf/pdf-page-map.json').read_text())))
report = {'scope': 'FULL reference-package validation only; no app implementation or native qualification',
          'state': 'PASS' if passed else 'FAIL', 'seconds': round(time.perf_counter() - started, 3), 'steps': results}
(ARTIFACTS / 'full-reference-gate.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
sys.exit(0 if passed else 1)
