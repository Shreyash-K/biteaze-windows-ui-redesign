# Acceptance and validation

## Visual authority

1. `reference/design/design.css`, `reference/design/assets/brand-tokens.css`, the rendered offline prototype and PNGs define geometry, typography, colors and components.
2. `reference/Biteaze-Windows-UI-Reference.pdf` is the indexed visual review book. `docs/SCREEN-COVERAGE.csv` links its pages to source and screenshots.
3. `reference/design/IMPLEMENTATION-GUIDE.md` defines responsive behavior and interactions. Original tablet pages establish context; the redesigned desktop reference is the target.
4. Current production controllers/domain contracts govern money, permissions, data and commands. If a picture disagrees, preserve authority and document the smallest visual adaptation.

Use actual brand assets already approved in the app, replacing the concept letter mark. Preserve exact brand spelling. No new visual direction, gradients, decorative backgrounds or generic dashboard substitutes.

This task targets the light, slate-and-orange desktop design shown in the PDF. The shared brand token file also contains generic dark-theme presets and comments; those do not override the rendered reference or authorize a theme change. Match the values actually applied by `reference/design/design.css`.

## Geometry and density

| Client viewport / effective pixels | Rail | Bill | Catalog |
|---|---:|---:|---|
| 1920×1080 | 96 | 492 | 178 category column, 4 product columns |
| 1366×768 | 80 | 404 | Category row, 3 product columns |
| 1280×720 | 72 | 380 | Category row, 3 product columns |

Use actual available Electron client bounds; the prototype includes a simulated title bar for context. Replace it with real Windows chrome without doubling that region. Never scale the whole 1920 canvas as an image. Handle Windows 100%, 125% and 150% settings separately from CSS viewport tests; 1920 physical pixels at 150% provides about 1280 effective pixels before chrome/taskbar. 1366 physical pixels at 150% is below this kit's minimum and requires an explicit narrow-window/minimum-size decision, not a claim of support.

Keep total, tender state and checkout outside the line-item scroller. Product grid, category list, bill items, page content and dialog body scroll independently. Modal header/footer remain available at short heights. Use kit widths: dialogs 540/640/860, payment 1040 or 980 compact, drawer 580 or 540 compact. Avoid absolute positioning for general page layout.

Retain Inter body, Plus Jakarta Sans headings, tabular prices, 4px spacing rhythm, slate canvas/white panels, brand orange and named semantic statuses. Primary action uses dark legible text on bright orange. Maintain the app's existing semantic-token and computed-contrast rules; focus can match the reference while retaining sufficient contrast.

## Required screen evidence

All 72 CSV IDs must have implementation owner, real source paths, capability disposition and screenshots. Capture each at all three client sizes: 216 observations minimum. For long pages capture scroll continuations. Compare actual app with the corresponding reference state; small font rendering differences across OS are acceptable, structural differences need explanation. A global similarity score alone cannot approve the UI.

For each comparison inspect rail/header, pane proportions, gutters, font metrics, text wrapping, amounts, selected/disabled styles, scroll boundaries, overflow, overlay placement, sticky actions and focus visibility. Use deterministic test fixtures and redact account/customer identifiers. Never use real payments or data mutations to reach a visual state.

Maintain separate columns for IMPLEMENTED, VISUAL_PASS, BEHAVIOR_PASS and WINDOWS_DEVICE_PASS. A screenshot is not payment/permission proof. A successful mocked bridge test is not physical-printer proof. Unavailable states can be visually verified while the capability remains blocked.

## Meaningful behavior paths

- Create a bill; search/scan; configure required and optional modifiers; edit quantity/note; remove; verify authoritative totals remain unchanged by UI code.
- Attach/change customer; preserve staff/service context; apply/remove existing discount/coupon/loyalty; denied/stale responses remain visible.
- Hold/resume/discard and restore quotation/challan; navigate away/back; late async responses cannot resurrect obsolete state.
- Existing cash, UPI, card and credit preview/confirmation paths; insufficient tender, pending/unavailable/denied/stale outcomes; double-click/retry behavior. Never convert pending into success by timeout.
- Payment completion and receipt print failure are independent. Retry/reprint through existing queues without duplicate sale or accidental KOT routing.
- Running orders, table transfer/split/merge, KOT send/failure/retry, stale revisions and exact selected order. No second order store.
- Sales detail → preview → reason/confirmation for refund/void; permissions and retained audit fields.
- Day close with unresolved activity/variance; cash movement; credit settlement and supplier/expense mutations through existing commands.
- Settings edits, receipt/KOT/A4 templates, printer roles, profile/operator capabilities; preserve currently supported controls absent from a screenshot.
- Keyboard-only path, accessible names, focus loop/return, Escape priority, screen-reader status, long localized strings, empty/large data, interrupted loading, offline/unavailable and reconnect states.

## Actual application checks

Inspected baseline uses Node 22.22.1/npm 10.9.4. Inspect current versions and prerequisites before running. Do not run these in the reference repository.

Focused iteration checks include the relevant existing DOM suites:
`npm run test:p4-2-ordinary-item-configuration-dom`, `test:p4-4-parties-operators-dom`, `test:p4-production-dom-cohort`, `test:p6-3-printer-setup-dom`, `test:p6-4-barcode-label-dom`, `test:p6-12-renderer-dom`, `test:p6-6-customer-display-dom`, plus `npm run probe:contrast` where the environment supports it. Prefix each named script with `npm run`. Read package.json before invoking; scripts may change.

Final application gate: `npm run gate:canonical-full`. At the inspected revision it runs tests, contract drift, i18n engine, four-project typecheck, lint/layer boundaries and build. It requires clean exact source, correct Node, shared harness, minimum 512 MiB free space and Firebase Auth emulator prerequisites; Windows uses Git Bash for the harness. Current full floor 80s / budget 900s and unit ceiling 180s come from `ci/performance-budgets.json`; do not copy stale test counts or weaken those limits. The app's own QA/contrast/CI requirements still apply beyond this local canonical runner.

Use `.quality-gate-verify.sh`/current repository tooling for exact-source/freshness/FULL verification. Preserve existing hooks. Do not publish scoped or changed-tree evidence as full. Record each gate duration and mechanism; schedule native rebuilds and test resources centrally. Shared harness files stay symlinked, never copied or replaced with a weaker local script.

## Qualification limits

The app baseline labels itself IMPLEMENTED_UNQUALIFIED with Windows hardware unqualified. This handoff ran reference/package checks only. Windows install/update, real DPI behavior, physical printers/receipt fit, live payment hardware/providers and real synchronization remain NOT_MEASURED until separately exercised. Missing hardware is a stated qualification gap, not grounds to fabricate a green release.
