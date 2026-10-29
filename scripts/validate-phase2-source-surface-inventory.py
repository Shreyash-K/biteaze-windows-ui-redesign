#!/usr/bin/env python3
"""Validate the embedded source-surface baseline; optionally check a local app clone."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / 'phase-2-remaining-screens' / 'source-surface-inventory.json'
VALID = {'phase1', 'phase2', 'shared_non_ui', 'explicit_exclusion'}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_gap_policy(gaps: object) -> None:
    """This published package claims complete renderer-surface coverage."""
    assert isinstance(gaps, list), 'known_ui_gaps must be a list'
    assert gaps == [], 'Known UI gaps must be empty for this complete reference package'


def exercise_gap_policy() -> None:
    """Prove the policy accepts an empty list and rejects a plausible non-empty one."""
    validate_gap_policy([])
    try:
        validate_gap_policy([{'source_path': 'src/renderer/example.ts', 'reason': 'probe', 'next_action': 'probe'}])
    except AssertionError:
        return
    raise AssertionError('known_ui_gaps policy probe unexpectedly accepted a non-empty list')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-root', type=Path, help='Optional private app checkout for baseline drift validation.')
    args = parser.parse_args()
    data = json.loads(INVENTORY.read_text())
    entries = data.get('entries', [])
    assert data.get('baseline_commit') == '7932bbbedabdd0cef4295919a91674f35fa815cf', 'Unexpected baseline commit'
    assert data.get('extraction', {}).get('file_count') == len(entries) == 154, 'Expected all 154 renderer TypeScript files'
    paths = [entry.get('source_path') for entry in entries]
    assert len(paths) == len(set(paths)), 'Duplicate source paths'
    for entry in entries:
        assert entry.get('classification') in VALID, f"Unclassified source: {entry.get('source_path')}"
        assert len(entry.get('sha256', '')) == 64, f"Missing source hash: {entry.get('source_path')}"
        assert isinstance(entry.get('rationale'), str) and entry['rationale'], f"Missing rationale: {entry.get('source_path')}"
        assert isinstance(entry.get('state_ids'), list), f"Missing state IDs: {entry.get('source_path')}"
    phase2_ids = {row['id'] for row in json.loads((ROOT / 'phase-2-remaining-screens' / 'screen-manifest.json').read_text())}
    for entry in entries:
        for state_id in entry['state_ids']:
            # Phase 1 IDs predate this folder, so only enforce Phase 2 IDs where
            # the entry says it has a Phase 2 relationship.
            if entry['classification'] == 'phase2':
                assert state_id in phase2_ids, f"Unknown Phase 2 state: {entry['source_path']} -> {state_id}"
    gaps = data.get('known_ui_gaps', [])
    validate_gap_policy(gaps)
    exercise_gap_policy()
    if args.app_root:
        observed = sorted(p.relative_to(args.app_root).as_posix() for p in (args.app_root / 'src/renderer').rglob('*.ts'))
        assert observed == sorted(paths), 'Renderer file set drifted from embedded baseline'
        for entry in entries:
            target = args.app_root / entry['source_path']
            assert target.is_file(), f"Missing baseline source: {entry['source_path']}"
            assert sha(target) == entry['sha256'], f"Baseline source drift: {entry['source_path']}"
    print(json.dumps({'state': 'PASS', 'entries': len(entries), 'known_ui_gaps': len(gaps),
                      'gap_policy_probe': 'accepts_empty_rejects_nonempty',
                      'checked_app_root': str(args.app_root) if args.app_root else None}))

if __name__ == '__main__':
    main()
