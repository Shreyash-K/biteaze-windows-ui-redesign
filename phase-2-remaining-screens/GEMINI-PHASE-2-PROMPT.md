Implement the complete Phase 2 Biteaze Windows UI redesign in the existing app only after the active Phase 1 build has reached a stable integration point. The app is `Shreyash-K/android-billing-desktop` (private). The visual/reference repository is `Shreyash-K/biteaze-windows-ui-redesign` (public), with Phase 2 at `phase-2-remaining-screens/`. Do not replace the application with this prototype, create a new framework, or treat its sample data/actions as product logic.

Work through this in one sustained session if the environment permits, with a living tracker that survives compaction. Do not pretend a single session guarantees external/hardware qualification. Preserve all existing local work: inspect status, current branch/HEAD, active owner files, instructions, and build locks before changing anything; never reset/stash/overwrite another worker's changes. Phase 1 may have changed the app since the source revision used for this reference (`7932bbbedabdd0cef4295919a91674f35fa815cf`), so inspect and reconcile drift instead of reverting toward that revision.

## Read before implementation

1. In the reference repo, read `START-HERE.md`, `GEMINI.md`, `docs/CODEBASE-MAP.md`, `docs/PRODUCTION-BOUNDARIES.md`, and the Phase 2 files `README.md`, `IMPLEMENTATION-PLAN.md`, `ACCEPTANCE.md`, `SOURCE-SURFACE-INVENTORY.md`, `source-surface-inventory.json`, `screen-manifest.json`, `screen-coverage.csv`, `requirements-coverage.json`, `source-map.json`, `EVIDENCE.md`, and `Biteaze-Windows-Phase-2-Reference.pdf`.
2. Run or open `phase-2-remaining-screens/index.html` locally and inspect all 214 states numbered 73–286, the screenshots, continuations, responsive evidence, CSS, bundled fonts, and Phase 1 reference. The actual target is the light slate/white/orange desktop system, not the dark reference navigator or simulated title bar.
3. In the app, read its current instructions, coordination/tracker state, package scripts, architecture, bridge, current source, and full-gate policy. The app is Electron with TypeScript and DOM renderers; retain that architecture, its localization, named preload bridge, main-process authority, canonical billing engine, persistence/security, and existing navigation semantics.

## Coordinate a real team, when supported

You are the single integrator for shared renderer entrypoints, global CSS, app navigation, dialog host, tracker, and test/build scheduling. Use at most three workers at once; do not claim subagents ran if your environment cannot run them. Reuse workers sequentially as capacity frees.

Assign exact, non-overlapping ownership:

1. **Commerce worker:** Phase 2 states 74–136: purchasing, documents, reporting/GST, inventory/imports, customer credit, marketing. It owns only the corresponding route renderers/styles/tests.
2. **Operations worker:** states 137–188: auth/onboarding, print/labels, device/staff, backup/restore/sync, support/legal, categories, appointments/jobs. It owns only corresponding route renderers/styles/tests.
3. **Service worker:** states 189–245: food service, QR ordering, billing recovery, checkout authority, command palette/scanner/update. It owns only corresponding route renderers/styles/tests. The integrator owns shared readiness/admission states 246–286.

Workers are not alone in the codebase. Each must preserve peers' edits, return changed paths, focused tests, screenshots, unresolved capability gaps, and row dispositions. Keep common shell changes with the integrator. After slices land, use an independent reviewer for the exact final app diff, evidence, semantic boundaries, and layout comparison.

## Build order

1. Create an app-local tracker from the existing template. For every Phase 2 ledger row record source path/controller/bridge capability, owner, state IDs, supported/missing authority, screenshot locations, and `IMPLEMENTED`, `VISUAL_PASS`, `BEHAVIOR_PASS`, `WINDOWS_DEVICE_PASS`. Keep both the 213 product-state count and 174 source-inventory-entry denominator explicit; three related entries intentionally share cross-module reference states and the five readiness requirements each represent finite outcome variants.
2. Adapt/reuse Phase 1 primitives first: light slate canvas, white panels, orange primary actions, Inter body/Plus Jakarta Sans headings, labelled semantic statuses, section menus, data-table wrappers, responsive workspace split, dialog/drawer host and disabled controls. Match at 1920×1080, 1366×768, and 1280×720 effective client pixels. Use real Windows chrome, not the prototype chrome.
3. Implement every supported state, subscreen, popup, empty/loading/error/denied/stale/conflict/pending/unknown/disabled state in the ledger. Do not stop at a dashboard or generic screen. Keep all existing app capabilities outside the reference reachable and apply the design system to them where needed.
4. Bind visible fields/actions to real production state. Detail templates and report results must preserve the selected record/report identity; reference-only feedback for non-canonical samples is not a product limitation. Cross-Phase-1 dialog placeholders must use the real parent workspace in the app, with opener focus restored. A missing backend/bridge/permission must render an honest unavailable state and a documented gap. It is never permission to fabricate a success, approval, stock quantity, printer result, provider callback, or public publication.
5. Reconcile all changes, run meaningful focused checks during implementation, then run the app's current full canonical gate on the clean exact final source before any push/merge. Preserve full coverage and duration budgets. If a repeated gate is over its budget, stop equivalent repeats, repair scheduling without reducing coverage, and prove the guard before resuming.

## Non-negotiable behavior boundaries

- Main/domain authority owns money, tax, legal documents, tender/payment state, stock, printer routing, permissions, revisions/CAS, persistence, and provider/device results. The renderer is not a second source of truth.
- Unknown save/payment/import/document/print outcomes retry or reconcile the same operation identity. Never create a duplicate sale, correction, import page, or print claim.
- Preserve immutable issued/legal values, correction chains, expected revisions/values, customer/quotation/challan identity checks, and private export/manual-composer wording.
- Retain the actual supported tender and order-type scope. Do not enable split tender, delivery, manager approval, or new service capabilities only because the reference has a convenient visual pattern.
- QR source commit, public mirror pending/failed/live, table QR, and order intake are separate truths. A failed/intake-unavailable result is not an empty list.
- Print queued/transport accepted does not mean physical output. Manual messaging/composer opened does not mean delivered. Native scanner/update/printer/payment qualification is separate from mocked or browser evidence.
- Preserve selected food order/table and revisions through hold/resume, transfer/merge/split/KOT/recovery. Show exact stale/unavailable/blocked reasons.

## Verification and closeout

For every row, capture deterministic synthetic-fixture app screenshots at all three sizes, including scroll continuations, and visually compare rail/header proportions, grids, text wrapping, amounts, status/disabled styles, overflow, modal placement, sticky actions, and focus. Add behavior tests around changed controller/IPC contracts, validation, stale async responses, focus/Escape, recovery/retry, and retained form state. Never use real merchant data, money, payments, messages, printing, or production services to obtain proof.

Finish with the app branch/HEAD, commits, changed files, full row ledger, before/after screenshots, focused/full gate results with durations, reviewer findings, exact blockers, and qualification matrix. Do not push, merge, deploy, release, charge a payment, send a message, or mutate live merchant data unless separately authorized.
