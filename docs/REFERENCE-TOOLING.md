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
```

`python scripts/run-reference-checks.py` runs the complete reference gate payload, including the PDF rebuild, and records each step's duration and scheduling mechanism in `artifacts/full-reference-gate.json`.

The integrity check covers every distributed file, all 72 coverage rows, 98 PNG dimensions, 104-page design PDF, 33-page input PDF, and static local dependencies. The browser check loads every state at 1920×1080, 1366×768 and 1280×720 (216 observations), checking errors, asset loading, screen identity, overflow, dialogs and checkout visibility. The interaction suite checks 29 representative **demo** interactions, including illustrative arithmetic/PIN/payment states that must never be copied as production authority.

Reports are written to ignored `artifacts/`. To capture a fresh set of 216 reference screenshots without overwriting supplied assets:

```sh
npm run validate:reference -- --capture
```

The original reference reports remain in `reference/design/` as provenance. New reports do not establish native Windows, hardware, provider, security or app behavior qualification.

## PDF generation source

```sh
python scripts/build-design-book.py
```

This rebuilds the 104-page original book from the supplied screen PNGs and fonts into `artifacts/pdf/`, including a regenerated page map and temporary font instances. It never overwrites the canonical PDF or reference source. The source preserves the original design-book content; the newer code-informed instructions are in `docs/`. Font/report-library changes and PDF metadata can change binary output without changing the design.

## Intentional reference revisions

The manifest is integrity metadata, not a signature from an external authority. After an intentional reviewed reference change, regenerate it and rerun the complete package checks:

```sh
python scripts/generate-manifest.py
```

Do not regenerate it merely to hide missing or modified assets. Preserve the original design when implementing in the separate application repository.

For this publication, the owner’s shared `~/.autoloop-harness/run-gate.sh` enforces a FULL, exact-source reference gate with a 120-second budget. The scheduling mechanism is one Chromium instance, all 216 required state/size pairs, followed by the 29 demo interactions and PDF rebuild; no coverage is dropped. A fixed budget is enforced instead of an unmeasured loop. Recalibrate only from measured evidence when tooling or coverage changes. The actual app has its own, separate canonical FULL gate and budgets.
