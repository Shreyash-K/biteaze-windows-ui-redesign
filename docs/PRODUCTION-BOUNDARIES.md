# Production boundaries for the UI redesign

## Scope

These constraints apply to the clean remote baseline `7932bbbedabdd0cef4295919a91674f35fa815cf` of the Windows app. The reference PDF, screenshots and `reference/design` demo define appearance and proposed UI states. They do **not** grant authority to change financial, security, data, printer or provider behavior.

The remote IPC contract version is **38**. A dirty local checkout had an uncommitted version 39 plus retail-order work; those local changes are not part of the baseline. Never treat a local file as established production behavior merely because it exists on one machine.

## Layer and security boundary

`docs/ARCHITECTURE.md` in the application repository is the detailed authority map. In brief:

| Layer | Owns | UI redesign rule |
|---|---|---|
| Renderer | Presentation and user interaction | Consume named bridge/controller results. Do not access filesystem, database, tokens, keys, printer, updater, OS integrations or provider APIs. |
| Preload | Narrow named bridge | Do not expose raw `ipcRenderer`; do not widen it for cosmetic convenience. |
| Main | Privileged operations, persistence, printing, provider orchestration | Retain validation and opaque error handling. |
| Shared/domain engine | Contracts and business calculations | Do not recreate money logic in TypeScript UI code. |

`src/main/security.ts` supplies hardened BrowserWindow preferences: sandbox and context isolation enabled; Node integration, worker/subframe Node, webviews and insecure content disabled. Preserve these settings and the restrictive CSP. Local assets are allowed under `font-src 'self'`; external font/network loosening is not required.

`src/shared/ipc-contract.ts` is a closed registry. `src/main/ipc-router.ts` accepts declared channels once, verifies the trusted sender/frame, returns opaque handler failures, and `assertContractFullyServed()` runs before the window opens. A genuine new capability requires the explicit shared contract, main handler, preload exposure, bounded parsing, test coverage and registration. A visual requirement is not a reason to create new IPC.

## Billing, payment and document authority

The renderer must render values and state returned by the production paths. It must not compute or infer them independently.

| Concern | Canonical paths / seam | Preserve |
|---|---|---|
| Checkout totals | `src/preload/billing-totals-bridge.ts`; `src/main/billing/register-billing-totals-handler.ts`; `vendor/billing-domain/android-billing-billing-domain.js`; `com.example.core.js.BillingEngines.computeCheckoutTotals` | Tax, rounding, quantity, discount, payable and change. Cart requests/responses are bounded, including a maximum of 100 lines. |
| Documents / draft lifecycle | `src/preload/documents-bridge.ts`; `src/shared/documents-contract.ts`; `src/main/documents/register-document-handlers.ts` | Drafts, checkout policy, parties, holds/resume/cancel, history, reprint, return, void, credit authorization/lifecycle, exact operation IDs and revisions. |
| Checkout completion | `src/main/billing/cash-checkout-service.ts`; `checkout-shared-authority.ts`; `cash-checkout-authority-provider.ts`; `sqlcipher-p4-8-commit-document-store.ts` | Preview → returned `paymentRevision` → completion. Only main owns identity, payable amount, stock, khata, receipt facts and commit authority. |
| Inventory | `src/main/inventory/inventory-command-service.ts`; `sqlcipher-inventory-store.ts`; `inventory-runtime.ts`; `ci/contracts/store-registry.json` | Renderer input is untrusted. Keep main validation, revisions/CAS and the existing single availability model. |

Meaningful document/payment results include `ready`, `committed`, and `queued`, plus `invalid`, `denied`, `stale`, `unavailable`, `not_found`, `conflict`, `incomplete`, and `refused`. Design every relevant result visibly. Pending, denied, stale or offline is not success.

Never copy these demonstration-only behaviors into the application:

- sample price arithmetic, payment totals or change calculations from `reference/design/*.js`;
- the reference demo’s accepting six-digit PIN;
- placeholder QR payloads, fake card references or automatic payment success;
- synthetic customer/contact, inventory or availability data as a substitute for a controller result;
- a success toast that bypasses durable save/preview/complete authority.

If the reference calls for a flow that lacks backend authority—such as split tender, delivery dispatch detail, a manager approval ceremony or floor-plan persistence—describe the missing contract in the coverage tracker and keep the UI truthful. Do not fabricate it in the renderer.

## Printing and operational states

Use `src/main/printing/production-printing-runtime.ts`, `print-queue.ts`, `src/shared/printing/print-center-contract.ts`, and `src/main/billing/production-p4-9-receipt-print.ts` as the authority. Roles are separate: `receipt`, `kot`, `report`, `a4`, and `label`; thermal widths include `MM58` and `MM80`. A receipt must never fall back to a KOT route.

Show canonical queue/workspace states such as queued, sending, failed, printed, cancelled, retry-exhausted, ready, offline and unavailable. Main composes printable content from committed receipt facts. The UI must not print a prototype, report a successful print because a dialog closed, or route an arbitrary document to an available printer.

## Changes that are allowed in this redesign

The implementation may change renderer layout, HTML structure, CSS, local font packaging, accessible components, dialog presentation, responsive behavior, labels and state mapping. It may use the existing controllers and named `window.biteaze` bridge methods. It may add meaningful renderer tests for the changed interaction and visual/DOM contracts.

It must preserve existing command objects, operation IDs, revisions, confirmations, permission checks, localization and error outcomes. It must keep unrelated app capabilities reachable. It must not replace the current renderer with the reference demo, install a new UI framework merely to reproduce visuals, expose privileged APIs, add a second store, weaken CSP/security settings, or make any live payment, message, destructive data, account, or deployment action.

## Verification and qualification limits

Use the current application instructions and scripts for execution; this document does not replace them. The remote baseline expects Node `22.22.1` and npm `10.9.4`. Its final project gate is `npm run gate:canonical-full`, and it has a clean-tree, exact-source, FULL-evidence requirement. Focused renderer checks help iteration but cannot substitute for the canonical final gate when theme, navigation or billing wiring changes.

The application is documented as `IMPLEMENTED_UNQUALIFIED`: prior qualification is macOS-only. Passing tests/builds cannot demonstrate Windows installation, display scaling, physical receipt printers, USB/RAW hardware, payment providers, live stock/payment operation, or on-device accessibility. These remain `NOT_MEASURED` until directly tested. See [`ACCEPTANCE.md`](ACCEPTANCE.md) for the handoff’s required evidence matrix.
