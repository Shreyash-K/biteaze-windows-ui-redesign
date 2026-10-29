# Evidence and provenance

## Reference kit, produced before code inspection

- 72 screens/states; 72 full-HD PNGs, 14 scroll continuations, 12 compact PNGs.
- 104-page PDF; original 33-page tablet PDF included separately.
- 216 reference layout measurements: no measured horizontal overflow, outside-viewport dialog footer or JavaScript errors; 26.622s.
- 29 representative local prototype interaction checks passed; 2.530s.
- 9 explorer views checked; 72 guide links; 2.242s.
- PDF geometry/image/text checks passed; 0.955s.

Original reports are in `reference/design/*validation.json` and `VALIDATION-SUMMARY.json`. Those results test the illustrative reference, not the Windows application. They do not establish live business behavior, complete accessibility conformance or native device readiness.

## Later source inspection

A clean GitHub snapshot of `Shreyash-K/android-billing-desktop` was inspected at `7932bbbedabdd0cef4295919a91674f35fa815cf`. `app-source.json` records identity and local divergence. `docs/INSPECTED-SOURCE-HASHES.json` records hashes of key inspected files to help detect drift; it is not a complete code audit. The older local checkout at 6717d4c had 49 dirty paths. No local application edits were uploaded or modified in preparing this handoff.

Inspection found plain TypeScript DOM route renderers, existing authoritative bridge/controllers, absent styles for billing classes, inline dialogs/payment, and several proposed capabilities not established remotely. Read CODEBASE-MAP and PRODUCTION-BOUNDARIES for exact seams and limitations.

## Package checks

`python3 scripts/validate-package.py` checks all manifest hashes, the complete 72-row mapping, PNG geometry, local HTML dependencies and PDF page counts/geometry. `npm run validate:reference` loads all 72 states at 3 sizes and checks errors/overflow/visible dialog footers in the relocated package. Its complete scope is the reference only. The shared gate receipt for publication lives in Git metadata outside tracked content and binds the final repository content; publication metadata is reported separately. See [REFERENCE-TOOLING.md](REFERENCE-TOOLING.md) for reproducible commands and [the independent review](../evidence/HANDOFF-REVIEW.md) for its bounded scope.

## Not performed

No application source implementation, native Windows run, current app full test gate, production deployment, live payment, printer job, customer message or merchant-data mutation was performed for this documentation delivery. Those are not implied by reference/package checks.

## Design research

- [Petpooja restaurant billing](https://www.petpooja.com/poss/restaurant-billing-software)
- [Square floor-plan management](https://squareup.com/help/us/en/article/6427-building-your-floor-plan)
- [Lightspeed order split/merge](https://o-series-support.lightspeedhq.com/hc/en-us/articles/31329418475419-Merging-or-splitting-orders)
- [Microsoft effective-pixel layout guidance](https://learn.microsoft.com/en-ca/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design)

The desktop proposal is an original application of these workflow ideas to the supplied Biteaze tablet theme; it is not copied vendor UI or proof of feature parity.
