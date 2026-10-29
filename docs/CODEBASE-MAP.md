# Windows application code map

## Baseline and reconciliation rule

This map describes the clean remote `main` of [`Shreyash-K/android-billing-desktop`](https://github.com/Shreyash-K/android-billing-desktop) at **`7932bbbedabdd0cef4295919a91674f35fa815cf`** (inspected 29 October 2026). Check the current commit before editing and update this map when paths or contracts have moved.

The observed local checkout was at `6717d4c9703bf821b45e77094b410a184ff9c236` with 49 modified or untracked paths. It is not the source of truth for this handoff and none of those changes were included. In particular, its uncommitted retail/shop-order IPC/runtime work, a `table_cycle_advanced` food-service change, and an inventory sync-v2 method are absent from the remote baseline. Do not reset, stage, overwrite, or depend on them. Start in a clean branch/worktree and reconcile them with their owner separately.

## Renderer architecture

The desktop app is **plain TypeScript that builds DOM elements** inside Electron. It is not React, Vue, or a component framework. Preserve that architecture unless a separate, approved migration says otherwise.

| Responsibility | Current path / stable seam | Redesign guidance |
|---|---|---|
| Static accessible shell | `src/renderer/index.html` | Keep static landmarks and the named mounts: `#app-bar`, `#app-nav`, `#main-content`, `#more-nav`, `#route-content`, `#command-palette`. Add a shared dialog host here only if the integration owner owns the shell. |
| Renderer boot and composition | `src/renderer/main.ts`, `boot(region)` | One integration owner. It selects routes, installs keyboard/scanner behavior, composes controllers, and is a likely conflict point with excluded local work. |
| Route state | `src/renderer/navigation-state.ts`, `createNavigationState(...)` | Keep route/page state and existing destinations; do not make a second navigation store. |
| Navigation renderer | `src/renderer/navigation-view.ts`, `renderNavigation(...)`, `NavigationRouteRenderer`, `NavigationDocument` | It replaces route children deterministically and restores focus by element ID. Overlay state must survive/repaint through the route owner. |
| Global visual system | `src/renderer/styles.css` | One design-system owner. This is the 861-line global CSS file; extend semantic tokens and responsive rules rather than scatter per-screen inline styles. |
| Renderer bridge typing | `src/renderer/global.d.ts` | Use the existing named `window.biteaze` surface. Pure visual work should not require a change here. |

`index.html` deliberately holds the landmark frame as literal static markup for accessibility. Renderer code paints only into its mounts. `renderNavigation()` replaces children on each repaint and restores focus/selection where it can; preserve that behavior when replacing inline views with richer layouts.

The app CSP already allows same-origin fonts (`font-src 'self'`). The bundled Inter and Plus Jakarta Sans assets may therefore be added as local assets through the normal build/static-asset process. Do not load external fonts or weaken CSP.

## Existing destinations and likely design mappings

The primary runtime destinations are `dashboard` (when enabled), `billing`, `customers`, `inventory`, and `more`. `more` currently contains:

- Financial: `suppliers`, `purchases`, `expenses`, `cash`, `financial-reports`
- Reporting: `gst-filing`, `day-close`
- Documents: `sales-history`, `quotations`, `delivery-challans`
- Operations: `print-center`, `barcode-labels`, `support-health`, `legal-ops`, `profile`, `sync_review`, `setup`, `onboarding-wizard`
- Conditional vertical destinations: `food-service`, `category-adaptation`, `category-reports`, `appointments`, `jobs`
- Marketing functionality is currently presented from the More menu rather than a separate route.

Use these paths as the initial implementation ownership map:

| Reference area | Existing code | Required reconciliation |
|---|---|---|
| Billing workspace, item configuration, cart, customer/staff attachment, discounts, coupons, hold/resume, payment and completion | `src/renderer/features/billing/billing-cart-route.ts` | One billing owner. Re-layout it around the existing workspaces/controllers. Retain drafts, revisions, retry, lifecycle invalidation and customer-display publication. |
| Food service: active orders, dine-in/takeaway, menu modifiers, tables, transfer/merge/split, KOT, menu publishing, table QR | `src/renderer/features/food-service/food-service-route.ts`; `FoodServiceRouteRenderer.focusOrder(orderId)` | Make proposed orders/tables views presentation over this workspace. It is not a second order engine. |
| Sales history, return and void | `src/renderer/features/documents/documents-route.ts`, `documents-controller.ts` | Surface refund/void from Sales History; preserve its existing preview and confirmation flow. |
| Customers / credit | `src/renderer/features/customers/customer-khata-route.ts`, `customer-khata-controller.ts` | Rework presentation only; avoid native `window.confirm` only after replacing it with an accessible route-owned confirmation. |
| Catalog/inventory | `src/renderer/features/inventory/inventory-route.ts`, `inventory-workspace-controller.ts` | Preserve stock authority and catalog loading. |
| Suppliers, expenses, cash and reports | `src/renderer/features/financial/*`, `reporting/*` | Use existing destinations and controllers before adding a new page. |
| Coupons / promotions / loyalty | `src/renderer/features/marketing/marketing-route.ts` | Keep current consent/reversal/promotion behavior reachable. |
| Operator settings, staff and printer configuration | `src/renderer/features/operator-experience/operator-experience-route.ts`, controller; `print-center/*` | Split visual sections only after confirming existing commands and permissions. |
| Barcode labels | `src/renderer/features/barcode-labels/barcode-label-route.ts` | Preserve its explicit print/label workflow. |

## Billing is the main integration hotspot

`src/renderer/features/billing/billing-cart-route.ts` is currently a large, stateful route (about 2,334 lines) that combines state, command handling, validation and DOM rendering. Its public renderer surface is:

```ts
interface BillingCartRouteRenderer extends NavigationRouteRenderer {
  addProduct(productId, selectedVariationId?): boolean;
  hasOpenCart(): boolean;
  deactivate(): void;
  invalidate(): void;
}
```

Keep its use of:

- `createCartWorkspace(...)` for authoritative total presentation;
- `createItemConfigurationWorkspace(...)` for modifier/configuration state;
- `createDocumentsController(...)` for documents and checkout;
- `createInventoryWorkspaceController(...)` for the catalog;
- operation IDs, payment revisions, fingerprints, retry handling and stale-response protection;
- `deactivate()` / `invalidate()` and update deferral while there is an open cart.

The concrete broken visual seam is useful: the route emits `.billing-parties`, `.billing-held-orders`, `.billing-held-order`, `.billing-catalog`, `.billing-product`, `.billing-item-configuration`, `.billing-cart`, `.billing-cart-line`, `.billing-promotions`, and `.billing-action`, but the remote stylesheet has no matching rules. Build the desktop layout by styling and structuring these real semantics, then introduce small route-owned components only where that makes state ownership clearer.

Payment remains a two-stage process: persist a durable checkout draft, request an authoritative payment preview, then complete with `SAVE` or `PRINT`. The valid modes are `CASH`, `UPI`, `CARD`, and `CREDIT`. A polished payment dialog must still reflect the returned state; it must not suggest bank/card verification or payment success where none exists.

## Dialogs, shortcuts and proposed-screen gaps

There is no generic modal host today; the command palette is the sole true shell overlay. Billing confirmations/configuration/payment outcomes are inline, and session gates replace the main region. A shared native `<dialog>` (or equivalent accessible dialog) can be added at the shell level, but its content/state belongs to the owning route. It needs focus entry/return, Escape behavior, an inert background and a body scroller with header/footer outside it. Do not add a parallel cart, order or payment store.

The keyboard registry includes product search, quantities, customer, hold/resume, discounts, tender, completion, reprint, KOT, drawer, product and PLU shortcuts. The current dispatcher actually wires only PLU; other visible shortcuts report “not connected.” Treat that as a behavior gap: do not present a shortcut as live until a route-aware `MerchantKeyboardActionPort` is implemented and tested.

The reference kit intentionally proposes some surfaces not established as remote behavior:

| Proposed reference state | Remote capability status | Implementation rule |
|---|---|---|
| Split tender | No dedicated renderer state found | Do not invent a payment allocation authority; record it as a contract gap. |
| Delivery and delivery details | Food service currently exposes dine-in/takeaway | Do not fabricate delivery dispatch data. |
| Visual floor plan | Table operations exist, no floor-plan model found | Use a truthful list/grid until an authoritative floor-plan model exists. |
| Generic manager-PIN modal / lock screen | No shared billing authority/state found | Do not copy demo PIN logic. Integrate only real role/auth outcomes. |
| Printer/KOT error dialogs | Canonical queue states exist, no shared UI dialog system | Render actual queue/availability outcomes; do not make a “reprint succeeded” preview. |
| Rich split-bill UI | Food service splits a selected line/quantity | Map only to the existing command semantics. |

Generated files under `src/renderer/generated/` are not hand-edit targets. Pure visual work should not need updates to preload, the shared IPC contract or the main process.

## Shared-file ownership for a team

Give one coordinator ownership of `main.ts`, `index.html`, `styles.css`, `navigation-state.ts`, and `navigation-view.ts`. Give a single billing worker ownership of `billing-cart-route.ts`; a separate food-service worker owns `food-service-route.ts` and its wire; remaining-feature workers own their non-overlapping routes. The coordinator integrates only after reviewing each change against the tracker and the current base. All workers must preserve changes made by others.

For the visual source of truth, see `../reference/design/index.html`, `../reference/design/design.css`, `../reference/design/screen-manifest.json`, the 72 screenshots, and [`SCREEN-COVERAGE.csv`](SCREEN-COVERAGE.csv). For non-negotiable authority boundaries, see [`PRODUCTION-BOUNDARIES.md`](PRODUCTION-BOUNDARIES.md).
