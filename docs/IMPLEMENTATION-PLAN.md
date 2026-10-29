# Implementation plan

Use a single continuing implementation session with explicit phase boundaries. This plan is for the existing app, not for rewriting the reference prototype. Completion is evidence-based; session duration cannot guarantee absent backend capabilities or hardware verification.

## 0 — Reconcile source and establish evidence

- Read the current app's AGENTS/GEMINI instructions, coordination state, build-token rules, architecture, package scripts and gate policy. Record branch, HEAD, dirty status and active owners. The handoff baseline is in `app-source.json`.
- Use the current authorized app checkout. If local work must be excluded, use an isolated worktree or clean clone and record that fact; do not reset/stash someone else's work. Never copy dirty main/preload/retail additions from the inspected machine without ownership reconciliation.
- Run the reference locally and inspect every screen, continuation and compact example. Save before screenshots of the actual app using synthetic fixtures. Don't trigger live merchant actions to obtain screenshots.
- Copy the tracker template and 72-row coverage CSV into the app's task docs. Inventory additional current app routes. Reconcile each screen with real controller methods, state tags, revision requirements and permission checks. Mark exact missing authority separately from missing UI.
- Establish environment/tool prerequisites and test baseline. Record pre-existing failures separately; don't weaken tests. Preserve the existing shared harness; install its project hook only when absent and permitted by the app's instructions. Chain existing hooks. Never replace the gate.

Deliver: source inventory, route-to-reference mapping, ownership table, before screenshots, test baseline and gap decisions. Proceed to implementation without an unnecessary approval pause for ordinary UI edits.

## 1 — Shell and reusable visual primitives

- Coordinator/shell owner implements semantic shell, navigation rail, outlet/status context, dialog/drawer host, spacing/typography tokens and adaptive layout.
- Add local Inter and Plus Jakarta Sans with licenses through the app's existing asset pipeline and CSP. Use approved current Biteaze assets instead of the prototype's concept “b” mark.
- Add controls/panels/tables/tags/empty states/dialog primitives only where needed by the requested UI. Preserve existing localization keys, accessibility landmarks and meaningful DOM contracts.
- Keep `#app-bar`, `#app-nav`, `#main-content`, `#more-nav`, `#route-content` and command palette semantics compatible with navigation tests. A dialog host outside route repainting must preserve focus and route lifecycle.
- Resolve current absent billing class styling with structured layout, not arbitrary absolute positioning. Keep feature selectors scoped, avoid global button/table overrides that break other routes.
- Shell integration must precede parallel feature work. Publish the component contracts and owned files in the tracker.

Deliver: shell + primitives with reference screenshots at all three sizes; route smoke tests and contrast checks.

## 2 — Core billing and order workflows

- Billing owner transforms the current long inline billing route into catalog + fixed bill panel + contextual dialogs/drawers, using existing workspaces/controllers.
- Preserve cart state, decimal values, attribution, quotations/challan restore, discounts/coupons/loyalty, drafts, held bills, previews, customer display and update deferral.
- Modifiers/line edits/customer/order note/discount/hold/discard are views over the current state and commands. Closing an overlay must not reset the cart or authorize an operation.
- Orders worker implements running-order/table/transfer/split/KOT views over food-service commands, preserving selected-order focus and existing state transitions. A visual floor plan is proposed; persisted placement needs supported storage, not a made-up local store.
- Payment owner (same billing owner) retains durable checkout draft → authoritative payment preview → explicit SAVE/PRINT completion. Wire all response variants and retries; payment failure and print failure are separate.
- Do not enable split tender, delivery, manager approval or any other unsupported flow merely because the demo has it. Determine current support first; render truthful unavailable/denied states and file a precise gap if absent.

Deliver: all applicable billing/order screen rows, behavior tests and screenshot evidence, remaining authority gaps stated.

## 3 — Supporting screens and settings

- Reskin sales/detail/refund/void, day close, expenses, suppliers, customers/credit, inventory/item editing, reporting, dashboard, marketing and settings by adapting existing route renderers.
- Settings subsections can become organized pages/drawers while retaining existing actions, controls and backend validations. Preserve printable template semantics, printer-role separation, widths, operator restrictions and real data sources.
- Keep app capabilities that are outside the 72-state proposal: onboarding/auth/admission, quotations, delivery challans, purchases, GST filing, support/health, barcode labels, sync review, category adaptations, appointments/jobs and legal/operations where available. Apply the common shell/components without inventing feature flows.
- Never drop form fields or current permissions because the screenshot doesn't contain them. Use an “Advanced” or suitable existing detail section and record the adaptation.

Deliver: remaining reference rows + preserved-route inventory; no unreachable existing workflows.

## 4 — Keyboard, accessibility and behavior integration

- Connect only commands that have real route-aware actions. Current remote keyboard wiring primarily handles PLU; advertise a shortcut only after it works and is covered.
- Test search, scanner focus, quantity changes, customer selection, navigation, dialog focus loop/return, Escape, disabled states, asynchronous cancellation/stale response and form retention.
- Resolve palette/Escape/overlay priority centrally. Prevent double submissions while keeping authoritative retry/recovery available. Confirm no event-listener leaks after route transitions.
- Adapt long Hindi/Gujarati labels, large text, reduced motion, high contrast and keyboard-only operation with existing localization infrastructure.

Deliver: integration tests, accessibility findings, resolved route/overlay/shortcut conflicts.

## 5 — Complete visual and correctness gate

- Review every one of the 72 rows against the reference at all three client sizes. Include long-scroll content and all relevant statuses, not merely default routes.
- Capture actual app results, reference comparison views and reviewer findings. Fix layout inconsistencies before final gate.
- Run required app-focused checks during iteration; on the final committed clean source run `npm run gate:canonical-full` plus applicable existing visual/contrast/QA checks. Follow current app policy if it differs from this snapshot. Full coverage must not be replaced with a faster subset.
- Preserve already-valid checks. If a repeated gate exceeds budget or 1.5× measured floor without a budget, stop equivalent repeats, repair scheduling with the same denominator, and prove budget acceptance/rejection before resuming. One coordinator owns native rebuild/build-token scheduling.
- Independent reviewer inspects the exact final diff, screen evidence, unresolved gaps and boundary preservation. Review fixes require appropriate revalidation.

Deliver: tracker, 72-row coverage, preserved-feature inventory, before/after screenshots, gate reports/durations and logical commits. App push/merge/release is not part of this handoff's authorization.
