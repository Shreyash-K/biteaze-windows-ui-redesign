# Phase 2 reference evidence

Measured on 29 October 2026. This is evidence for the **design reference package**, not for the actual Windows app.

| Evidence | Result |
|---|---|
| Addressable reference states | 214: 213 additional product states plus one directory; numbered 73–286 |
| Requirement coverage | 174 requirements, all mapped; 35 directly referenced source paths identified by SHA-256 |
| Complete renderer inventory | All 154 renderer TypeScript files classified; zero known UI gaps at the inspected baseline; includes 41 finite outcomes from five readiness/admission modules |
| Source baseline | `Shreyash-K/android-billing-desktop` at `7932bbbedabdd0cef4295919a91674f35fa815cf` |
| Browser layouts | PASS: all 214 states at 1920×1080, 1366×768 and 1280×720; 642 observations |
| Demo interaction checks | PASS: 112 navigation, direct modal focus, opener return, Escape, browser-back, search and selected-record identity checks |
| Enabled action outcomes | PASS: 462 workspace/dialog actions navigate, show explicit demo feedback, or focus validation |
| Capture duration | 28.469 seconds; three concurrent viewport pages in one Chromium process, then interaction checks |
| Captured assets | 236 full-HD PNGs: 214 primary plus 22 long-content continuations; 56 compact PNGs; 292 PNGs total |
| Review book | 300 pages, 1280×900 pt; all primary states, continuations and compact examples |
| Phase 2 integrity/coverage checks | PASS: 4,667 checks, 0 failures, 0.278 seconds; local file/hash/coverage/PDF parsing |
| App implementation | NOT_STARTED by this package |
| Native Windows / physical DPI / hardware / provider qualification | NOT_MEASURED |

`capture-evidence.json` contains the check names and SHA-256 identities of the prototype inputs and published image/PDF outputs. `scripts/validate-phase2-package.py` rejects modified inputs or outputs until intentionally recaptured and re-reviewed. The repository-wide asset manifest separately covers all distributed files. These hashes are integrity metadata, not an independent digital signature.

## What was checked

The browser validator checks each route identity, fonts, local asset failures, horizontal overflow, visible action/dialog bounds, accessible input labels and linked targets. All dialogs/drawers are exercised for initial focus on direct load, focus containment, inert/hidden backdrop, a single current navigation section matching their parent, unique footer action labels, and Escape return. Four representative Phase 2 opener flows verify exact focus restoration for Escape and the close button. Cross-page Phase 1 navigation is verified; focus restoration across that page boundary is NOT_MEASURED. Linked Phase 1 backdrops are explicitly labelled reference placeholders. It also checks the explorer, purchase navigation, browser back, table search, nine non-canonical record/report selections, and the canonical report link. All 462 enabled workspace/dialog actions are exercised for an observable navigation, demo-feedback or validation outcome; this does not prove production semantics. It does not execute application IPC or real provider/device operations.

Visual inspection included contact sheets for all 214 screen compositions and selected full-size/modal/compact views, including all 41 readiness/admission outcomes and the QR publication/table dialogs. PDF samples included the cover, implementation guide, index, overview, food composition, sign-in, print reconciliation, readiness states and a compact dialog. Automated checks cover the full denominator; human-style visual sampling does not imply every pixel or every possible content combination was inspected.

Independent review identified and corrected a reversed cash-variance label, a print status that overstated physical output, document/payment actions that changed fixture identity, inconsistent import/label counts, missing readiness outcomes and implementation-ledger fields. QR publication, public visibility and table admission are represented separately. Account readiness does not imply billing admission; an unknown invoice-counter outcome retains its operation identity and blocks a fresh retry. Public fixtures use unusable phone, tax identity, payment address and URL placeholders. Review also corrected duplicate modal actions, competing navigation highlights, missing initial/return focus, silent actions, and row/report actions that substituted a different sample identity. The final captures and PDF were rebuilt after these corrections. Names and examples are authored fixtures, not merchant/customer exports.

## Publication gate

The final publication uses the existing shared timed `FULL` gate on the exact clean committed source. Its payload is `scripts/run-reference-checks.py`: eight steps covering both integrity checks, the complete source-surface inventory, all 216 Phase 1 plus 642 Phase 2 layout observations, all 29 Phase 1 plus 112 Phase 2 interactions and 462 enabled-action outcomes, and both PDF rebuilds (104 and 300 pages). Each step records wall time and its scheduling mechanism. The enforced total budget is 120 seconds. No Phase 1 coverage was removed.

Fresh run reports are intentionally generated under ignored `artifacts/`, including `full-reference-gate.json`, `phase2-validation.json` and `phase2-package-validation.json`. The publication commit and final gate outcome are recorded in a separate publication attestation outside the gated source tree and reported with the repository link. This avoids changing source identity after its gate. The baseline implementation ledger remains unassigned: visual success for this demo must never be recorded as success for the app.

## Limits and next evidence

The design is based on the inspected source revision. Phase 1 implementation may have changed that source; Gemini must inspect the current app before applying Phase 2. Source-map hashes allow drift to be detected without publishing private application code. The dirty local app checkout, private source contents, production records and runtime secrets are excluded.

The app must separately prove main-process authority, financial totals/tax, persisted operation identity, failure/stale/conflict handling, permissions, printing, scanning, sync, QR publication/intake, recovery and updates. Browser viewport sizes approximate effective client pixels, not Windows display scaling. Real Windows 100%, 125% and 150% DPI, Narrator, devices, physical paper, payment/provider behavior and production release readiness remain NOT_MEASURED.
