# Renderer source-surface inventory

`source-surface-inventory.json` is the coverage boundary for this reference. It enumerates every one of the 154 TypeScript files below `src/renderer/` in the clean private app checkout at `7932bbbedabdd0cef4295919a91674f35fa815cf`.

The JSON deliberately contains only source-relative paths, SHA-256 hashes, classifications, public reference state IDs, and rationales. It does not contain private application source. The classifications are:

| Classification | Meaning |
|---|---|
| `phase1` | A direct runtime surface anchored to an existing Phase 1 reference state. |
| `phase2` | A direct Phase 2 manifest anchor or runtime support for a named Phase 2 state. Support mapping does not claim it is a separate visual screen. |
| `shared_non_ui` | Renderer composition, controller, bridge/runtime support, generated contract/policy, type declaration, or accessibility utility without an independently registered screen. |
| `explicit_exclusion` | Test-only source; it is intentionally not a shipping UI surface. |

## Extraction and validation

Maintainers generated the manifest with:

```sh
python3 scripts/generate-phase2-source-surface-inventory.py
python3 scripts/validate-phase2-source-surface-inventory.py --app-root /path/to/windows-app-checkout
```

The first command requires the clean inspected app clone at the documented baseline. The second command works without private source for structural validation, or with `--app-root` to reject a changed/missing renderer file or hash. A downstream implementer must re-run the app-root form against their actual source and reconcile drift; the embedded baseline must not be treated as a replacement for current code review.

## Coverage status

The five formerly uncovered renderer presentation surfaces are direct Phase 2 outcome groups 246–286: account readiness, current-device claim, handover admission, invoice-counter verification, and restore-entry. Every finite presentation outcome from those source modules is separately addressable. `known_ui_gaps` is empty at this inspected baseline; the validator requires it to remain empty and self-tests both policy directions (accepts empty, rejects a non-empty probe). Any future uncovered surface requires a new reviewed reference-package revision rather than weakening this complete-package gate.

This is intentionally a gap declaration, not a request to fabricate screens or weaken acceptance. The application source still determines which of these states can be reached, what data is safe to show, and how recovery works.
