# Phase 2 implementation plan

Use this after Phase 1 has reached a stable integration point. Phase 2 is not a replacement application and does not authorize resetting, stashing, overwriting, or assuming the state of any in-progress Phase 1 work.

## 0. Reconcile before changing the app

Read the current application instructions, coordination state, tracker, branch, HEAD, dirty paths, package scripts, and gate policy. Compare the current app against source-map data from this folder and record drift. Preserve active work; use a clean worktree only when the app's own rules permit it. Copy the Phase 2 ledger into the app task documentation and give each row a real route/controller/bridge disposition before coding.

The source baseline used to make this reference is `7932bbbedabdd0cef4295919a91674f35fa815cf`. It is an inspection point, not a required reset target.

## 1. Establish shared UI contracts

One integrator owns renderer entrypoints, global styles, navigation, overlay host, test scheduling, and the living tracker. Reuse Phase 1 primitives and preserve the Electron + TypeScript DOM architecture. Do not introduce a replacement UI framework or use the reference HTML as app logic.

Build only reusable additions needed by the new states: structured page heading, section menu, two-pane workspace, validated form fields, table overflow wrapper, named semantic status, drawer/dialog host, disabled controls, and async/revision outcome presentation. Preserve keyboard focus, Escape priority, route lifecycle, localization, and named preload bridge boundaries.

## 2. Implement in bounded vertical slices

Use at most three non-overlapping workers plus the integrator. Each worker receives exact file ownership and state IDs, changes no shared entrypoint without handoff, preserves peers' work, and records paths/tests/gaps in the tracker.

| Slice | State groups | Required authority checks |
|---|---|---|
| Commerce | Purchasing, documents, reports, inventory, customers, marketing (74–136) | Main-owned financial/legal totals; cursor/range bounds; CAS/revision mutations; private export/share semantics; immutable correction/audit evidence. |
| Operations | Setup, printing, device & staff, recovery, support, services (137–188) | Admission/restore state, EULA/version, printer queue vs physical output, owner/operator access, account lifecycle, sync quarantine, category entitlement. |
| Service and checkout | Food service, QR ordering, billing recovery, checkout, desktop (189–245) | Selected-order revision, KOT routing, QR source/mirror/intake truth, canonical billing and tender/credit rules, unknown-outcome retry identity, scanner/update state. |
| Readiness | Account/device/handover/counter/restore admission outcomes (246–286) | Every issued readiness/presentation outcome, forward-only counter rules, and recovery admission rather than generic boot errors. |

For each row, keep all visible fields and actions reachable. Bind normal, loading, empty, unavailable, denied, stale/conflict, pending/unknown, and successful outcomes to real controller state. A visual shell for an absent authority may be implemented only as an explicit unavailable state; do not invent success.

## 3. Preserve critical boundaries

- Money, tax, legal documents, stock quantities, and totals are calculated/validated by the existing canonical app authority. Renderer presentation never becomes the authority.
- IPC remains named, least-privilege, and main-owned. Preserve SQLCipher/persistence, permissions, revisions, and approved device integrations.
- “Unknown” save, payment, import, print, or document outcomes retry or reconcile the same operation identity; they never silently create a second sale or mutation.
- QR publishing distinguishes committed source revision, public mirror pending/failed/live, and intake unavailable. A failure does not mean an empty order list.
- “Queued” or “transport accepted” print status does not claim physical output. Hardware/device qualification is separate.
- Keep scope limits already present in source: existing tenders only, revision/expected-value guards, category entitlements, manual-message composition rather than confirmed delivery, and owner-only destructive actions.

## 4. Evidence while building

For every ledger row, capture actual app evidence at 1920×1080, 1366×768, and 1280×720 effective client pixels. Add long-scroll continuations. Compare structure with the reference rather than accepting a global screenshot score. Record `IMPLEMENTED`, `VISUAL_PASS`, `BEHAVIOR_PASS`, and `WINDOWS_DEVICE_PASS` independently.

Run focused tests during each slice and retain passing evidence. On the exact clean final app source, run the application's current full canonical gate and its required visual/accessibility checks. Record each duration and the scheduling mechanism. A scoped green test cannot be published as final full evidence.

## 5. Integration gate

The integrator reviews all 213 product states and the 174 inventory entries against the ledger, resolves shared navigation/overlay conflicts, and asks an independent reviewer to inspect the exact final diff and evidence. The integrator owns readiness states 246–286 because they gate shared admission/recovery composition. Update the living tracker with HEAD, owners, completed rows, test results, blocked rows, and the next safe action. Do not push, merge, release, mutate merchant data, print, or charge a payment unless separately authorized.
