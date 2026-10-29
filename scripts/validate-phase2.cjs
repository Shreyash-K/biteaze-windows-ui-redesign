/* Full denominator: every Phase 2 state, three viewports, all linked targets. */
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'..'),dir=path.join(root,'phase-2-remaining-screens');
const capture=process.argv.includes('--capture');
const out=path.join(root,'artifacts');fs.mkdirSync(out,{recursive:true});
const sizes=[[1920,1080],[1366,768],[1280,720]];
(async()=>{
 const started=Date.now(),browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH}:{})});
 let manifest,continuations=[],responsive=[],results=[],interactions=[],actionOutcomes=[];
 try{
  const discovery=await browser.newPage();
  await discovery.goto(pathToFileURL(path.join(dir,'index.html')).href+'?capture=1');
  manifest=await discovery.evaluate(()=>phase2.manifest());
  if(manifest.length<100)throw new Error('Incomplete Phase 2 denominator: expected at least100 inventoried states');
  if(new Set(manifest.map(s=>s.id)).size!==manifest.length)throw new Error('Duplicate state IDs');
  if(capture)fs.writeFileSync(path.join(dir,'screen-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
  else if(JSON.stringify(JSON.parse(fs.readFileSync(path.join(dir,'screen-manifest.json'))))!==JSON.stringify(manifest))throw new Error('Rendered manifest differs from distributed manifest');
  await discovery.close();
  const original=JSON.parse(fs.readFileSync(path.join(root,'reference/design/screen-manifest.json'))).map(s=>s.id);
  const validTargets=new Set([...original,...manifest.map(s=>s.id)]);
  const chosen=new Set(manifest.filter((s,i,a)=>i===a.findIndex(x=>x.group===s.group)).map(s=>s.id));
  ['purchase-create','quotation-create-edit','product-create-advanced','labels-batch-setup','auth-create-account','jobs-intake','food-order-compose','retail-line-configuration','payment-completion-unknown','print-outcome-reconcile'].forEach(id=>chosen.add(id));
  // Three independent viewport pages share one Chromium process; all states remain covered.
  await Promise.all(sizes.map(async(size)=>{
   const page=await browser.newPage({viewport:{width:size[0],height:size[1]}});let errors=[];
   page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push('Asset failed: '+r.url()));
   await page.goto(pathToFileURL(path.join(dir,'index.html')).href+'?capture=1');await page.evaluate(()=>document.fonts.ready);
   for(const s of manifest){
    errors=[];
    try{await page.evaluate(id=>phase2.render(id),s.id);await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(resolve)));}catch(e){errors.push(e.message);}
    const metrics=await page.evaluate(()=>{
     const rect=el=>{if(!el)return null;const r=el.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height};};
     const dialog=document.querySelector('.p-dialog'),body=document.querySelector('.p-dialog-body')||document.querySelector('.p-body');
     const controls=[...document.querySelectorAll('.p-heading-actions button,.p-dialog-footer button')].filter(x=>x.getClientRects().length);
     return {id:phase2.current,fonts:document.fonts.check('14px Inter')&&document.fonts.check('20px "Plus Jakarta Sans"'),activeRail:[...document.querySelectorAll('.p-sidebar .nav-item.active')].map(x=>({current:x.getAttribute('aria-current'),label:x.textContent.trim()})),linkedParent:document.querySelector('[data-linked-phase1]')?.dataset.linkedPhase1,linkedTitle:document.querySelector('[data-linked-phase1] h1')?.textContent,windowOverflow:document.documentElement.scrollWidth>innerWidth+1,bodyOverflow:body.scrollWidth>body.clientWidth+1,dialog:rect(dialog),footer:rect(document.querySelector('.p-dialog-footer')),controls:controls.map(rect),footerLabels:[...document.querySelectorAll('.p-dialog-footer button')].filter(x=>x.getClientRects().length).map(x=>x.textContent.trim()),body:{height:body.clientHeight,scrollHeight:body.scrollHeight},targets:[...document.querySelectorAll('[data-go],[data-submit]')].map(x=>x.dataset.go||x.dataset.submit),unlabelled:[...document.querySelectorAll('input:not([type="checkbox"]),select,textarea')].filter(x=>!x.getAttribute('aria-label')&&!x.labels?.length).map(x=>x.outerHTML.slice(0,120))};
    });
    const outside=r=>r&&(r.x<-1||r.y<-1||r.right>size[0]+1||r.bottom>size[1]+1);
    const issues=[...errors];if(metrics.id!==s.id)issues.push('Wrong state');if(!metrics.fonts)issues.push('Fonts failed');if(metrics.windowOverflow||metrics.bodyOverflow)issues.push('Horizontal overflow');if(outside(metrics.dialog)||outside(metrics.footer)||metrics.controls.some(outside))issues.push('Action/dialog outside viewport');if(metrics.unlabelled.length)issues.push('Unlabelled input');if(metrics.activeRail.length!==1||metrics.activeRail[0].current!=='page')issues.push('Main rail must have one current section');if(new Set(metrics.footerLabels).size!==metrics.footerLabels.length)issues.push('Duplicate dialog action label');
    const modal=s.kind==='dialog'||s.kind==='drawer';
    const parent=modal?manifest.find(x=>x.id===s.parent):s;
    const expectedRail=parent?({'Overview':'Overview','Documents':'Documents','Reports':'Reports','Inventory':'Inventory','Food service':'Service','Billing recovery':'Billing','Checkout':'Billing','Device & staff':'Settings'})[parent.group]||'More':({'staff':'Settings','billing':'Billing','dashboard':'Overview'})[s.parent];
    if(metrics.activeRail[0]?.label!==expectedRail)issues.push('Rail differs from workspace/parent context');
    if(modal&&original.includes(s.parent)&&metrics.linkedParent!==s.parent)issues.push('Missing linked Phase 1 parent context');
    metrics.targets.filter(t=>!validTargets.has(t)).forEach(t=>issues.push('Broken target: '+t));
    results.push({screen:s.id,size,issues,...metrics});
    const stem=String(s.number).padStart(3,'0')+'-'+s.id;
    if(capture&&size[0]===1920){
     await page.screenshot({path:path.join(dir,'screens',stem+'.png')});
     if(metrics.body.scrollHeight>metrics.body.height+12){
      let index=1,last=0;
      while(true){
       const offset=await page.evaluate(()=>{const b=document.querySelector('.p-dialog-body')||document.querySelector('.p-body');b.scrollTop=Math.min(b.scrollHeight-b.clientHeight,b.scrollTop+Math.floor(b.clientHeight*.85));return b.scrollTop;});
       if(offset<=last)break;last=offset;await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(resolve)));
       const file=stem+'-continued-'+index+'.png';await page.screenshot({path:path.join(dir,'screens',file)});continuations.push({screen:s.id,file,offset,index});index++;
       if(index>20)throw new Error('Unexpectedly unbounded screen: '+s.id);
      }
     }
    }else if(capture&&chosen.has(s.id)){
     const file=stem+'-'+size.join('x')+'.png';await page.screenshot({path:path.join(dir,'responsive',file)});responsive.push({screen:s.id,size,file});
    }
   }
   await page.close();console.log(`Phase2 measured ${manifest.length} states at ${size.join('x')}`);
  }));
  const page=await browser.newPage({viewport:{width:1366,height:768}});await page.goto(pathToFileURL(path.join(dir,'index.html')).href);
  const check=(name,pass)=>interactions.push({name,state:pass?'PASS':'FAIL'});
  await page.selectOption('#screen-picker','purchase-register');check('Explorer selects a state',await page.evaluate(()=>phase2.current)==='purchase-register');
  await page.locator('[data-go="purchase-create"]').first().click();check('Purchase flow navigation',await page.evaluate(()=>phase2.current)==='purchase-create');
  await page.goBack();await page.waitForFunction(()=>phase2.current==='purchase-register');check('Browser back restores state',await page.evaluate(()=>phase2.current)==='purchase-register');
  for(const s of manifest.filter(x=>x.kind==='dialog'||x.kind==='drawer')){
   await page.goto(pathToFileURL(path.join(dir,'index.html')).href+'?screen='+encodeURIComponent(s.id));
   await page.locator('.p-dialog').waitFor();
   check(s.id+' direct load focuses dialog',await page.evaluate(()=>document.querySelector('.p-dialog').contains(document.activeElement)));
   const buttons=page.locator('.p-dialog button:visible:not(:disabled)');await buttons.last().focus();await page.keyboard.press('Tab');
   check(s.id+' traps focus and isolates backdrop',await page.evaluate(()=>{const dialog=document.querySelector('.p-dialog');return dialog.contains(document.activeElement)&&[...document.querySelectorAll('.titlebar,.sidebar,.topbar,.page,.statusbar,#reference-nav')].every(x=>x.inert&&x.getAttribute('aria-hidden')==='true')&&[...document.querySelectorAll('button,input,select,textarea,a[href],[tabindex="0"]')].filter(x=>x.getClientRects().length&&!dialog.contains(x)).every(x=>x.closest('[inert]'));}));
   const parent=s.parent||'phase2-overview';
   await page.keyboard.press('Escape');
   if(original.includes(parent)){
    await page.waitForURL(url=>url.pathname.endsWith('/reference/design/index.html')&&url.searchParams.get('screen')===parent);
    check(s.id+' closes to Phase 1 parent',true);
    await page.goto(pathToFileURL(path.join(dir,'index.html')).href);
   }else{
    await page.waitForFunction(id=>phase2.current===id,parent);
    check(s.id+' closes to parent',await page.evaluate(()=>document.activeElement===document.querySelector('h1')));
   }
  }
  for(const id of ['supplier-new','food-table-transfer','report-private-export','exit-biteaze-confirmation']){
   const parent=manifest.find(s=>s.id===id).parent;
   await page.evaluate(id=>phase2.go(id),parent);
   const trigger=page.locator(`.p-heading-actions [data-go="${id}"],.p-body [data-go="${id}"]`).first();
   await trigger.click();await page.keyboard.press('Escape');
   const escaped=await trigger.evaluate(el=>document.activeElement===el);
   await trigger.click();await page.getByRole('button',{name:'Close dialog',exact:true}).click();
   check(id+' restores opener for Escape and close',escaped&&await trigger.evaluate(el=>document.activeElement===el));
  }
  await page.evaluate(()=>phase2.go('phase2-overview'));await page.locator('.p-tile').first().click();check('Directory tiles open module',await page.evaluate(()=>phase2.current)!=='phase2-overview');
  const searchScreen=manifest.find(s=>s.id==='purchase-register');await page.evaluate(id=>phase2.go(id),searchScreen.id);
  if(await page.locator('[data-filter]').count()){
   await page.locator('[data-filter]').first().fill('zz-no-such-record');check('Search filters records',await page.locator('tbody tr:visible').count()===0);
   await page.locator('[data-filter]').first().fill('');check('Clearing search restores records',await page.locator('tbody tr:visible').count()>0);
  }
  // A reference action must not silently substitute another document, amount or tender.
  for(const [id,label,identity] of [
   ['billing-quotation-review','Continue to checkout','QUO-2026-028'],
   ['billing-challan-review','Continue to checkout','DC-2026-019'],
   ['billing-tcs-review','Apply and recheck','₹945.90'],
   ['payment-completion-conflict','Refresh payment review','Credit']
  ]){
   await page.evaluate(id=>phase2.go(id),id);
   await page.getByRole('button',{name:label,exact:true}).click();
   check(id+' retains source authority during demo action',await page.evaluate(()=>phase2.current)===id&&(await page.locator('#toast').textContent()).includes(identity));
  }
  // Non-canonical selected records must retain identity rather than open another fixture.
  for(const [id,row,label,identity] of [
   ['purchase-register','PUR-1074','Open','PUR-1074'],
   ['inventory-catalog-browse','Butter 500 g','Edit','BTR-500'],
   ['customer-search-aging','Sample Customer A','Open','Sample Customer A'],
   ['ongoing-order-recovery','H-1040','Resume','H-1040'],
   ['print-fleet-tests','Kitchen POS-58','Edit','Kitchen POS-58'],
   ['appointments-schedule','Sample Customer D','Open','Sample Customer D'],
   ['purchase-create','Butter 500 g','Edit','BT-106'],
   ['report-catalog',null,'GST tax','GST tax'],
   ['report-error-or-catalog-mismatch',null,'Retry report','GST tax']
  ]){
   await page.evaluate(id=>phase2.go(id),id);
   const area=row?page.locator('tr,.list-row').filter({hasText:row}).first():page.locator('.p-workspace');
   await area.getByRole('button',{name:label,exact:true}).click();
   const feedback=await page.locator('#toast').textContent();
   check(id+' selected '+identity+' retains identity',await page.evaluate(()=>phase2.current)===id&&feedback.includes(identity)&&feedback.includes('not represented'));
  }
  await page.evaluate(()=>phase2.go('report-catalog'));
  await page.getByRole('link',{name:'Sales summary',exact:true}).click();
  check('Canonical report link opens its own result flow',await page.evaluate(()=>phase2.current)==='report-processing'&&(await page.locator('h1').textContent()).includes('Sales summary'));
  // Every enabled workspace/dialog action has an observable reference outcome.
  for(const s of manifest){
   await page.evaluate(id=>phase2.render(id),s.id);
   const actions=await page.evaluate(()=>{
    const area=document.querySelector('.p-dialog')||document.querySelector('.p-workspace');
    return [...area.querySelectorAll('[data-go],[data-feedback],[data-submit]')].map((b,index)=>({index,label:b.textContent.trim(),target:b.dataset.go||b.dataset.submit,enabled:!b.disabled&&!!b.getClientRects().length})).filter(b=>b.enabled&&!/^(Back|Cancel|Close|Return)\b/i.test(b.label)&&b.label);
   });
   for(const action of actions){
    const result=await page.evaluate(({id,index})=>{
     phase2.render(id);const area=document.querySelector('.p-dialog')||document.querySelector('.p-workspace');
     const button=area.querySelectorAll('[data-go],[data-feedback],[data-submit]')[index];
     const toast=document.getElementById('toast');toast.textContent='';button.click();
     return {changed:phase2.current!==id,feedback:toast.textContent.trim(),validation:!!document.activeElement?.matches(':invalid')};
    },{id:s.id,index:action.index});
    if(original.includes(action.target)){
     await page.waitForURL(url=>url.pathname.endsWith('/reference/design/index.html')&&url.searchParams.get('screen')===action.target);
     result.changed=true;await page.goto(pathToFileURL(path.join(dir,'index.html')).href);
    }
    actionOutcomes.push({screen:s.id,label:action.label,state:result.changed||result.feedback||result.validation?'PASS':'FAIL',outcome:result.changed?'navigation':result.feedback?'demo-feedback':result.validation?'validation':'none'});
   }
  }
  await page.close();
 }finally{await browser.close();}
 if(capture){fs.writeFileSync(path.join(dir,'continuations.json'),JSON.stringify(continuations.sort((a,b)=>manifest.findIndex(s=>s.id===a.screen)-manifest.findIndex(s=>s.id===b.screen)||a.index-b.index),null,2)+'\n');fs.writeFileSync(path.join(dir,'responsive.json'),JSON.stringify(responsive.sort((a,b)=>a.file.localeCompare(b.file)),null,2)+'\n');}
 const failures=results.filter(r=>r.issues.length),failedInteractions=interactions.filter(r=>r.state!=='PASS'),failedActions=actionOutcomes.filter(r=>r.state!=='PASS');
 const report={scope:'Phase2 reference only; application/native/device qualification NOT_MEASURED',state:failures.length||failedInteractions.length||failedActions.length||!actionOutcomes.length||results.length!==manifest.length*3?'FAIL':'PASS',screens:manifest.length,observations:results.length,seconds:(Date.now()-started)/1000,failures,interactions,action_outcomes:actionOutcomes,measurements:results};
 fs.writeFileSync(path.join(out,'phase2-validation.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({state:report.state,screens:report.screens,observations:report.observations,seconds:report.seconds,failures:failures.map(x=>({id:x.screen,size:x.size,issues:x.issues})),failedInteractions,actionOutcomes:actionOutcomes.length,failedActions}));
 if(report.state!=='PASS')process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
