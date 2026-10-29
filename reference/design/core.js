/* Biteaze Windows reference. Synthetic data; no service, payment or printer integrations. */
const paths={
 search:'<circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 4.5 4.5"/>',
 grid:'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 bill:'<path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3Z"/><path d="M9 7h6M9 11h6M9 15h3"/>',
 table:'<rect x="4" y="6" width="16" height="12" rx="3"/><path d="M8 3h8M8 21h8M1 9v6M23 9v6"/>',
 orders:'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V2h6v2M9 9h6M9 13h6M9 17h3"/>',
 box:'<path d="m3 7 9-4 9 4v11l-9 4-9-4V7Zm0 0 9 4 9-4M12 11v11M7 5l10 5"/>',
 users:'<circle cx="9" cy="7" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3M16 4a3 3 0 0 1 0 6M18 14a5 5 0 0 1 3 5v2"/>',
 chart:'<path d="M4 3v18h17M8 16v-4M13 16V8M18 16V5"/>',
 settings:'<path d="m10 3-1 3-3 1-3 3 2 2-1 3 3 3 3-1 2 2 3-1 1-3 3-1v-4l-3-1-1-3-3-1-2 2Z"/><circle cx="11.5" cy="11.5" r="3"/>',
 chevron:'<path d="m9 5 7 7-7 7"/>', down:'<path d="m6 9 6 6 6-6"/>',left:'<path d="m15 5-7 7 7 7"/>', arrow:'<path d="M4 12h16m-6-6 6 6-6 6"/>',
 plus:'<path d="M12 5v14M5 12h14"/>',minus:'<path d="M5 12h14"/>',close:'<path d="m6 6 12 12M6 18 18 6"/>',check:'<path d="m5 12 4 4L19 6"/>',
 store:'<path d="M3 9 5 3h14l2 6M3 9c0 4 4 4 4 0 0 4 5 4 5 0 0 4 5 4 5 0 0 4 4 4 4 0M5 13v8h14v-8M9 21v-6h6v6"/>',
 bell:'<path d="M4 17h16l-2-4V9a6 6 0 0 0-12 0v4l-2 4ZM10 21h4"/>',
 clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 sun:'<circle cx="12" cy="12" r="4"/><path d="M12 1v2M12 21v2M1 12h2M21 12h2M4 4l2 2M18 18l2 2M4 20l2-2M18 6l2-2"/>',
 star:'<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3Z"/>',
 leaf:'<path d="M20 3C7 2 3 8 5 15c6 5 15 1 15-12ZM4 21 15 9"/>',
 flame:'<path d="M13 2c3 7 7 7 7 13a8 8 0 0 1-16 0c0-4 2-7 5-9 0 4 2 5 3 5 2-3 2-6 1-9Z"/>',
 bowl:'<path d="M3 11h18a9 9 0 0 1-18 0ZM8 22h8M7 3v4M12 2v5M17 3v4"/>',
 bread:'<path d="M5 11C0 9 3 3 7 4a8 8 0 0 1 10 0c4-1 7 5 2 7v10H5V11Z"/>',
 cup:'<path d="M4 8h12v9a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4V8ZM16 9h2a3 3 0 0 1 0 6h-2M7 2v3M12 2v3"/>',
 sweet:'<path d="M5 11h14l-2 10H7L5 11ZM5 11c-4-5 3-8 7-8s11 3 7 8M12 3V1"/>',
 bag:'<path d="M5 7h14l2 14H3L5 7ZM8 7V5a4 4 0 0 1 8 0v2"/>',
 truck:'<path d="M2 5h13v12H2V5ZM15 9h4l3 4v4h-7"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/>',
 user:'<circle cx="12" cy="7" r="4"/><path d="M4 22v-3a8 8 0 0 1 16 0v3"/>',
 more:'<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>',
 note:'<path d="M5 3h14v18H5V3ZM8 7h8M8 11h8M8 15h5"/>',
 tag:'<path d="M3 3h8l10 10-8 8L3 11V3Z"/><circle cx="7.5" cy="7.5" r="1"/>',
 percent:'<circle cx="7" cy="7" r="3"/><circle cx="17" cy="17" r="3"/><path d="m5 19 14-14"/>',
 pause:'<path d="M8 4v16M16 4v16"/>',
 print:'<path d="M7 8V3h10v5M7 17H3V9h18v8h-4M7 14h10v7H7v-7M17 11h1"/>',
 wifi:'<path d="M2 8a16 16 0 0 1 20 0M5 12a11 11 0 0 1 14 0M8 16a6 6 0 0 1 8 0"/><circle cx="12" cy="20" r=".5"/>',
 offline:'<path d="m3 3 18 18M2 8a15 15 0 0 1 3-2m4-2a16 16 0 0 1 13 4M5 12a11 11 0 0 1 4-2m6 0a11 11 0 0 1 4 2M8 16a6 6 0 0 1 8 0M12 20h.01"/>',
 keyboard:'<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M6 9h.1M10 9h.1M14 9h.1M18 9h.1M6 12h.1M10 12h.1M14 12h.1M18 12h.1M7 16h10"/>',
 filter:'<path d="M4 6h16M7 12h10M10 18h4"/>',
 cash:'<rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M5 9v6M19 9v6"/>',
 card:'<rect x="2" y="4" width="20" height="16" rx="3"/><path d="M2 9h20M6 15h4"/>',
 qr:'<path d="M3 3h6v6H3V3ZM15 3h6v6h-6V3ZM3 15h6v6H3v-6ZM15 15h2v2h-2v-2ZM19 15h2v6h-6v-2M3 12h5M12 3v5M12 12h5M12 16v5"/>',
 split:'<path d="M12 21V11M12 11l-7-7M12 11l7-7M3 9V3h6M15 3h6v6"/>',
 wallet:'<path d="M20 8V5H5a3 3 0 0 0 0 6h16v10H5a3 3 0 0 1-3-3V8M21 13h-6v5h6M17 15.5h.01"/>',
 shield:'<path d="M12 2 3 6v7c0 5 9 9 9 9s9-4 9-9V6l-9-4Z"/><path d="m8 12 3 3 5-6"/>',
 lock:'<rect x="5" y="10" width="14" height="12" rx="2"/><path d="M8 10V6a4 4 0 0 1 8 0v4M12 15v3"/>',
 undo:'<path d="M3 4v6h6M3 10a9 9 0 1 1 1 8"/>',
 trash:'<path d="M3 6h18M9 6V3h6v3M6 6l1 15h10l1-15M10 10v7M14 10v7"/>',
 info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>',
 warning:'<path d="M12 3 1 21h22L12 3ZM12 9v5M12 17h.01"/>',
 refresh:'<path d="M20 4v6h-6M20 10a8 8 0 0 0-14-5M4 20v-6h6M4 14a8 8 0 0 0 14 5"/>',
 download:'<path d="M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4"/>',
 calendar:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 2v6M17 2v6M3 11h18M7 15h3M14 15h3"/>',
 edit:'<path d="m16 3 5 5-13 13H3v-5L16 3ZM13 6l5 5"/>',
 send:'<path d="m2 3 20 9-20 9 4-9-4-9ZM6 12h16"/>',
 phone:'<path d="m6 3 4 5-3 3c2 3 3 4 6 6l3-3 5 4c-1 7-8 3-12-1S1 4 6 3Z"/>',
 link:'<path d="m10 14 4-4M7 16l-2 2a4 4 0 0 1-6-6l5-5a4 4 0 0 1 6 0M17 8l2-2a4 4 0 0 1 6 6l-5 5a4 4 0 0 1-6 0" transform="translate(2 -1) scale(.83)"/>',
 cloud:'<path d="M6 19a5 5 0 1 1 0-10 7 7 0 0 1 14-1 5.5 5.5 0 0 1-1 11H6Z"/>',
 monitor:'<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M12 17v4M7 21h10"/>',
 logout:'<path d="M9 3H3v18h6M12 12h10m-5-5 5 5-5 5"/>',
 help:'<circle cx="12" cy="12" r="9"/><path d="M9 8a3 3 0 1 1 5 3c-2 1-2 1-2 3M12 17h.01"/>',
 fork:'<path d="M5 3v7a3 3 0 0 0 6 0V3M8 3v18M19 3c-4 5-4 9 0 9v9M19 3v9"/>'
};
const ic=(n)=>`<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${paths[n]||paths.grid}</svg>`;
const esc=(v)=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=(v)=>'₹'+Number(v).toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});
const rupee=(v)=>'₹'+Number(v).toLocaleString('en-IN');
const badge=(t,c='')=>`<span class="badge ${c}">${t}</span>`;
const btn=(t,go='',type='',icon='')=>`<button class="btn ${type}" ${go?`data-go="${go}"`:'data-demo="Design preview: this action would open the connected workflow."'}>${icon?ic(icon):''}${t}</button>`;
const act=(t,a,type='',icon='',extra='')=>`<button class="btn ${type}" data-action="${a}" ${extra}>${icon?ic(icon):''}${t}</button>`;
const ib=(icon,go,label)=>`<button class="icon-btn" data-go="${go}" aria-label="${label}" title="${label}">${ic(icon)}</button>`;
const notice=(t,type='')=>`<div class="notice ${type}">${ic(type==='red'||type==='amber'?'warning':type==='green'?'check':'info')}<div>${t}</div></div>`;
const field=(label,value='',type='text',help='',attrs='')=>`<div class="field"><label>${label}</label><input type="${type}" value="${esc(value)}" ${attrs}>${help?`<div class="help">${help}</div>`:''}</div>`;
const select=(label,options,help='')=>`<div class="field"><label>${label}</label><select aria-label="${esc(label)}">${options.map(o=>`<option>${o}</option>`).join('')}</select>${help?`<div class="help">${help}</div>`:''}</div>`;
const check=(label,on=true)=>`<label class="check"><input type="checkbox" ${on?'checked':''}>${label}</label>`;
const toggle=(on=true,label='Change setting')=>`<button class="switch ${on?'on':''}" data-action="toggle" role="switch" aria-checked="${on}" aria-label="${label}"></button>`;
const row=(title,desc,right='')=>`<div class="list-row"><div><strong>${title}</strong>${desc?`<p>${desc}</p>`:''}</div>${right}</div>`;
const stat=(label,value,foot='',icon='')=>`<div class="stat"><div class="label">${icon?ic(icon):''}${label}</div><div class="value">${value}</div><div class="foot">${foot}</div></div>`;
const panel=(title,sub,content,action='')=>`<section class="panel"><div class="panel-head"><div><h3>${title}</h3>${sub?`<p>${sub}</p>`:''}</div>${action}</div><div class="panel-body">${content}</div></section>`;
const heading=(title,sub,actions='')=>`<div class="page-heading"><div><h1>${title}</h1><p>${sub}</p></div><div class="flex gap8">${actions}</div></div>`;
const search=(placeholder,id='')=>`<label class="search">${ic('search')}<input ${id?`id="${id}"`:''} aria-label="${placeholder}" placeholder="${placeholder}"><kbd>Ctrl K</kbd></label>`;
const tabs=(items,active=0)=>`<div class="tabs">${items.map((t,i)=>`<button class="${i===active?'active':''}" data-action="local-tab">${t}</button>`).join('')}</div>`;
const table=(headers,rows,foot='Showing all results')=>`<div class="panel"><div class="table-wrap"><table class="data-table"><thead><tr>${headers.map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div><div class="table-footer"><span>${foot}</span><span>29 October 2026 · Sample data</span></div></div>`;
const summaryRows=()=>`<div class="sum-row"><span>Subtotal · ${state.cart.reduce((n,i)=>n+i.qty,0)} items</span><span>${money(totals().sub)}</span></div><div class="sum-row discount"><button data-go="discount">Discount</button><span>− ${money(totals().discount)}</span></div><div class="sum-row"><button data-go="charges">CGST + SGST <span class="muted">5%</span></button><span>${money(totals().tax)}</span></div>`;
const menu=[
 ['Chur Chur Naan Platter',230,'Bestsellers','P01','2 variants',2],['Paneer Tikka',280,'Starters','S01','3 add-ons',1],['Aloo Pyaaz Paratha',110,'Parathas','P04','2 variants',1],['Masala Chaas',50,'Beverages','B02','Regular',2],
 ['Amritsari Kulcha',190,'Bestsellers','P02','2 variants',0],['Dal Makhani',220,'Main course','M01','Full portion',0],['Paneer Butter Masala',260,'Main course','M02','2 variants',0],['Veg Hakka Noodles',180,'Chinese','C01','Full portion',0],
 ['Tandoori Roti',30,'Breads','R01','Plain / Butter',0],['Jeera Rice',140,'Rice & biryani','R05','Full portion',0],['Sweet Lassi',90,'Beverages','B01','Regular',0],['Gulab Jamun',80,'Desserts','D01','2 pieces',0],
 ['Achari Paneer Tikka',290,'Starters','S03','3 add-ons',0],['Veg Dum Biryani',230,'Rice & biryani','R07','Full portion',0],['Butter Naan',55,'Breads','R03','Regular',0],['Malai Chaap',250,'Starters','S04','Unavailable',0]
];
const state={screen:'billing',category:'All items',query:'',cart:menu.slice(0,4).map((m,i)=>({name:m[0],price:m[1],qty:m[5],id:i})),service:'Dine-in',discount:50,customQty:1,customer:'Walk-in customer',voidReason:'Customer cancelled',payment:{method:'Cash',received:1000,change:55}};
const totals=()=>{const sub=state.cart.reduce((n,i)=>n+i.price*i.qty,0);const discount=Math.min(state.discount,sub);const tax=(sub-discount)*.05;return {sub,discount,tax,total:sub-discount+tax}};
const screens=[
 ['billing','Billing workspace','Billing','Proposed · core workflow','Persistent order, clear category navigation and a fixed payment action.'],
 ['billing-empty','Start a new bill','Billing','Proposed · core workflow','Empty state explains the next action without hiding menu selection.'],
 ['orders','Ongoing orders','Orders','Tablet p4','Queue states use text labels, elapsed time and direct resume actions.'],
 ['tables','Tables & floor plan','Orders','Tablet p4 + proposed floor plan','Table occupancy, amount and service state stay visible together.'],
 ['held','Held bills','Orders','Tablet p31 + proposed detail','Parked bills have a named owner and can be resumed or discarded explicitly.'],
 ['item-customize','Item modifiers','Bill tools','Tablet p6–7 + proposed ordering flow','Required choices precede optional add-ons. Price changes remain visible.'],
 ['line-edit','Edit an order line','Bill tools','Proposed · core workflow','Edit quantity and notes; kitchen-sent items require a separate correction.'],
 ['customer-select','Find / attach customer','Bill tools','Tablet p14 + proposed billing flow','Search by name or phone; adding a customer is secondary.'],
 ['customer-add','Add customer','Bill tools','Tablet p14','Only the essential fields lead; consent is explicit and unchecked.'],
 ['table-assign','Assign a table','Bill tools','Tablet p4','Available and occupied tables are visibly different.'],
 ['order-details','Order details & service','Bill tools','Tablet p31','Service mode, staff, price mode and order details are one coherent panel.'],
 ['discount','Apply bill discount','Bill tools','Tablet p22–23,31','Scope, amount and effective discount are visible before applying.'],
 ['coupon','Apply coupon','Bill tools','Tablet p24,31','Eligibility and reason for unavailable offers are explicit.'],
 ['charges','Charges & tax breakdown','Bill tools','Tablet p20,31','Show configured tax and charges without silent recalculation.'],
 ['note','Order note','Bill tools','Tablet p31','Receipt notes and kitchen instructions have distinct visibility.'],
 ['hold','Hold this bill','Bill tools','Tablet p31','A meaningful label makes the parked bill easy to retrieve.'],
 ['kot','Send to kitchen','Kitchen','Tablet p27 + proposed send flow','New items route to named stations; existing kitchen tickets are not resent.'],
 ['split-bill','Split a bill by items','Bill tools','Proposed · optional capability','Item splitting creates separate bills; it is distinct from multiple tenders.'],
 ['transfer','Move / merge table','Bill tools','Proposed · optional capability','Preview destination and source before moving or combining orders.'],
 ['payment-cash','Cash payment','Payments','Proposed · core workflow','Cash tender, quick amounts and change are readable at a glance.'],
 ['payment-upi','UPI payment','Payments','Tablet p20,25 + proposed checkout','Reference is deliberately non-payable; live status must come from the provider.'],
 ['payment-card','Card payment','Payments','Proposed · core workflow','Do not collect card data in the POS; use the configured terminal.'],
 ['payment-split','Split tender','Payments','Proposed · optional capability','Each tender has its own amount and status; balance remains visible.'],
 ['payment-credit','Credit / Udhar','Payments','Tablet p12,22 + proposed checkout','Require a customer and show limit, outstanding balance and due date.'],
 ['payment-success','Payment complete','Payments','Proposed · core workflow','Payment success and receipt delivery are separate statuses.'],
 ['payment-pending','Payment status unknown','Recovery','Proposed · failure state','Keep the bill locked while checking; prevent an accidental second charge.'],
 ['payment-failed','Payment failed','Recovery','Proposed · failure state','Only a confirmed failure exposes retry or an alternative method.'],
 ['print-failed','Receipt print failed','Recovery','Tablet p27 + proposed failure state','A print failure never changes the successful payment state.'],
 ['void','Void bill / cancel order','Recovery','Tablet p9,22','Show affected bill, kitchen state, mandatory reason and approval requirement.'],
 ['manager','Manager approval','Recovery','Tablet p22–23','Approval names the exact action and does not elevate the entire session.'],
 ['refund','Return / refund','Recovery','Tablet p9 + proposed detail','Select original items, reason and refund route; preserve receipt history.'],
 ['offline','Offline billing','Recovery','Proposed · recovery state','Separate local availability, sync queue and unavailable online methods.'],
 ['shortcuts','Keyboard shortcuts','Desktop','Proposed · desktop adaptation','Explicit shortcuts, focus handling and no global Enter-to-pay.'],
 ['sales','Sales history','Records','Tablet p9','Compact filterable ledger with a clear detail action per receipt.'],
 ['sale-detail','Receipt & payment detail','Records','Tablet p9 + proposed detail','Keep tender, receipt, refunds and activity tied to one transaction.'],
 ['day-close','Day close & cash count','Cash operations','Tablet p10–11','Counted cash, expected cash and variance are separate; closure is explicit.'],
 ['cash-movement','Cash in / cash out','Cash operations','Tablet p10–11','Record a reason and tender movement without mixing it with sales.'],
 ['customers','Customers','People','Tablet p14','Readable customer ledger, outstanding balance and direct context.'],
 ['customer-detail','Customer profile & ledger','People','Tablet p12,14','Balance and recent transactions sit together; consent is visible.'],
 ['credit','Credit outstanding','People','Tablet p12','Aging and due dates guide collection; reminders remain explicit.'],
 ['credit-settle','Receive credit payment','People','Tablet p12','Allocate received money to an identified outstanding balance.'],
 ['inventory','Items & inventory','Catalog','Tablet p5','Stock, availability and price are scannable; changes open an editor.'],
 ['item-edit','Item / variant editor','Catalog','Tablet p6–7','Organize price, inventory, modifiers and kitchen routing into groups.'],
 ['reports','Reports & exports','Management','Tablet p8,18–19','Separate report selection from the detailed operational billing view.'],
 ['dashboard','Business overview','Management','Tablet p1–3,18–19','A restrained summary with operational links; no dashboard clutter in billing.'],
 ['expenses','Expense ledger','Management','Tablet p17','Date, category, payment method and status form a compact ledger.'],
 ['expense-add','Add expense','Management','Tablet p17','Required amount, category and method; optional supporting detail.'],
 ['suppliers','Suppliers & payables','Management','Tablet p13','Outstanding amount and due status anchor the supplier ledger.'],
 ['supplier-payment','Pay supplier','Management','Tablet p13','Record payment against invoices and show the remaining payable.'],
 ['greetings','Greetings & reminders','Management','Tablet p15–16','Preview recipient, template and consent before each manual send.'],
 ['settings','Settings home','Settings','Tablet p20','Group billing, printing, people and store configuration.'],
 ['printers','Printers & kitchen routing','Settings','Tablet p27','Receipt, default KOT and station printers are separate assignments.'],
 ['receipt','Receipt / KOT layout','Settings','Tablet p28–29','Live sample preview and explicit paper size beside grouped toggles.'],
 ['detailed-bill','Detailed A4 / A5 invoice','Settings','Tablet p30','Keep detailed invoice choices distinct from thermal receipt settings.'],
 ['staff','Staff & permissions','Settings','Tablet p22–23','Role, status and privileges; discount and void limits stay visible.'],
 ['staff-add','Add staff member','Settings','Tablet p22–23','Role-scoped permissions and PIN setup in one bounded form.'],
 ['coupons','Coupons & offers','Settings','Tablet p24','Show offer value, validity and eligibility with distinct statuses.'],
 ['coupon-add','Create a coupon','Settings','Tablet p24','Name, type, validity and limits; preview the customer-facing offer.'],
 ['qr','QR ordering','Settings','Tablet p25–26','Payment timing and menu publication are separate configuration steps.'],
 ['order-id','Order & invoice numbering','Settings','Tablet p21','Preview the next number and explain reset cadence.'],
 ['tax','Tax & rounding','Settings','Tablet p20','Configuration reference only; rates require business validation.'],
 ['billing-preferences','Billing screen preferences','Settings','Tablet p31','One clean list of tools with role-specific visibility guidance.'],
 ['profile','Business profile & devices','Settings','Tablet p32–33','Account, plan, connected devices and data actions are clearly grouped.'],
 ['lock','Staff lock screen','Desktop','Tablet p22–23 + proposed lock screen','Lock hides transaction details and preserves the active bill.']
].map((s,i)=>({id:s[0],title:s[1],group:s[2],source:s[3],note:s[4],number:i+1}));

function shell(content,active='billing',offline=false){
 const navs=[['grid','Overview','dashboard'],['bill','Billing','billing'],['table','Tables','tables'],['orders','Orders','orders'],['box','Items','inventory'],['users','Customers','customers'],['chart','Reports','reports']];
 return `<div class="titlebar"><div class="flex gap8"><span class="mini-mark">b</span> Biteaze for Windows <span class="muted">/</span> Viral Patiyala <span class="muted">· Design reference</span></div><div class="window-controls" aria-hidden="true"><span>−</span><span>□</span><span>×</span></div></div>
 <nav class="sidebar" aria-label="Main navigation"><button class="brand-mark" data-go="billing" aria-label="Biteaze home">b</button>${navs.map(n=>`<button class="nav-item ${active===n[2]?'active':''}" data-go="${n[2]}">${ic(n[0])}<span>${n[1]}</span></button>`).join('')}<div class="rail-bottom"><button class="nav-item ${active==='settings'?'active':''}" data-go="settings">${ic('settings')}<span>Settings</span></button><button class="nav-item" data-go="lock">${ic('lock')}<span>Lock</span></button></div></nav>
 <header class="topbar"><button class="merchant" data-go="profile"><span class="merchant-icon">${ic('store')}</span><div style="text-align:left"><h3>Viral Patiyala</h3><p>Main outlet <span style="padding:0 6px">/</span> Counter 01</p></div>${ic('down')}</button><div class="top-actions"><span class="badge ${offline?'amber':'green'}"><i class="dot"></i>${offline?'Offline mode':'Synced'}</span><span class="small muted shift-label">${ic('sun').replace('class="icon"','class="icon" style="width:14px;height:14px;vertical-align:-3px;margin-right:5px"')} Morning shift · Open</span>${btn('Day close','day-close','small','clock')}<span class="top-rule"></span>${ib('keyboard','shortcuts','Keyboard shortcuts')}<button class="cashier" data-go="staff"><span class="avatar">SK</span><span style="text-align:left"><strong>Simran Kaur</strong><small>Cashier</small></span>${ic('down')}</button></div></header>
 <main class="page">${content}</main><footer class="statusbar"><div class="flex"><span class="state ${offline?'text-brand':'text-green'}"><i class="dot"></i>${offline?'Offline · 3 bills waiting to sync':'All changes saved'}</span><button class="state" data-go="printers">${ic('print')} Receipt printer ready</button><span>Business date: 29 Oct 2026</span></div><div class="flex"><span>Local sample data</span><button data-go="shortcuts">${ic('keyboard')} Keyboard shortcuts <kbd>?</kbd></button><span>12:42 PM</span></div></footer>`;
}
function billPanel(empty=false){
 return `<aside class="bill-panel"><div class="bill-head"><div class="between"><div><h2>${empty?'New bill':'Current bill'}</h2><div class="bill-id">${empty?'Ready for your next order':'#VP-1042'} ${empty?'':badge('Open','orange')} <span>${empty?'':'· 12:34 PM'}</span></div></div><div class="bill-actions">${ib('more','order-details','Bill details and actions')}</div></div><div class="service-switch">${[['table','Dine-in'],['bag','Takeaway'],['truck','Delivery']].map(([i,t])=>`<button class="${state.service===t?'active':''}" data-service="${t}">${ic(i)}${t}</button>`).join('')}</div></div>
 <div class="table-customer">${state.service==='Dine-in'?btn(empty?'Assign table':'T04 · 2 guests','table-assign','','table'):btn(state.service==='Delivery'?'Delivery · DEL-028':'Pickup · TK-028','delivery-details','',state.service==='Delivery'?'truck':'bag')}${btn(empty?'Add customer':state.customer,'customer-select','','user')}</div>
 <div class="bill-column-labels"><span>Item / quantity</span><span>Amount</span></div>
 ${empty?`<div class="empty-bill"><div class="empty-icon">${ic('bill')}</div><h3>Let’s start an order</h3><p>Select an item from the menu or scan a barcode to add it here.</p><span class="muted small">Search the menu with <kbd>Ctrl K</kbd></span></div>`:`<div class="bill-items">${state.cart.filter(i=>i.qty>0).map((i,n)=>`<div class="bill-line"><div class="bill-line-title"><span class="veg"></span><button data-go="line-edit">${i.name}</button><span class="amount">${money(i.price*i.qty)}</span></div><div class="line-bottom"><span class="line-meta">${rupee(i.price)}${n===0?' · Regular':' each'}</span><div class="qty"><button data-qty="${i.id}" data-change="-1" aria-label="Decrease ${i.name}">−</button><span>${i.qty}</span><button data-qty="${i.id}" data-change="1" aria-label="Increase ${i.name}">+</button></div>${n<2?badge('KOT sent','green'):badge('Not sent','amber')}</div>${n===0?`<div class="bill-note">${ic('note')}Less spicy · no onion garnish</div>`:''}</div>`).join('')}</div><div class="bill-utilities">${btn('Discount','discount','','percent')}${btn('Coupon','coupon','','tag')}${btn('Note','note','','note')}</div>`}
 <div class="bill-summary">${empty?'<div class="sum-row"><span>0 items</span><span>₹0.00</span></div>':summaryRows()}<div class="sum-total"><span>Total payable</span><strong>${empty?'₹0.00':money(totals().total)}</strong></div><div class="checkout">${empty?'<button class="btn wide" disabled>Add items to continue</button>':`${btn('','hold','hold','pause')}${btn(`<span>Pay ${money(totals().total)}</span><span><kbd>F8</kbd>${ic('arrow')}</span>`,'payment-cash','primary')}`}</div>${!empty?`<div class="bill-subfooter"><button data-go="kot">Send to kitchen <kbd>F4</kbd></button><button data-go="split-bill">Split bill</button><button data-go="void">Void</button></div>`:''}</div></aside>`;
}
function billing(empty=false,offline=false){
 const categories=[['grid','All items','64'],['star','Bestsellers','12'],['flame','Starters','10'],['bread','Parathas','8'],['bowl','Main course','12'],['bread','Breads','6'],['bowl','Rice & biryani','5'],['fork','Chinese','4'],['cup','Beverages','5'],['sweet','Desserts','2']];
 let shown=menu.filter(m=>(state.category==='All items'||m[2]===state.category)&&(m[0].toLowerCase().includes(state.query.toLowerCase())||m[3].toLowerCase().includes(state.query.toLowerCase())));
 return `<div style="height:100%;display:flex;flex-direction:column">${offline?`<div class="offline-strip"><span class="flex gap8">${ic('offline')} You’re offline. Cash billing is available; 3 saved bills are waiting to sync.</span>${btn('View sync queue','offline','small quiet')}</div>`:''}<div class="billing" style="min-height:0;flex:1"><section class="catalog"><div class="catalog-header"><div><h1>Billing</h1><p>Good service starts with a smooth order.</p></div><div class="header-tabs"><button class="active" data-go="billing">New bill</button><button data-go="orders">Ongoing <span class="count">08</span></button><button data-go="held">Held <span class="count">03</span></button></div></div><div class="search-row">${search('Search items, code or scan barcode','menu-search')}${btn('','billing-preferences','','filter')}</div><div class="catalog-body"><nav class="categories" aria-label="Menu categories"><div class="eyebrow">Menu categories</div>${categories.map(([i,t,c])=>`<button class="category ${state.category===t?'active':''}" data-category="${t}">${ic(i)}<span>${t}</span><span>${c}</span></button>`).join('')}</nav><div class="products-area"><div class="products-label"><strong>${state.category}</strong><span>${shown.length} featured items <span style="padding:0 7px">·</span> Retail prices</span></div><div class="product-grid">${shown.map((m)=>{const idx=menu.indexOf(m);const q=empty?0:(state.cart.find(i=>i.id===idx)?.qty||0);return `<button class="product ${q?'selected':''} ${idx===15?'unavailable':''}" ${idx===15?'data-demo="Malai Chaap is unavailable. Update availability in Items."':`data-item="${idx}"`}><div class="product-top"><span class="veg"></span><span class="product-code">${m[3]}</span></div><span class="product-name">${m[0]}</span><div class="product-bottom"><div><div class="product-price">${rupee(m[1])}</div><div class="product-options">${m[4]}</div></div><span class="plus">${q||'+'}</span></div></button>`}).join('')}</div>${!shown.length?`<div class="empty-bill"><h3>No matching items</h3><p>Try a different name or item code.</p>${act('Clear search','clear-search','soft')}</div>`:''}</div></div><div class="catalog-hint">${ic('keyboard')} <span><kbd>Ctrl K</kbd> Search items <span style="padding:0 10px">·</span> <kbd>F2</kbd> New bill <span style="padding:0 10px">·</span> <kbd>F4</kbd> Send KOT <span style="padding:0 10px">·</span> <kbd>F8</kbd> Payment</span></div></section>${billPanel(empty)}</div></div>`;
}
function receipt(detailed=false){return `<div class="paper ${detailed?'a4-paper':''}"><div class="mini-logo">b</div><h3>Viral Patiyala</h3><div class="receipt-center">Main outlet · Sample receipt<br>Tax configuration: illustrative<br>29 Oct 2026 · 12:42 PM</div><hr><div class="receipt-line"><span>Invoice #VP-1042</span><span>Table T04</span></div><div class="receipt-line"><span>Cashier: Simran</span><span>2 guests</span></div><hr>${state.cart.map(i=>`<div class="receipt-line"><span>${i.qty} × ${i.name}</span><span>${money(i.qty*i.price)}</span></div>`).join('')}<hr><div class="receipt-line"><span>Subtotal</span><span>${money(totals().sub)}</span></div><div class="receipt-line"><span>Discount</span><span>−${money(totals().discount)}</span></div><div class="receipt-line"><span>CGST 2.5%</span><span>${money(totals().tax/2)}</span></div><div class="receipt-line"><span>SGST 2.5%</span><span>${money(totals().tax/2)}</span></div><hr><div class="receipt-line receipt-total"><span>TOTAL</span><span>${money(totals().total)}</span></div><div class="receipt-line"><span>Paid via cash</span><span>${money(totals().total)}</span></div><hr><p class="receipt-center">Thank you for dining with us.<br>See you again at Viral Patiyala!</p>${detailed?'<div style="margin-top:80px;border-top:1px solid #e2e8f0;padding-top:12px;text-align:right">Authorised signatory</div>':''}</div>`}
