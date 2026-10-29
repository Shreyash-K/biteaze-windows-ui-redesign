# Phase 2 acceptance

## Visual contract

Use Phase 1 tokens and `reference/design/design.css` together with this folder's `phase2.css`, source demo, screenshots, and Phase 2 PDF. The prototype's simulated title bar and reference navigator are review aids, not production chrome. Retain the application’s approved assets and brand mark.

Match at 1920×1080, 1366×768, and 1280×720 effective client pixels. Check rail/header consistency, page and menu widths, gutters, type metrics, semantic colors, labelled status, table overflow, independently scrolling panes, drawer/dialog placement, modal header/footer visibility, focused/disabled styling, long text, and sticky decision surfaces. Test Windows 100%, 125%, and 150% scaling separately; browser-like viewport validation does not prove physical DPI behavior.

## Per-row acceptance

Every `screen-coverage.csv` row must name an owner, app source path, implementation/evidence links, and all four status columns below. Record capability disposition beside the matching requirement in the application implementation ledger. The supplied CSV is an untouched handoff baseline; copy it into the private application before updating it:

| Column | Meaning |
|---|---|
| `implemented_status` → `IMPLEMENTED` | The route/view is wired to the real app state and commands. |
| `visual_status` → `VISUAL_PASS` | Actual screenshots at all three sizes were compared with the reference. |
| `behavior_status` → `BEHAVIOR_PASS` | Meaningful tests or deterministic manual evidence cover its input/action/outcome contract. |
| `windows_device_status` → `WINDOWS_DEVICE_PASS` | A real Windows/device/provider/physical check was performed where applicable. |

`WINDOWS_DEVICE_PASS` remains `NOT_MEASURED` for ordinary web-style screenshot evidence, mocked bridge tests, printers not physically checked, payment terminals/providers not exercised, scanners not connected, or update/install paths not performed.

## Meaningful behavior evidence

Verify the actual source-backed contract rather than demo navigation:

- Financial, document, GST, credit, stock, import, day-close, and account changes preserve authority, expected revision/value, correction/audit semantics, and failure states.
- Document/correction/reprint states retain issued identity; legal totals do not become editable demo values; private export/share never claims recipient delivery.
- Food service retains order type, table rules, selected order/revision, modifiers, hold/resume, transfer/merge/split, routed KOT, and stale/unavailable recovery.
- QR flow separates backend readiness, source publication, mirror state, table QR, intake, and accepted orders. Public mirror failure must remain visible.
- Billing recovery and payment completion use one durable operation identity. Unknown/pending/conflict/stale outcomes do not duplicate sales or become success on a timeout. Credit warnings/reservation/overrides stay scoped to actual policy.
- Printer, label, scanner, command, backup/restore, sync, staff, jobs, and Windows update actions show actual readiness/permission/operation state. Physical output and installed-update completion are not inferred.
- Account readiness, device claim, handover admission, invoice-counter verification, and restore-entry outcomes retain their distinct issued presentation states. A counter outcome that is unknown or latched cannot be represented as a retry that creates a new invoice number.
- Keyboard-only navigation, accessible names, focus return/loop, Escape priority, validation, disabled actions, long localized content, and navigation away/back preserve form/order state as the app requires.

## Final evidence gate

Use current application instructions and gate tooling. Preserve their full denominator and time budgets. The final gate runs only on the exact clean source to be reviewed; record its command, result, duration, source revision, and the mechanism that constrained duration. Any test over budget is a scheduling/performance defect to repair before equivalent repeats, without reducing coverage.

The reference package's browser/PDF checks establish only package/demo correctness. They do not qualify Electron, Windows, native APIs, printers, scanners, payments, sync, or production services.
