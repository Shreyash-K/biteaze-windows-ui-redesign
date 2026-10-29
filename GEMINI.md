# Biteaze Windows redesign context

Read `START-HERE.md`, `docs/CODEBASE-MAP.md`, `docs/PRODUCTION-BOUNDARIES.md`, `docs/IMPLEMENTATION-PLAN.md`, and `docs/ACCEPTANCE.md` before implementation. Read the current app's own instructions and tracker as well. This is a public reference repository; implement in `Shreyash-K/android-billing-desktop`.

Match `reference/design/index.html`, `reference/design/design.css`, the 72 PNGs, compact examples and PDF. Do not invent another visual direction. Preserve the current Electron + TypeScript DOM stack, controllers, localization, named preload bridge, shared calculation engine, security boundaries and existing capabilities. Prototype JavaScript is illustrative, not production domain logic. Never copy fake PIN approval, sample money calculations, QR placeholders or success toasts into operational behavior.

Target client area: 1920×1080, 1366×768, 1280×720 effective pixels. Keep totals/checkout pinned and scroll lists/dialog bodies independently. Use real window chrome. The dark demo explorer is not application UI.

Every screen in `docs/SCREEN-COVERAGE.csv` must be accounted for. Current code takes precedence for financial/security authority; the reference takes precedence for visuals. Reconcile conflict explicitly. No silent removal of existing workflows. Missing backend support is a documented gap, not permission to fabricate a service.

One coordinator owns shared renderer entrypoints, global CSS, navigation, integration, test scheduling and tracker. Give workers non-overlapping file ownership and exact screen IDs; they are not alone in the codebase and must preserve peer changes. Use actual subagents if available. No pretend delegation.

Update the living tracker after each phase with base/HEAD, owners, completed changes, evidence, gaps and next step. Read it after context loss. Run focused checks while iterating and the application's full canonical gate before any application push/merge. No production deploy, real payment, real message, destructive data change or permission bypass is authorized by this design task.

For the remaining workflows after the active Phase 1 build is stable, use `phase-2-remaining-screens/GEMINI-PHASE-2-PROMPT.md`. Phase 2 has 214 references numbered 73–286, 174 audited inventory requirements, and its own coverage ledger, PDF, source map and evidence. Reuse implemented components and preserve app drift/local work.
