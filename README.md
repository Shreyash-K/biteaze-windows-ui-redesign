# Biteaze Windows UI redesign — Gemini / Antigravity handoff

**Start with [START-HERE.md](START-HERE.md), then paste [GEMINI-START-PROMPT.md](GEMINI-START-PROMPT.md) into Antigravity.**

This private repository contains the complete reference kit and a code-informed implementation plan for the existing Windows app. It is not a replacement application or a claim that the redesign has been implemented.

| Need | File |
|---|---|
| Copy-paste instruction | [GEMINI-START-PROMPT.md](GEMINI-START-PROMPT.md) |
| Persistent agent context | [GEMINI.md](GEMINI.md) |
| Actual app source / inspected revision | [app-source.json](app-source.json) |
| Code map and integration seams | [docs/CODEBASE-MAP.md](docs/CODEBASE-MAP.md) |
| Every screen and implementation evidence row | [docs/SCREEN-COVERAGE.csv](docs/SCREEN-COVERAGE.csv) |
| Step-by-step build plan and team ownership | [docs/IMPLEMENTATION-PLAN.md](docs/IMPLEMENTATION-PLAN.md) |
| Business and security boundaries | [docs/PRODUCTION-BOUNDARIES.md](docs/PRODUCTION-BOUNDARIES.md) |
| Visual matching and validation | [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) |
| 104-page design book | [reference/Biteaze-Windows-UI-Reference.pdf](reference/Biteaze-Windows-UI-Reference.pdf) |
| Offline interactive demo / editable HTML, CSS and JS | [reference/design/index.html](reference/design/index.html) |
| 72 full-HD screenshots + 14 continuations | [reference/design/screens](reference/design/screens) |
| 12 compact examples | [reference/design/responsive](reference/design/responsive) |
| Fonts, licences, tokens | [reference/design/assets](reference/design/assets) |
| Original 33-page tablet reference | [reference/Android-tablet-original.pdf](reference/Android-tablet-original.pdf) |
| Measured reference evidence / limitations | [docs/EVIDENCE.md](docs/EVIDENCE.md) |
| Package integrity | [asset-manifest.json](asset-manifest.json) |
| Validation and PDF rebuild source | [docs/REFERENCE-TOOLING.md](docs/REFERENCE-TOOLING.md) |

## Preview

Download or clone this repository. Open `reference/design/index.html` locally, or run:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8765/reference/design/index.html`. On Windows, `py -m http.server 8765 --bind 127.0.0.1` is the equivalent. GitHub displays source HTML; it does not run this private interactive demo directly.

## Application repository

[Shreyash-K/android-billing-desktop](https://github.com/Shreyash-K/android-billing-desktop) is the production code repository. Both repositories require access to the owner's GitHub account. The inspected remote baseline is `7932bbbedabdd0cef4295919a91674f35fa815cf`. Reconcile newer source before editing; this kit does not freeze development on that revision.

The local checkout had 49 uncommitted/untracked entries and an older HEAD. Those changes are not included here. They must not be reset or silently assumed to exist in GitHub. The clean remote snapshot was inspected separately.

## Scope and authority

Reproduce the supplied desktop visual design across all 72 reference states and preserve existing app capabilities. The live app owns business rules, authentication, data, payments, tax, stock and printing. The reference owns visual hierarchy, layout, component appearance and proposed view states. Missing capabilities must be explicitly tracked; never make demo behavior appear operational.

The original design guide/PDF correctly says the Windows code was not inspected when version one was produced. The later code inspection and implementation instructions live in this repository's `docs/` directory. No product implementation or native Windows qualification is claimed by these documents.

Confidential: the supplied tablet PDF contains outlet/account context. Keep this repository private. All sample customers and transactions in the new desktop prototype are illustrative.
