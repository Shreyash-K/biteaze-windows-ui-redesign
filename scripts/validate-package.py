#!/usr/bin/env python3
"""Validate the complete reference package. Does not execute application code."""
import csv
import hashlib
import importlib.util
import json
import re
import struct
import sys
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'reference/design'
STARTED = time.perf_counter()
CHECKS = 0
FAILURES = []


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        FAILURES.append(message)


def json_file(path):
    return json.loads(path.read_text(encoding='utf-8'))


def png_size(path):
    header = path.read_bytes()[:24]
    if header[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'Invalid PNG: {path}')
    return struct.unpack('>II', header[16:24])


def local_target(source, href):
    parts = urlsplit(unquote(href))
    if parts.scheme or parts.netloc or not parts.path or parts.path.startswith('/'):
        return None
    return (source.parent / unquote(parts.path)).resolve()


def run():
    manifest = json_file(ROOT / 'asset-manifest.json')
    check(len(manifest['files']) == manifest['file_count'], 'Manifest file count')
    spec = importlib.util.spec_from_file_location('manifest_generator', ROOT / 'scripts/generate-manifest.py')
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    listed = [f['path'] for f in manifest['files']]
    actual = [p.relative_to(ROOT).as_posix() for p in generator.package_files()]
    check(len(set(listed)) == len(listed), 'Duplicate manifest paths')
    check(sorted(listed) == sorted(actual), 'Manifest differs from actual distributed files')
    for entry in manifest['files']:
        path = (ROOT / entry['path']).resolve()
        check(path.is_relative_to(ROOT), f'Unsafe path: {entry["path"]}')
        check(path.is_file(), f'Missing file: {entry["path"]}')
        if not path.is_file() or not path.is_relative_to(ROOT):
            continue
        data = path.read_bytes()
        check(len(data) == entry['bytes'], f'File size: {entry["path"]}')
        check(hashlib.sha256(data).hexdigest() == entry['sha256'], f'File hash: {entry["path"]}')
        check(len(data) < 100_000_000, f'GitHub oversized file: {entry["path"]}')

    screens = json_file(DESIGN / 'screen-manifest.json')
    check(len(screens) == 72, 'Expected all 72 reference states')
    check(len({s['id'] for s in screens}) == 72, 'Duplicate state IDs')
    check([s['number'] for s in screens] == list(range(1, 73)), 'State numbering')
    with (ROOT / 'docs/SCREEN-COVERAGE.csv').open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    check(len(rows) == 72, 'Expected all 72 coverage rows')
    check([r['screen_id'] for r in rows] == [s['id'] for s in screens], 'Coverage/state identity mismatch')
    page_map = json_file(ROOT / 'reference/pdf-page-map.json')
    page_by_key = {p['key']: p['page'] for p in page_map if p['key']}
    for screen, row in zip(screens, rows):
        check(int(row['number']) == screen['number'], f'Coverage number: {screen["id"]}')
        check(row['title'] == screen['title'], f'Coverage title: {screen["id"]}')
        check(int(row['pdf_page']) == page_by_key[screen['id']], f'PDF page: {screen["id"]}')
        check(row['status'] == 'NOT_STARTED', f'Handoff must not claim implementation: {screen["id"]}')
        check(png_size(ROOT / row['png']) == (1920, 1080), f'PNG geometry: {screen["id"]}')
        check(row['prototype_url'].endswith('?screen=' + screen['id']), f'Prototype target: {screen["id"]}')
    continuation_rows = json_file(DESIGN / 'continuations.json')
    check(len(continuation_rows) == 14, 'Expected 14 continuations')
    for entry in continuation_rows:
        check(entry['screen'] in page_by_key, f'Continuation state: {entry["screen"]}')
        check(png_size(DESIGN / 'screens' / entry['file']) == (1920, 1080), f'Continuation PNG: {entry["file"]}')
    check(len(list((DESIGN / 'screens').glob('*.png'))) == 86, 'Expected 86 screen PNGs')
    responsive = list((DESIGN / 'responsive').glob('*.png'))
    check(len(responsive) == 12, 'Expected 12 compact PNGs')
    for path in responsive:
        size = tuple(map(int, path.stem.rsplit('-', 1)[1].split('x')))
        check(png_size(path) == size, f'Compact PNG geometry: {path.name}')

    for path, expected in [(ROOT / 'reference/Biteaze-Windows-UI-Reference.pdf', 104),
                           (ROOT / 'reference/Android-tablet-original.pdf', 33)]:
        reader = PdfReader(path)
        check(not reader.is_encrypted, f'Encrypted PDF: {path.name}')
        check(len(reader.pages) == expected, f'Page count: {path.name}')
    reader = PdfReader(ROOT / 'reference/Biteaze-Windows-UI-Reference.pdf')
    for page in reader.pages:
        check(tuple(float(x) for x in page.mediabox[2:]) == (1280, 820), 'Design PDF page geometry')
    check(len(page_map) == 104, 'PDF index length')

    # All static local HTML/CSS dependencies; dynamic state routes are covered in Chromium.
    for source in list(DESIGN.glob('*.html')) + list(DESIGN.rglob('*.css')):
        text = source.read_text(encoding='utf-8')
        refs = re.findall(r'(?:src|href)=[\"\']([^\"\']+)[\"\']', text)
        refs += re.findall(r'url\([\"\']?([^\)\"\']+)', text)
        for href in refs:
            target = local_target(source, href)
            if target:
                check(target.is_relative_to(ROOT) and target.exists(), f'Broken local asset/link: {source.name} → {href}')
    for source in [ROOT / 'README.md', ROOT / 'START-HERE.md', *list((ROOT / 'docs').glob('*.md'))]:
        for href in re.findall(r'\]\(([^)]+)\)', source.read_text(encoding='utf-8')):
            target = local_target(source, href)
            if target:
                check(target.is_relative_to(ROOT) and target.exists(), f'Broken handoff link: {source.name} → {href}')
    source = json_file(ROOT / 'app-source.json')
    check(source['repository'] == 'https://github.com/Shreyash-K/android-billing-desktop', 'Application identity')
    check(source['local_changes_included'] is False, 'Dirty application files must remain excluded')
    check(source['implementation_status'] == 'NOT_STARTED', 'Application status must remain honest')


try:
    run()
except Exception as exc:
    FAILURES.append(f'{type(exc).__name__}: {exc}')
report = {'scope': 'Entire distributed reference package; not application qualification',
          'checks': CHECKS, 'failures': FAILURES, 'seconds': round(time.perf_counter() - STARTED, 3),
          'state': 'FAIL' if FAILURES else 'PASS'}
(ROOT / 'artifacts').mkdir(exist_ok=True)
(ROOT / 'artifacts/package-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report))
sys.exit(1 if FAILURES else 0)
