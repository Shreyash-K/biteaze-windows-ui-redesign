# Biteaze for Windows · UI implementation reference

Version 1 · 29 October 2026 · Viral Patiyala sample outlet

This is a proposed desktop design system and visual reference, with 72 named screen states. It includes an offline clickable HTML prototype, screenshots, a PDF design book, and these implementation notes. The source is the supplied 33-page Android tablet reference, plus the official POS and Microsoft references listed below. The existing Windows codebase was not inspected or changed.

## Open the reference

Open `index.html` in a desktop browser. The dark reference strip at the bottom is a design explorer, not part of the proposed app. Select any screen, use the previous/next controls, or click the relevant app actions. All fonts and assets are local; no install or network connection is required. The PNG files in `screens/` show the app without the explorer.

The prototype uses synthetic people, masked contact information, illustrative prices and a demonstration bill. Search, item addition, modifier pricing, discounts, cash change, split tender, customer selection and selected keyboard paths work locally. Many secondary actions show the next design state or a preview notification. Forms, exports, printing, sync, receipts and account changes are not connected to production. Reload to reset the examples. The demo PIN accepts any six digits; it is not an authentication implementation. Payment QR panels are deliberately non-payable placeholders.

## Design direction

Keep Biteaze’s light slate surfaces, orange brand accent and rounded geometry. Use orange for the next important action and the current selection. The result should feel like a calm counter workspace: prices aligned, fewer competing buttons, clear order status and a consistent location for checkout.

The primary layout has a labelled application rail, an outlet/staff header, a catalog workspace and a persistent bill on the right. Category navigation and item search are immediately available. Menu items use text-first tiles so missing photography does not damage the layout. A native window title bar is represented for context; use the actual Windows title bar and window behavior in implementation.

The source PDF shows ongoing orders but does not show the core item-entry or payment surfaces. Those screens and their exception states are proposed flows. The screen manifest records which source pages informed each design; the mapping is functional, not a claim that every proposed interaction already exists in the app. The small “b” marks are concept placeholders; replace them with the approved vector brand/outlet assets.

## Desktop geometry

All dimensions are effective UI pixels / Windows DIPs. Design against available client area after real OS chrome, taskbar and scaling are accounted for. Do not scale a fixed 1920-pixel canvas down as an image.

| Reference viewport | Rail | Bill width | Catalog structure | Behavior |
|---|---:|---:|---|---|
| 1920 × 1080 | 96 | 492 | 178px category column + 4 product columns | Comfortable desktop reference |
| 1366 × 768 | 80 | 404 | Horizontal category chips + 3 columns | Compact desktop reference |
| 1280 × 720 | 72 | 380 | Horizontal category chips + 3 columns | Effective-pixel check for 1080p at 150% scaling |

The provided large-screen style also defines a 2200px breakpoint with five product columns and a 520px bill. That larger breakpoint has not been visually qualified in this delivery. Below 1280 × 720 effective pixels, use a dedicated narrow-window design or an explicit minimum client size; this kit does not claim a phone layout.

The title bar is represented as 32px, outlet header as 80/72/64px, and status bar as 28px. Bill items, products, categories, settings content and modal bodies own their scrolling. The total and primary payment action stay outside the bill item scroller. A growing order must never push checkout below the window.

At short heights, compress nonessential spacing, move categories into a row, and keep fewer bill lines visible with scrolling. The full kitchen note remains in item details; compact billing hides the inline note and secondary bottom shortcuts. KOT, split and void remain available from Order details and keyboard paths. Do not hide the total, payment status or pending kitchen state.

## Component system

| Element | Reference value / rule |
|---|---|
| Canvas / surface | `#F8FAFC` / `#FFFFFF` |
| Main / secondary text | `#0F172A` / `#64748B` |
| Divider | `#E2E8F0`, 1px |
| Brand | `#F97316`; pale selection `#FFF7ED` |
| Text on orange action | Dark orange `#431407`; avoid small white text on the bright fill |
| Success | Emerald text + pale emerald surface + explicit status word |
| Pending / warning | Amber text + pale amber surface + explicit state |
| Destructive | Rose fill/text, reserved for void/refund/discard confirmations |
| Focus | 3px visible indigo outline, 3px offset in this reference |
| Body | Inter; 13–14px primary controls, 12px supporting text |
| Headings | Plus Jakarta Sans; 22–28px page/dialog titles |
| Total | 28–32px, bold, tabular numeric figures |
| Spacing | 4px base rhythm; common 8, 12, 16, 20, 24, 28, 32 |
| Radius | 10px controls, 14–16px tiles/panels, 20px dialogs |
| Primary controls | 44px default; checkout 48–50px |
| Compact controls | 32–36px secondary actions, 26–30px quantity stepper |
| Motion | Subtle 150ms state changes; honor reduced-motion preference |

This is a keyboard/mouse desktop density. For a touch-first Windows deployment, enlarge quantity steppers, compact toggles and secondary targets to at least 44px and recheck the available bill height. Do not reduce operational labels below the compact examples to fit more rows. Small 9–11px metadata in this kit is secondary; essential names, totals and primary actions remain larger.

The bundled `assets/brand-tokens.css` is the Biteaze foundation; `design.css` defines the concrete desktop adaptation. Its final rules are authoritative for the screenshots, including compact height overrides. Do not import unrelated web marketing effects into the billing view. Controls always need hover, focused, selected, disabled and error styles. Use text alongside color for status, align monetary values to the right and retain two decimal places where appropriate.

## Dialogs and drawers

Use a centered 540px dialog for a short task, 640px for customer/item detail, 860px for comparison or bill splitting, and 1040px for payment (980px at short heights). Order details use a 580px right drawer (540px on smaller widths). Maximum height follows the available window, with the heading and action footer pinned and the body scrolling.

Each dialog has one clear title, supporting bill identity, labelled fields, and one primary action. Keep Cancel/Back on the left and the primary action on the right. Destructive actions use specific names such as “Void bill” or “Discard draft.” Avoid generic “Yes” confirmations. Show the affected bill, amount, reason and approval scope before commitment.

The prototype makes the background inert, traps Tab in dialogs and supports Escape. In the Windows implementation, also restore focus to the invoking control, announce validation errors, support Narrator and high-contrast themes, and prevent nested dialogs from creating confusing focus chains. Do not close a transaction merely because the user dismisses its progress window.

## Billing and payment behavior

1. **Compose the order.** Select service mode, table/pickup/delivery context and customer. Search by name or item code; reserve scanner handling for a dedicated input path. Add variants/modifiers before committing a configured line. Preserve notes and selected options per line, not just by product ID.
2. **Send to the kitchen.** Mark unsent, sent and changed quantities explicitly. The KOT preview groups only the relevant changes by kitchen station. Decreasing or cancelling a sent item creates a correction, with reason and permissions. Track station acknowledgements independently.
3. **Adjust the bill.** Discounts display the amount, effective percentage, reason and resulting total. Discounts above the cashier limit go to a scoped manager review. Coupon replacement is explicit. Packaging, delivery, taxes and rounding have separate lines.
4. **Collect payment.** Keep bill identity and amount alongside the selected method. Cash distinguishes received amount from change; card collection requires a confirmed terminal result/reference. Credit is a customer ledger posting, not cash received. Split tender preserves each confirmed portion and shows the remaining balance.
5. **Resolve exceptions.** Pending/unknown is distinct from failed. A timeout never fabricates success or authorizes a duplicate collection. Receipt print failure leaves a successful payment successful. Kitchen failure retains the pending station and ticket identity; a customer receipt printer is never silently used as a kitchen fallback.

All tax values, credit limits, names, references and dates are sample configuration. Implement money, tax, discounts, refund allocation and rounding with the app’s approved domain rules; do not copy JavaScript demo arithmetic as a financial engine. The reference’s sample bill is subtotal ₹950 − discount ₹50 + tax ₹45 = ₹945, with ₹1,000 received and ₹55 change.

Splitting a bill by items creates separate receipts; split tender settles one receipt using multiple methods. Keep both labels distinct. When splitting by items, preserve allocated discounts/tax and make the sum of child bills equal the original payable amount. Moves and merges must identify the source and destination, including the destination’s existing balance. Unpaid, unsent drafts can be discarded; kitchen-sent orders use the void/correction path.

## Supporting workflows

- **Orders and tables:** offer a fast list plus a floor plan; table cards show occupancy, elapsed time, bill amount and status. Keep service filters consistent. A selected table opens a detail pane, with bill actions close to the order context.
- **Day close:** show denominations beside expected/actual cash reconciliation. Keep open orders and held bills visible before final closure. Carry-forward must be explicit; closure, export and messaging are separate actions.
- **Customers and credit:** maintain a profile, ledger, due balance, ageing and collection history. Keep collection allocation and receipt identity visible. Reminder sending requires a recipient/content review and the app’s consent rules.
- **Inventory:** use a dense item table with availability, prices and quick search. Group variant/modifier editing in a dedicated page instead of an oversized popup.
- **Settings:** keep a stable settings sub-navigation. Receipt, kitchen routing, tax, staff, numbering and billing tools each have a separate home. Long settings pages include continuation screenshots so lower controls remain part of the reference.
- **Printers:** separate customer receipt, default kitchen and per-station roles. Show readiness, connection and paper width before assignment. Test-print status and physical printer behavior require device verification.
- **Permissions:** show roles and limits in context. Approval authorizes the named operation and reviewed revision; it does not temporarily unlock unrestricted cashier permissions. The reference does not implement permission enforcement.
- **Messaging:** greetings and reminders offer language/template and recipient review. No automatic send is implied by saving a template, collecting money or closing the day.

## Keyboard mapping

| Action | Proposed shortcut |
|---|---|
| Search / scan items | Ctrl K |
| Start another bill (hold current first) | F2 |
| Find customer | F3 |
| Send KOT | F4 |
| Discount | F6 |
| Payment | F8 |
| Hold bill | F9 |
| Lock counter | Ctrl L |
| Close dialog | Escape |
| Shortcuts help | ? |

Enter activates the focused action; it must not trigger payment merely because an input submitted. Preserve draft state when switching screens. Windows/browser reserved-key conflicts and scanner termination behavior need native integration checks.

## Mapping to the supplied tablet document

| Tablet pages | Observed module | Desktop designs |
|---|---|---|
| 1–3 | Overview | 45 |
| 4 | Ongoing orders / tables | 3–5; proposed core billing 1–2, 65–66 |
| 5 | Item inventory | 42 |
| 6–7 | Item prices, variants, modifiers, units | 6–7, 43 |
| 8 | Reports hub | 44 |
| 9 | Sales history / returns | 31, 34–35 |
| 10–11 | Day close, cash count, cash movement | 36–37, 71 |
| 12 | Credit outstanding | 39–41 |
| 13 | Suppliers / payables | 48–49 |
| 14 | Customers | 8–9, 38–39 |
| 15–16 | Greetings / reminder templates | 50 |
| 17 | Expenses | 46–47 |
| 18–19 | Sales summaries | 44–45 |
| 20 | General settings / tax | 51, 61 |
| 21 | Order numbering | 60 |
| 22–23 | Staff, PINs, permissions | 29–30, 55–56, 64, 70 |
| 24 | Coupons | 13, 57–58 |
| 25–26 | QR menu / ordering | 59 |
| 27 | Receipt/KOT printers | 52, 68–69 |
| 28–29 | Receipt and KOT format | 53 |
| 30 | Detailed A4/A5 invoices | 54 |
| 31 | Billing tool visibility | 11–19, 62 |
| 32–33 | Business profile, subscription, devices, backup | 63 |

Source screenshots inform theme, feature groups and terminology. The design book is not a field-for-field specification for every source setting, account-deletion flow or administrative feature. Before implementation, reconcile the live Windows feature inventory with this mapping. Core payments, modifiers, line corrections, order changes, confirmations and recovery designs are explicit proposals where the source did not show their full flow.

## Research and decisions

- [Petpooja restaurant billing](https://www.petpooja.com/poss/restaurant-billing-software) describes restaurant billing, kitchen tickets, table management and keyboard/touch use. These informed the compact operator workspace and separation of bill actions from configuration.
- [Square floor plans](https://squareup.com/help/us/en/article/6427-building-your-floor-plan) describes floor sections and table management. This informed the proposed floor-plan view beside an order detail panel.
- [Lightspeed merging/splitting orders](https://o-series-support.lightspeedhq.com/hc/en-us/articles/31329418475419-Merging-or-splitting-orders) describes order splitting and merging. The reference distinguishes item-based bill splitting from multiple tender methods.
- [Microsoft responsive screen sizes](https://learn.microsoft.com/en-ca/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design) explains effective pixels and adaptive layouts. This informed the 1280 × 720 effective-pixel check in addition to the requested monitor sizes.

These are design interpretations from official sources, not copied screens or claims of feature parity. No third-party screenshots or logos are included.

## Build sequence and acceptance

Implement the shell, tokens and reusable controls first; then the billing/catalog layout; then modifiers and order tools; then payments/recovery; then supporting modules and settings. Keep domain/payment/printing logic behind the view model, with the layout bound to explicit state. Map these components to the Windows framework already in use; this HTML is a reference, not a recommendation to replace the application framework.

Accept the layout only when the bill total and checkout stay visible at the agreed effective sizes with an empty bill, a long bill, long names, multiple modifiers, error text and real translated strings. Check 100%, 125%, 150% and 200% scaling against available client dimensions on real Windows hardware. Test keyboard focus, Narrator, high contrast, scanner input and touch targets where applicable. Verify actual receipt/KOT printers, provider callbacks, offline recovery and account permissions with the application’s own integration tests.

The delivered automated checks cover browser-rendered geometry and selected demo interactions only. `layout-validation.json` records every named state at the three effective sizes; `interaction-validation.json` records exercised prototype paths. These do not establish native Windows DPI behavior, accessibility conformance, production calculation correctness or device/provider reliability.

## Screen index

| # | Screen | Source / basis |
|---:|---|---|
| 01 | [Billing workspace](index.html?screen=billing) | Proposed · core workflow |
| 02 | [Start a new bill](index.html?screen=billing-empty) | Proposed · core workflow |
| 03 | [Ongoing orders](index.html?screen=orders) | Tablet p4 |
| 04 | [Tables & floor plan](index.html?screen=tables) | Tablet p4 + proposed floor plan |
| 05 | [Held bills](index.html?screen=held) | Tablet p31 + proposed detail |
| 06 | [Item modifiers](index.html?screen=item-customize) | Tablet p6–7 + proposed ordering flow |
| 07 | [Edit an order line](index.html?screen=line-edit) | Proposed · core workflow |
| 08 | [Find / attach customer](index.html?screen=customer-select) | Tablet p14 + proposed billing flow |
| 09 | [Add customer](index.html?screen=customer-add) | Tablet p14 |
| 10 | [Assign a table](index.html?screen=table-assign) | Tablet p4 |
| 11 | [Order details & service](index.html?screen=order-details) | Tablet p31 |
| 12 | [Apply bill discount](index.html?screen=discount) | Tablet p22–23,31 |
| 13 | [Apply coupon](index.html?screen=coupon) | Tablet p24,31 |
| 14 | [Charges & tax breakdown](index.html?screen=charges) | Tablet p20,31 |
| 15 | [Order note](index.html?screen=note) | Tablet p31 |
| 16 | [Hold this bill](index.html?screen=hold) | Tablet p31 |
| 17 | [Send to kitchen](index.html?screen=kot) | Tablet p27 + proposed send flow |
| 18 | [Split a bill by items](index.html?screen=split-bill) | Proposed · optional capability |
| 19 | [Move / merge table](index.html?screen=transfer) | Proposed · optional capability |
| 20 | [Cash payment](index.html?screen=payment-cash) | Proposed · core workflow |
| 21 | [UPI payment](index.html?screen=payment-upi) | Tablet p20,25 + proposed checkout |
| 22 | [Card payment](index.html?screen=payment-card) | Proposed · core workflow |
| 23 | [Split tender](index.html?screen=payment-split) | Proposed · optional capability |
| 24 | [Credit / Udhar](index.html?screen=payment-credit) | Tablet p12,22 + proposed checkout |
| 25 | [Payment complete](index.html?screen=payment-success) | Proposed · core workflow |
| 26 | [Payment status unknown](index.html?screen=payment-pending) | Proposed · failure state |
| 27 | [Payment failed](index.html?screen=payment-failed) | Proposed · failure state |
| 28 | [Receipt print failed](index.html?screen=print-failed) | Tablet p27 + proposed failure state |
| 29 | [Void bill / cancel order](index.html?screen=void) | Tablet p9,22 |
| 30 | [Manager approval](index.html?screen=manager) | Tablet p22–23 |
| 31 | [Return / refund](index.html?screen=refund) | Tablet p9 + proposed detail |
| 32 | [Offline billing](index.html?screen=offline) | Proposed · recovery state |
| 33 | [Keyboard shortcuts](index.html?screen=shortcuts) | Proposed · desktop adaptation |
| 34 | [Sales history](index.html?screen=sales) | Tablet p9 |
| 35 | [Receipt & payment detail](index.html?screen=sale-detail) | Tablet p9 + proposed detail |
| 36 | [Day close & cash count](index.html?screen=day-close) | Tablet p10–11 |
| 37 | [Cash in / cash out](index.html?screen=cash-movement) | Tablet p10–11 |
| 38 | [Customers](index.html?screen=customers) | Tablet p14 |
| 39 | [Customer profile & ledger](index.html?screen=customer-detail) | Tablet p12,14 |
| 40 | [Credit outstanding](index.html?screen=credit) | Tablet p12 |
| 41 | [Receive credit payment](index.html?screen=credit-settle) | Tablet p12 |
| 42 | [Items & inventory](index.html?screen=inventory) | Tablet p5 |
| 43 | [Item / variant editor](index.html?screen=item-edit) | Tablet p6–7 |
| 44 | [Reports & exports](index.html?screen=reports) | Tablet p8,18–19 |
| 45 | [Business overview](index.html?screen=dashboard) | Tablet p1–3,18–19 |
| 46 | [Expense ledger](index.html?screen=expenses) | Tablet p17 |
| 47 | [Add expense](index.html?screen=expense-add) | Tablet p17 |
| 48 | [Suppliers & payables](index.html?screen=suppliers) | Tablet p13 |
| 49 | [Pay supplier](index.html?screen=supplier-payment) | Tablet p13 |
| 50 | [Greetings & reminders](index.html?screen=greetings) | Tablet p15–16 |
| 51 | [Settings home](index.html?screen=settings) | Tablet p20 |
| 52 | [Printers & kitchen routing](index.html?screen=printers) | Tablet p27 |
| 53 | [Receipt / KOT layout](index.html?screen=receipt) | Tablet p28–29 |
| 54 | [Detailed A4 / A5 invoice](index.html?screen=detailed-bill) | Tablet p30 |
| 55 | [Staff & permissions](index.html?screen=staff) | Tablet p22–23 |
| 56 | [Add staff member](index.html?screen=staff-add) | Tablet p22–23 |
| 57 | [Coupons & offers](index.html?screen=coupons) | Tablet p24 |
| 58 | [Create a coupon](index.html?screen=coupon-add) | Tablet p24 |
| 59 | [QR ordering](index.html?screen=qr) | Tablet p25–26 |
| 60 | [Order & invoice numbering](index.html?screen=order-id) | Tablet p21 |
| 61 | [Tax & rounding](index.html?screen=tax) | Tablet p20 |
| 62 | [Billing screen preferences](index.html?screen=billing-preferences) | Tablet p31 |
| 63 | [Business profile & devices](index.html?screen=profile) | Tablet p32–33 |
| 64 | [Staff lock screen](index.html?screen=lock) | Tablet p22–23 + proposed lock screen |
| 65 | [Takeaway billing](index.html?screen=billing-takeaway) | Tablet p4 + proposed ordering flow |
| 66 | [Delivery billing](index.html?screen=billing-delivery) | Tablet p4 + proposed ordering flow |
| 67 | [Delivery / pickup details](index.html?screen=delivery-details) | Proposed · core workflow |
| 68 | [Choose a printer](index.html?screen=printer-select) | Tablet p27 + proposed picker |
| 69 | [Kitchen ticket not sent](index.html?screen=kot-failed) | Proposed · recovery |
| 70 | [Approve a larger discount](index.html?screen=discount-approval) | Tablet p22–23 + proposed approval |
| 71 | [Review day closure](index.html?screen=day-close-review) | Tablet p10–11 + proposed review |
| 72 | [Discard a held draft](index.html?screen=discard-draft) | Proposed · recovery |
