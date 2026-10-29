# Team ownership and integration

One coordinator is accountable for the result. Use native subagents only when supported by the active Antigravity surface; otherwise execute the same roles sequentially and state that limitation. Respect the available concurrency slots. Do not assume a subagent sees parent history.

## Phase assignments

| Role | Scope / owned files | Boundary |
|---|---|---|
| Coordinator | Tracker, evidence ledger, `src/renderer/main.ts`, final integration and gate scheduling | Sole writer of composition root; approves ownership transfers |
| Mapper (initial, read-only) | Current routes, capabilities, bridge methods and 72-row reconciliation | No product edits; reuse as reviewer later |
| Shell/design-system worker | `src/renderer/index.html`, `styles.css`, `navigation-state.ts`, `navigation-view.ts`, new shared presentation primitives agreed with coordinator | Complete primitive contract before feature workers rely on it |
| Billing/dialog worker | `features/billing/`, cart-facing presentation integration, billing dialog states | Sole writer of billing-cart-route; no domain calculation or privileged contract changes |
| Orders worker | `features/food-service/` presentation and corresponding route tests | Existing order/KOT/table commands only; preserve later table-cycle work when present |
| Supporting-workflows worker | Explicitly assigned customer, documents, inventory, reporting, financial, marketing, operator and print-center route subsets | Split into smaller workers only with disjoint files; no simultaneous shared CSS edits |
| Independent reviewer | Read-only screenshots, user paths, final diff, tests and authority boundaries | Must not approve its own changes; reports concrete failures and evidence |

This is a set of roles, not a requirement to start all agents at once. For four slots, use coordinator + mapper + shell + reviewer early; then coordinator + billing + orders + supporting worker after shell integration. Reuse mapper/reviewer capacity at phase boundaries. Keep test/build ownership central.

## Shared-file rule

Feature workers request global CSS/navigation/entrypoint edits from their owner. They may produce scoped style proposals or own a new feature stylesheet only after the asset inclusion is agreed. Do not split the 2,334-line billing route across multiple writers. Extract small view helpers only to enable this redesign; do not undertake an unrelated architecture rewrite.

Generated wire files are generated through the current repository tooling. No hand edits. A missing visual control does not justify changing IPC/global bridge types.

## Worker task template

> Read the app's current rules, task tracker, reference GEMINI.md, CODEBASE-MAP.md and PRODUCTION-BOUNDARIES.md. Your exact screen IDs are [...]; your only writable files are [...]. Use [prototype links], [PNG paths], and [controller symbols]. Implement presentation while preserving the named production actions and all current states. You are not alone: do not revert other workers' edits. Ask the coordinator for shared-file changes. Before finishing, report the diff, tests and durations, screenshots at the assigned sizes, affected coverage rows, and unresolved gaps. Do not push, merge, deploy or touch live data.

## Integration contract

Before each phase, record owned paths and current HEAD. Workers return patches/commits against that base and evidence tied to their code. The coordinator integrates non-overlapping changes, resolves conflicts using current behavior, reruns impacted checks and updates the tracker. No repeated status requests when local evidence already answers them. No communication with unrelated chats/tasks.

The final reviewer evaluates the integrated app, not isolated worker screenshots. Completed phases need integrated source and evidence. Empty progress messages, process activity and unverified success claims do not count as completed work.
