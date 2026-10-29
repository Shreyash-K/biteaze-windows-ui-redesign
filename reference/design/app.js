const modalParents={
 'printer-select':'printers','day-close-review':'day-close','discard-draft':'held','cash-movement':'day-close','credit-settle':'credit','expense-add':'expenses','supplier-payment':'suppliers','staff-add':'staff','coupon-add':'coupons','order-id':'settings','refund':'sale-detail',
 'payment-success':'billing','print-failed':'billing','manager':'billing'
};
const navFor={'billing-takeaway':'billing','billing-delivery':'billing',sales:'reports','sale-detail':'reports','day-close':'reports',held:'orders',inventory:'inventory','item-edit':'inventory',customers:'customers','customer-detail':'customers',credit:'customers',reports:'reports',dashboard:'dashboard',expenses:'reports',suppliers:'reports',greetings:'customers',tables:'tables',orders:'orders'};
const app=document.getElementById('app');
let toastTimer,discountMode='flat',digitStarted=false;
const qp=new URLSearchParams(location.search);
if(qp.has('capture'))document.body.classList.add('capture');
function notify(message){const box=document.getElementById('toast');box.textContent=message;box.classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>box.classList.remove('visible'),3800)}
function draw(){
 const id=state.screen, base=modalParents[id]||'billing';
 if(id==='billing-empty'){state.cart=[];state.discount=0}
 if(id==='discount')discountMode='flat';
 let content='',nav='billing';
 if(id==='billing'||id==='billing-empty')content=billing(id==='billing-empty');
 else if(dialogs[id]){content=pages[base]?pages[base]():billing();nav=navFor[base]||(base==='billing'?'billing':'settings')}
 else if(pages[id]){content=pages[id]();nav=navFor[id]||(id==='offline'?'billing':'settings')}
 else content=billing();
 app.innerHTML=shell(content,nav,id==='offline')+(dialogs[id]?dialogs[id]():'');
 const active=screens.find(x=>x.id===id)||screens[0];
 document.title=`${String(active.number).padStart(2,'0')} · ${active.title} | Biteaze Windows reference`;
 document.getElementById('reference-nav').innerHTML=`<strong>BITEAZE <span style="font-weight:400;color:#94a3b8">/ Windows design</span></strong><button class="nav-control" data-step="-1" aria-label="Previous design">${ic('left')}</button><select id="screen-selector" aria-label="Choose design screen">${[...new Set(screens.map(x=>x.group))].map(g=>`<optgroup label="${g}">${screens.filter(x=>x.group===g).map(s=>`<option value="${s.id}" ${s.id===id?'selected':''}>${String(s.number).padStart(2,'0')} · ${s.title}</option>`).join('')}</optgroup>`).join('')}</select><button class="nav-control" data-step="1" aria-label="Next design">${ic('chevron')}</button><span class="reference-label">${active.source} · ${active.number} / ${screens.length}</span><a href="guide.html" target="_blank">Design notes ↗</a>`;
 if(id==='billing'){const input=document.getElementById('menu-search');if(input)input.value=state.query}
 document.querySelectorAll('button').forEach(b=>{if(!b.textContent.trim()&&!b.hasAttribute('aria-label'))b.setAttribute('aria-label',b.dataset.go==='hold'?'Hold bill':b.dataset.go==='billing-preferences'?'Menu display preferences':'More options')});
 if(id==='lock')document.querySelector('.page').setAttribute('aria-hidden','true');
 if(dialogs[id]){document.querySelectorAll('.page,.sidebar,.topbar').forEach(e=>{e.setAttribute('inert','');e.setAttribute('aria-hidden','true')});setTimeout(()=>document.querySelector('.dialog input, .dialog select, .dialog button, #unlock-pin')?.focus({preventScroll:true}),0)}
 digitStarted=false;
}
function navigate(id){if(!screens.some(s=>s.id===id))return;state.screen=id;state.customQty=1;history.replaceState(null,'','#'+id);draw()}
function updateCash(){const i=document.getElementById('cash-input');if(!i)return;const cash=Number(i.value),diff=cash-totals().total;document.getElementById('cash-change').textContent=money(Math.max(0,diff));document.getElementById('complete-payment').disabled=!Number.isFinite(cash)||diff<-.001;const box=document.querySelector('.change');box.classList.toggle('insufficient',diff<0);box.querySelector('span').textContent=diff<0?'Still required':'Change to return';if(diff<0)document.getElementById('cash-change').textContent=money(-diff)}
function customTotal(){const base=document.querySelector('input[name="portion"]:checked')?.closest('.radio-card').textContent.includes('Large')?290:230;const addons=[...document.querySelectorAll('[data-addon]:checked')].reduce((n,x)=>n+Number(x.dataset.addon),0);return (base+addons)*state.customQty}
function updateCustom(){if(document.getElementById('custom-total'))document.getElementById('custom-total').textContent=money(customTotal());if(document.getElementById('custom-qty'))document.getElementById('custom-qty').textContent=state.customQty}
function countCash(){const total=[...document.querySelectorAll('[data-denom]')].reduce((n,x)=>n+Math.max(0,Number(x.value))*Number(x.dataset.denom),0)+Number(document.getElementById('coins-input')?.value||0);['counted-cash','cash-count-side'].forEach(id=>document.getElementById(id).textContent=money(total));const el=document.getElementById('cash-variance');const difference=total-10160;el.textContent=money(Math.abs(difference))+(difference===0?' · Balanced':difference>0?' · Over':' · Short');el.style.color=difference===0?'#6ee7b7':'#fbbf24'}
function discountValue(){const v=Number(document.getElementById('discount-input')?.value||0);return discountMode==='percent'?totals().sub*v/100:v}
function updateDiscount(){const d=Math.min(Math.max(0,discountValue()),totals().sub);document.getElementById('discount-total').textContent=money((totals().sub-d)*1.05);document.getElementById('discount-detail').textContent=`${money(d)} discount · ${(d/totals().sub*100).toFixed(2)}% of subtotal`}
document.addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b)return;
 if(b.dataset.go){navigate(b.dataset.go);return}
 if(b.dataset.step){const idx=screens.findIndex(s=>s.id===state.screen);navigate(screens[(idx+Number(b.dataset.step)+screens.length)%screens.length].id);return}
 if(b.dataset.demo){notify(b.dataset.demo);return}
 if(b.dataset.category){state.category=b.dataset.category;draw();return}
 if(b.dataset.service){state.service=b.dataset.service;navigate(state.service==='Takeaway'?'billing-takeaway':state.service==='Delivery'?'billing-delivery':'billing');return}
 if(b.dataset.item){if(state.screen==='billing-empty')state.cart=[];const id=Number(b.dataset.item);if(id===0){navigate('item-customize');return}const found=state.cart.find(i=>i.id===id);if(found)found.qty++;else state.cart.push({id,name:menu[id][0],price:menu[id][1],qty:1});state.screen='billing';draw();notify(`${menu[id][0]} added to the bill.`);return}
 if(b.dataset.qty){const item=state.cart.find(i=>i.id===Number(b.dataset.qty));if(item){if(Number(b.dataset.change)<0&&item.id<2){navigate('line-edit');notify('Kitchen-sent items use the correction workflow.');return}item.qty=Math.max(0,item.qty+Number(b.dataset.change));draw()}return}
 if(b.dataset.cash){document.getElementById('cash-input').value=b.dataset.cash;updateCash();return}
 if(b.dataset.digit){const input=document.getElementById('cash-input');let v=b.dataset.digit;if(!digitStarted&&v!=='⌫')input.value='';digitStarted=true;if(v==='⌫')input.value=input.value.slice(0,-1);else if(v!=='.'||!input.value.includes('.'))input.value+=v;updateCash();return}
 if(b.dataset.discountMode){discountMode=b.dataset.discountMode;b.parentElement.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b));document.querySelector('.dialog .field label').textContent=discountMode==='percent'?'Discount percentage':'Discount amount';document.getElementById('discount-input').value=discountMode==='percent'?'5':'50';updateDiscount();return}
 const a=b.dataset.action;if(!a)return;
 if(a==='toggle'){b.classList.toggle('on');b.setAttribute('aria-checked',b.classList.contains('on'));return}
 if(a==='local-tab'){b.parentElement.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b));notify('Reference selection updated. Related content is representative sample data.');return}
 if(a==='choice'||a==='select-table'){b.parentElement.querySelectorAll('button').forEach(x=>x.classList.toggle('selected',x===b));return}
 if(a==='custom-minus'){state.customQty=Math.max(1,state.customQty-1);updateCustom();return}
 if(a==='custom-plus'){state.customQty++;updateCustom();return}
 if(a==='add-custom'){const price=customTotal()/state.customQty;const existing=state.cart.find(i=>i.id===0&&i.price===price);if(existing)existing.qty+=state.customQty;else state.cart.push({id:0,name:'Chur Chur Naan Platter',price,qty:state.customQty});navigate('billing');notify('Configured item added to this sample bill.');return}
 if(a==='clear-search'){state.query='';state.category='All items';draw();return}
 if(a==='new-bill'){state.cart=[];state.query='';state.discount=0;navigate('billing-empty');return}
 if(a==='hold-bill'){navigate('held');notify('Sample bill held. Select Resume to continue the example.');return}
 if(a==='complete-payment'){const split=state.screen==='payment-split';const due=split?Math.max(0,totals().total-500):totals().total;const received=Number(document.getElementById(split?'split-cash-input':'cash-input').value);if(!Number.isFinite(received)||received<due){notify('Enter enough cash to cover the remaining balance.');return}state.payment={method:split?'UPI + Cash':'Cash',received,change:received-due};navigate('payment-success');return}
 if(a==='card-payment'){const refs=[...document.querySelectorAll('.payment-main input')];if(!refs.at(-1)?.value.trim()){notify('Enter the approved terminal reference before recording payment.');refs.at(-1)?.focus();return}state.payment={method:'Card',received:totals().total,change:0};navigate('payment-success');notify('Approved card payment recorded in the reference. No real payment was made.');return}
 if(a==='credit-payment'){navigate('customer-detail');notify('Demo: bill posted to customer credit. No money was collected.');return}
 if(a==='remove-discount'){state.discount=0;navigate('billing');return}
 if(a==='apply-discount'){const v=discountValue();if(v<0||v>totals().sub){notify('Discount must be between zero and the subtotal.');return}if(v/totals().sub>.1){state.requestedDiscount=v;state.discountReason=document.querySelector('.dialog select').value;navigate('discount-approval');return}state.discount=v;navigate('billing');notify('Bill discount updated.');return}
 if(a==='apply-coupon'){state.discount=50;navigate('billing');notify('WELCOME50 replaced the existing discount in this example.');return}
 if(a==='request-void'){if(!document.getElementById('void-reason').value){notify('Select a reason before requesting approval.');return}state.voidReason=document.getElementById('void-reason').value;navigate('manager');return}
 if(a==='approve-discount'){if(!/^\d{6}$/.test(document.querySelector('.dialog input[type="password"]').value)){notify('Enter any six digits for this visual demonstration.');return}state.discount=state.requestedDiscount??150;navigate('billing');notify('Reviewed sample discount applied. No production permission was changed.');return}
 if(a==='approve-void'){if(!/^\d{6}$/.test(document.querySelector('.dialog input[type="password"]').value)){notify('Enter six digits to demonstrate approval.');return}navigate('billing-empty');notify('Sample void approved. Production approval must be validated by the application.');return}
 if(a==='unlock'){if(!/^\d{6}$/.test(document.getElementById('unlock-pin').value)){notify('Enter any six digits for the demo.');return}navigate('billing');return}
 if(a==='close-day'){navigate('day-close-review');return}
 if(a==='check-status'){notify('No payment provider is connected. Pending remains pending; choose a result in the design explorer.');return}
 if(a==='refund-approval'){notify('Design reference: approval must identify this ₹945 refund, original receipt and selected returned items. No refund was issued.');return}
 if(a==='attach-customer'){state.customer=b.closest('.list-row').querySelector('strong').textContent;navigate('billing');notify('Customer attached to this sample bill.');return}
 const actions={
 'attach-customer':['billing','Aarav Shah selected for this demonstration.'],
 'save-customer':['billing','Customer form preview saved locally for this demonstration.'],
 'send-kot':['billing','Demo ticket prepared for the configured stations. No printer job was sent.'],
 'save-item':['inventory','Item editor preview saved. Production data is unchanged.'],
 'save-settings':[null,'Design preview saved in this session. No real configuration was changed.'],
 'test-print':[null,'Printer preview only. No physical print job was sent.'],
 'preview-pdf':[null,'The complete PDF reference is included in this design kit. No production invoice is generated.'],
 'preview-menu':[null,'Menu preview only. No live menu is published by this reference.'],
 'preview-message':[null,'Message review preview. Nothing is sent or opened in WhatsApp.'],
 'save-movement':['day-close','Demo cash movement recorded. No actual drawer balance changed.'],
 'save-collection':['credit','Demo collection preview. No money was collected.'],
 'save-expense':['expenses','Demo expense saved. Production records are unchanged.'],
 'save-supplier-payment':['suppliers','Demo supplier payment record. No money was transferred.'],
 'save-staff':['staff','Staff form preview saved. No account or PIN was created.'],
 'save-coupon':['coupons','Coupon form preview saved. No offer was published.'],
 'export':[null,'Export is represented in the design. The reference includes only synthetic sample data.']
 };
 if(actions[a]){if(actions[a][0])navigate(actions[a][0]);notify(actions[a][1])}
});
document.addEventListener('input',e=>{
 if(e.target.id==='menu-search'){const pos=e.target.selectionStart;state.query=e.target.value;draw();const input=document.getElementById('menu-search');input.focus();input.setSelectionRange(pos,pos)}
 if(e.target.id==='cash-input')updateCash();
 if(e.target.id==='discount-input')updateDiscount();
 if(e.target.id==='split-cash-input'){const diff=Number(e.target.value)-Math.max(0,totals().total-500);document.getElementById('split-change').textContent=diff<0?'Insufficient cash':money(diff);document.getElementById('complete-payment').disabled=diff<0;}
 if(e.target.matches('[data-denom],#coins-input'))countCash();
 if(e.target.id==='customer-search'){const q=e.target.value.toLowerCase();document.querySelectorAll('.selection-list .list-row').forEach(x=>x.style.display=x.textContent.toLowerCase().includes(q)?'':'none')}
});
document.addEventListener('change',e=>{
 if(e.target.id==='screen-selector'){navigate(e.target.value);return}
 if(e.target.type==='radio'){document.querySelectorAll(`input[name="${e.target.name}"]`).forEach(x=>x.closest('.radio-card')?.classList.toggle('selected',x.checked))}
 if(e.target.matches('[data-addon],input[name="portion"]'))updateCustom();
});
document.addEventListener('keydown',e=>{
 if(e.key==='Tab'&&dialogs[state.screen]){const controls=[...document.querySelectorAll('.overlay button:not([disabled]),.overlay input,.overlay select,.overlay textarea,.overlay a')].filter(x=>x.offsetParent!==null);const first=controls[0],last=controls.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus()}return}
 if(e.key==='Escape'&&dialogs[state.screen]&&state.screen!=='lock'){e.preventDefault();navigate(modalParents[state.screen]||'billing');return}
 if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();document.querySelector('.overlay input:not([type="checkbox"]),#menu-search,.toolbar input')?.focus();return}
 if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='l'){e.preventDefault();navigate('lock');return}
 if(e.target.matches('input,textarea,select'))return;
 const keys={F2:state.cart.length?'hold':'billing-empty',F3:'customer-select',F4:'kot',F6:'discount',F8:'payment-cash',F9:'hold','?':'shortcuts'};
 if(keys[e.key]){e.preventDefault();if(['F4','F6','F8','F9'].includes(e.key)&&!state.cart.some(i=>i.qty>0)){notify('Add an item to begin this bill.');return}navigate(keys[e.key])}
});
window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(screens.some(x=>x.id===id)){state.screen=id;draw()}});
window.designReference={screens,navigate,totals,state};
state.screen=qp.get('screen')||location.hash.slice(1)||'billing';
if(!screens.some(x=>x.id===state.screen))state.screen='billing';
draw();
