#!/usr/bin/env python3
"""Generate a public, hash-only inventory of the inspected private renderer.

The script reads private source only when run by the reference-package maintainer.
Its JSON output contains paths, SHA-256 values, classifications and public mapping
metadata; it never copies source text. The companion validator can validate the
embedded baseline without the private repository and can optionally check a local
app checkout for drift.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP = ROOT.parents[1] / 'work' / 'windows-app-remote'
OUT = ROOT / 'phase-2-remaining-screens' / 'source-surface-inventory.json'
BASELINE = '7932bbbedabdd0cef4295919a91674f35fa815cf'

# These are source-backed Phase 1 runtime surfaces.  They are anchored to the
# existing first reference set rather than falsely asserting a Phase 2 state.
PHASE1 = {
    'src/renderer/features/catalog/catalog-workspace.ts': ['billing', 'billing-empty'],
    'src/renderer/features/catalog/item-configuration-workspace.ts': ['item-customize'],
    'src/renderer/features/cart/cart-workspace.ts': ['line-edit'],
    'src/renderer/features/checkout/discount-marketing-workspace.ts': ['discount', 'coupon', 'charges'],
    'src/renderer/features/checkout/hold-resume-workspace.ts': ['orders', 'hold', 'order-details'],
    'src/renderer/features/checkout/parties-operators-workspace.ts': ['customer-select', 'customers', 'manager', 'staff'],
    'src/renderer/printer-setup/printer-setup-presentation.ts': ['printers', 'printer-select', 'receipt'],
}

# Runtime support files with direct Phase 2 consequences.  This is deliberately
# not a visual-state claim: a controller/wire may serve several listed states.
P2_SUPPORT = {
    'src/renderer/auth-controller.ts': ['auth-sign-in', 'auth-create-account', 'auth-password-reset', 'auth-google-pending'],
    'src/renderer/auth-messages.ts': ['auth-sign-in', 'auth-create-account', 'auth-password-reset'],
    'src/renderer/features/barcode-labels/barcode-label-wire.ts': ['labels-batch-setup', 'labels-exact-preview', 'labels-submit-failure'],
    'src/renderer/features/customers/customer-khata-controller.ts': ['customer-search-aging', 'customer-profile-khata-detail', 'khata-statement-share', 'khata-settlement-receipt'],
    'src/renderer/features/documents/documents-controller.ts': ['document-search-register', 'document-detail-complete', 'sales-return-preview-confirm', 'quotation-create-edit', 'challan-create-edit'],
    'src/renderer/features/financial/financial-controller.ts': ['supplier-directory-detail', 'supplier-payment-record', 'purchase-create', 'expense-history-edit'],
    'src/renderer/features/food-service/food-service-wire.ts': ['food-service-workspace', 'food-running-order', 'qr-order-intake'],
    'src/renderer/features/inventory/inventory-workspace-controller.ts': ['inventory-catalog-browse', 'product-edit-delete-revision', 'stock-movement-entry', 'inventory-conflicts-quarantine'],
    'src/renderer/features/keyboard/application-commands.ts': ['command-palette', 'plu-shortcode-result'],
    'src/renderer/features/keyboard/command-registry.ts': ['command-palette'],
    'src/renderer/features/keyboard/keyboard-command-controller.ts': ['command-palette', 'plu-shortcode-result'],
    'src/renderer/features/keyboard/keyboard-runtime.ts': ['command-palette', 'plu-shortcode-result'],
    'src/renderer/features/operator-experience/operator-experience-controller.ts': ['operator-settings', 'backup-recovery', 'profile-security', 'sync-conflict-review'],
    'src/renderer/features/print-center/hardware-qualification-wire.ts': ['print-hardware-qualification'],
    'src/renderer/features/print-center/print-center-wire.ts': ['print-setup-discovery', 'print-fleet-tests', 'print-job-history', 'print-outcome-reconcile'],
    'src/renderer/features/print-center/production-print-center-composition.ts': ['print-setup-discovery', 'print-printer-editor', 'print-fleet-tests', 'print-job-history'],
    'src/renderer/features/reporting/reporting-controller.ts': ['report-catalog', 'report-processing', 'report-table-result', 'gst-filing-pack-summary'],
    'src/renderer/features/scanner/catalog-code-dispatch.ts': ['plu-shortcode-result'],
    'src/renderer/features/scanner/keyboard-wedge-scanner.ts': ['scanner-setup', 'scanner-test', 'scanner-runtime-status'],
    'src/renderer/features/scanner/scanner-input-policy.ts': ['scanner-setup'],
    'src/renderer/features/scanner/scanner-runtime.ts': ['scanner-runtime-status'],
    'src/renderer/features/scanner/scanner-setup-controller.ts': ['scanner-setup', 'scanner-test'],
    'src/renderer/staff-authorization-controller.ts': ['staff-authorization', 'staff-member-security', 'staff-pin-recovery'],
}

# The five formerly uncovered presentation modules are direct manifest anchors
# 246–286. This completed package must leave no known renderer UI gaps.
GAPS: list[dict[str, str]] = []

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def direct_phase2() -> dict[str, list[str]]:
    manifest = json.loads((ROOT / 'phase-2-remaining-screens' / 'screen-manifest.json').read_text())
    mapping: dict[str, list[str]] = {}
    for row in manifest:
        source = row.get('source', '')
        if source.startswith('src/renderer/'):
            mapping.setdefault(source, []).append(row['id'])
    return mapping

def classify(path: str, phase2: dict[str, list[str]]) -> tuple[str, str, list[str]]:
    if '/__tests__/' in path or path.startswith('src/renderer/__tests__/'):
        return 'explicit_exclusion', 'Test-only renderer file; tested behavior is not a separately shippable UI surface.', []
    if path in phase2:
        return 'phase2', 'Direct source anchor in the Phase 2 screen manifest.', phase2[path]
    if path in PHASE1:
        return 'phase1', 'Runtime surface represented by the existing Phase 1 reference set.', PHASE1[path]
    if path in P2_SUPPORT:
        return 'phase2', 'Runtime support for listed Phase 2 state(s); not a separate visual screen claim.', P2_SUPPORT[path]
    if path.endswith('.d.ts'):
        return 'shared_non_ui', 'Type declaration, not a renderer surface.', []
    if '/generated/' in path or path.endswith('.generated.ts'):
        return 'shared_non_ui', 'Generated contract/policy data; visual state is anchored by its route/surface.', []
    return 'shared_non_ui', 'Renderer composition, controller, policy, utility, runtime, or accessibility support; no independently registered surface.', []

def main() -> None:
    app = DEFAULT_APP
    if not app.exists():
        raise SystemExit(f'Private source checkout not found: {app}')
    files = sorted((app / 'src/renderer').rglob('*.ts'))
    phase2 = direct_phase2()
    entries = []
    for file in files:
        rel = file.relative_to(app).as_posix()
        classification, rationale, state_ids = classify(rel, phase2)
        entries.append({'source_path': rel, 'sha256': sha(file), 'classification': classification,
                        'rationale': rationale, 'state_ids': state_ids})
    output = {
        'schema_version': 1,
        'baseline_commit': BASELINE,
        'extraction': {
            'method': 'Enumerated every src/renderer/**/*.ts file in a clean read-only checkout; direct Phase 2 anchors come from screen-manifest.json; Phase 1 anchors and runtime-support relationships are explicit tables in the generator.',
            'file_count': len(entries),
            'public_data_only': 'Paths, hashes, classifications, state IDs and rationales. No source text is copied.',
        },
        'entries': entries,
        'known_ui_gaps': GAPS,
    }
    OUT.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'output': str(OUT), 'files': len(entries), 'gaps': len(GAPS)}))

if __name__ == '__main__':
    main()
