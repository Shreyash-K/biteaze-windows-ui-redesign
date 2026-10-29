# Phase 2 — remaining Windows workflows

This folder is the second part of the Biteaze Windows design reference. It covers the operational screens omitted from the 72-screen Phase 1 billing kit: 214 separately addressable reference states numbered **73–286**. It contains 213 product states and one workflow directory. The prototype uses synthetic records only and never contacts an app, payment provider, printer, scanner, or service.

Open `index.html` in a local browser. Use the bottom reference navigator to select screens, follow its local links, and inspect dialogs, drawers, gates, long-content continuations, and responsive layouts. For a local server:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8765/phase-2-remaining-screens/`.

## What is authoritative

| Need | File |
|---|---|
| Visual demo and editable source | `index.html`, `phase2.css`, `common.js`, `commerce.js`, `operations.js`, `service.js`, `readiness.js`, `app.js` |
| Every state, source seam and coverage ID | `screen-manifest.json` |
| Full visual review book | `Biteaze-Windows-Phase-2-Reference.pdf` |
| Screenshot route/page map | `pdf-page-map.json` |
| Screen and inventory ledger | `screen-coverage.csv`, `requirements-coverage.json` |
| Current inspected source revision and hashes | `source-map.json` |
| Every renderer TypeScript source surface and explicit exclusions | `source-surface-inventory.json`, `SOURCE-SURFACE-INVENTORY.md` |
| Measured package evidence and limits | `EVIDENCE.md` |
| Build prompt for Antigravity | `GEMINI-PHASE-2-PROMPT.md` |

The PDF, screenshot files, coverage ledger and source-map are generated deliverables included alongside this README. The source prototype is intentionally editable. Exact published screenshot and PDF counts are recorded in `EVIDENCE.md` after the final capture.

All new customer, supplier and operator fixtures are fictional examples, not imported records. Phone values beginning with `00000`, `07TESTX0000X0Z0`, `sample@invalid`, and `example.invalid` are deliberately unusable placeholders. They illustrate field placement and must be replaced with validated application values in the actual app. The receipt QR graphic is decorative, not a working destination.

## Scope and boundary

The visual language extends Phase 1: light slate canvas, white panels, orange primary actions, Inter body text, Plus Jakarta Sans headings, named status labels, dense but readable desktop layouts, and independent scrolling panels. Phase 2 is designed at 1920×1080, 1366×768, and 1280×720 effective client pixels.

It is a code-informed reference for the private Electron/TypeScript DOM application at `Shreyash-K/android-billing-desktop`, inspected at `7932bbbedabdd0cef4295919a91674f35fa815cf`. It does not implement that app. The actual app remains the authority for state, main-process IPC, money, tax, printer routing, permissions, revisions, payment outcomes, persistence, and device signals. Do not copy demo totals, fake results, or local navigation behavior into production.

The repository is public. The app source is private. Do not add private application code, credentials, customer records, logs, local paths containing secrets, or the live merchant database here.

## Coverage

The 174 source-inventory entries are represented by the 213 product states (three existing entries deliberately share related cross-module states; the five readiness requirements each have finite outcome variants):

- Purchasing, documents, reports, inventory, customers and marketing.
- Auth, onboarding, printing, staff/device controls, backup/restore, support, legal operations, appointments and jobs.
- Food-service order lifecycle, QR publication/intake, billing recovery, checkout authority, command palette, scanner, and Windows update states.
- Account readiness, current-device claim, handover admission, invoice-counter verification, and local restore-entry outcomes.

Blocked, pending, stale, failure, conflict, and recovery screens are intentional. A disabled control in a reference state means its prerequisite is absent; the actual app must bind it to its own authority rather than enabling it for visual parity.

Some list rows share one visual detail template. The canonical sample opens that detail; other samples explicitly retain their selected identity and report that their dedicated detail is not represented. These feedback actions are reference boundaries, not instructions to disable real application capabilities. Dialogs whose parent lives in Phase 1 show a labelled linked-workspace backdrop and return to the original reference page. The app must use its actual underlying workspace and restore the real opener.
