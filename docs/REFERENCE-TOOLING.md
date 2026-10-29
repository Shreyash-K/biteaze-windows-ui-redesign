# Reproduce the reference checks and PDF

These tools operate only on this design package. They do not test or modify the Electron application. The demo runs without installation; dependencies are needed only for validation or PDF regeneration.

## Setup

From this repository root, use Python 3.10+ and a supported Node.js runtime:

```sh
python3 -m venv .venv
```

Activate the virtual environment for your shell (`source .venv/bin/activate` on macOS/Linux, `.venv\Scripts\Activate.ps1` in Windows PowerShell), then:

```sh
python -m pip install -r requirements.txt
npm ci --ignore-scripts
npx playwright install chromium
```

An existing Chrome/Chromium can be used instead by setting `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` to its absolute executable path. A managed environment can resolve an already-installed Playwright through Node's standard `NODE_PATH`. No dependency install is needed to open the offline demo.

## Full reference-package validation

```sh
python scripts/validate-package.py
npm run validate:reference
npm run validate:interactions
python scripts/validate-phase2-package.py
npm run validate:phase2
```

`python scripts/run-reference-checks.py` runs the complete reference gate payload, including both PDF rebuilds, and records each step's duration and scheduling mechanism in `artifacts/full-reference-gate.json`.

The integrity check covers every distributed file, all 72 coverage rows, 98 PNG dimensions, 104-page design PDF, 33-page input PDF, and static local dependencies. The browser check loads every state at 1920×1080, 1366×768 and 1280×720 (216 observations), checking errors, asset loading, screen identity, overflow, dialogs and checkout visibility. The interaction suite checks 29 representative **demo** interactions, including illustrative arithmetic/PIN/payment states that must never be copied as production authority.

Phase 2 adds all 214 screen states, 174 audited requirement entries, and regenerated screenshot/PDF assets. Its browser validator covers all three sizes (642 observations) using three concurrent pages in one Chromium process, plus 112 demo interaction checks and 462 enabled-action outcomes. Together the FULL gate retains all 858 layout observations and 141 interactions plus 462 action outcomes. Capture-source hashes bind the supplied Phase 2 PNG/PDF evidence to the published demo inputs.

Reports are written to ignored `artifacts/`. To recapture Phase 1 into its validation artifacts:

```sh
npm run validate:reference -- --capture
```

To intentionally replace the supplied Phase 2 captures after an approved design revision, run `npm run validate:phase2 -- --capture`. This writes the Phase 2 PNGs, manifest, continuation and responsive indices in place; rebuild the PDF, regenerate coverage, then run `python scripts/record-phase2-capture.py` as the final capture-binding step. It refreshes hash evidence only after all reviewed outputs are in place.

The original reference reports remain in `reference/design/` as provenance. New reports do not establish native Windows, hardware, provider, security or app behavior qualification.

## PDF generation source

```sh
python scripts/build-design-book.py
python scripts/build-phase2-book.py
```

This rebuilds the 104-page original book from the supplied screen PNGs and fonts into `artifacts/pdf/`, including a regenerated page map and temporary font instances. It never overwrites the canonical PDF or reference source. The source preserves the original design-book content; the newer code-informed instructions are in `docs/`. The Phase 2 builder writes its dynamic-page-count book and page map to `artifacts/phase2-pdf/`; copy reviewed outputs into `phase-2-remaining-screens/`, rerun `python scripts/build-phase2-coverage.py` to update page links, then run `python scripts/record-phase2-capture.py`. This coverage generator intentionally resets implementation status to the blank handoff baseline: do not run it on a live implementation evidence ledger. Source metadata stays pinned unless `--source-root` is explicitly supplied.

Font/report-library changes and PDF metadata can change binary output without changing the design.

## Intentional reference revisions

The manifest is integrity metadata, not a signature from an external authority. After an intentional reviewed reference change, regenerate it and rerun the complete package checks:

```sh
python scripts/generate-manifest.py
```

Do not regenerate it merely to hide missing or modified assets. Preserve the original design when implementing in the separate application repository.

For this publication, the owner’s shared `~/.autoloop-harness/run-gate.sh` enforces a FULL, exact-source reference gate with a 120-second budget. The gate retains all 216 Phase 1 and 642 Phase 2 required state/size pairs, all 141 demo interactions and 462 action outcomes, both package checks, source-surface inventory validation, and both PDF rebuilds. Phase 2 uses three concurrent viewport pages in one Chromium process; other steps are sequential to bound memory. Every step records its duration and mechanism; no coverage is dropped. A fixed budget is enforced instead of an unmeasured loop. Recalibrate only from measured evidence when tooling or coverage changes. The actual app has its own, separate canonical FULL gate and budgets.
