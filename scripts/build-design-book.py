#!/usr/bin/env python3
"""Rebuild the original design book into artifacts/pdf without changing canonical files."""
from pathlib import Path
import sys,json,logging,html
logging.getLogger('fontTools').setLevel(logging.ERROR)
from fontTools.ttLib import TTFont as FontTool
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
ROOT=Path(__file__).resolve().parents[1]
r=ROOT/'reference/design'
artifact_dir=ROOT/'artifacts/pdf'
artifact_dir.mkdir(parents=True,exist_ok=True)
out=artifact_dir/'Biteaze-Windows-UI-Reference.pdf'
for name,file,weight in [('Inter','Inter',400),('InterB','Inter',650),('Jakarta','PlusJakartaSans',700)]:
 p=artifact_dir/(name+'.ttf')
 f=FontTool(str(r/'assets'/(file+'.ttf')))
 instantiateVariableFont(f,{'wght':weight},inplace=True).save(p)
 pdfmetrics.registerFont(TTFont(name,str(p)))
pdfmetrics.registerFontFamily('Inter',normal='Inter',bold='InterB')
screens=json.loads((r/'screen-manifest.json').read_text());cont=json.loads((r/'continuations.json').read_text())
W,H=1280,820;ink='#0F172A';muted='#64748B';orange='#F97316';line='#E2E8F0';bg='#F8FAFC'
c=canvas.Canvas(str(out),pagesize=(W,H),pageCompression=1)
c.setTitle('Biteaze for Windows — Billing UI design reference')
c.setAuthor('Biteaze · Design reference prepared with Codex')
c.setSubject('72 desktop screen states, responsive reference and implementation direction')
pages=[]
def rect(x,y,w,h,color,rad=0,stroke=None):
 c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(stroke or color));c.setLineWidth(.7)
 if rad:c.roundRect(x,y,w,h,rad,fill=1,stroke=bool(stroke))
 else:c.rect(x,y,w,h,fill=1,stroke=bool(stroke))
def text(t,x,y,size=12,font='Inter',color=ink):
 c.setFont(font,size);c.setFillColor(HexColor(color));c.drawString(x,y,t)
def para(t,x,y,w,size=13,color=muted,font='Inter',leading=None,markup=False):
 p=Paragraph(t if markup else html.escape(t),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.5,textColor=HexColor(color)))
 ww,hh=p.wrap(w,1000);p.drawOn(c,x,y-hh);return y-hh

def top(title,kicker,sub=None):
 rect(0,0,W,H,'#FFFFFF');text(kicker.upper(),40,786,10,'InterB',orange);text(title,40,748,27,'Jakarta')
 if sub:para(sub,40,726,1180,12)

def footer(label='WINDOWS DESIGN REFERENCE'):
 c.setStrokeColor(HexColor(line));c.line(40,36,1240,36)
 text('BITEAZE  /  '+label,40,20,8.5,'InterB',muted);text('29 OCT 2026',1093,20,8.5,'Inter',muted);text(f'{c.getPageNumber():03d}',1214,20,8.5,'InterB',ink)
def end(title,key=None):
 if key:c.bookmarkPage(key);c.addOutlineEntry(title,key,0,False)
 pages.append({'page':c.getPageNumber(),'title':title,'key':key});c.showPage()
def card(title,body,x,y,w=360,h=120,num=None):
 rect(x,y-h,w,h,bg,12,stroke=line)
 if num:rect(x+18,y-43,25,25,orange,7);text(str(num),x+26,y-35,11,'InterB','#431407')
 tx=x+56 if num else x+20
 text(title,tx,y-29,14,'InterB');para(body,x+20,y-49,w-40,12)
# 1 — cover
rect(0,0,W,H,bg);rect(0,H-10,W,10,orange)
rect(52,735,34,34,orange,10);text('b',63,744,21,'Jakarta','#431407');text('BITEAZE / WINDOWS',100,746,13,'InterB')
text('DESIGN REFERENCE 01',1012,746,11,'InterB',muted)
para('One clear workspace.\nEvery billing moment.',52,654,320,40,ink,'Jakarta',46)
para('A systematic desktop interface for the restaurant counter.',54,452,282,17,muted,leading=26)
for y,n,t in [(358,'72','screen states'),(298,'03','effective viewport sizes'),(238,'01','shared component language')]:
 text(n,54,y,27,'Jakarta',orange);text(t,110,y+5,12,'InterB')
rect(381,152,847,482,'#FFFFFF',12,stroke=line)
c.drawImage(str(r/'screens/01-billing.png'),389,159,width=831,height=467.4375)
para('1920 × 1080 primary  ·  1366 × 768 compact  ·  1280 × 720 scaling check',389,132,825,11)
text('Viral Patiyala sample outlet',54,106,12,'InterB');para('Source-informed redesign. Proposed screens and demo behavior are identified throughout.',54,88,300,10)
footer('BILLING + SUPPORTING WORKFLOWS');end('Start here','cover')
# 2 — layout direction
top('A stable layout for a busy counter','01 / Layout logic','The cashier always knows where to find items, the active order and the next action.')
c.drawImage(str(r/'screens/01-billing.png'),40,231,width=800,height=450)
for x,y,n in [(103,574,1),(282,519,2),(671,489,3),(767,273,4)]:
 rect(x,y,25,25,orange,7);text(str(n),x+8,y+7,10,'InterB','#431407')
card('Persistent navigation','Labelled rail and outlet/staff context. Operational modules stay in the same place.',870,680,370,120,1)
card('Fast item selection','Search, categories and text-first tiles. Prices and options are readable without product photography.',870,545,370,120,2)
card('One active bill','Service, customer, quantities and kitchen status stay together. Bill items scroll within this panel.',870,410,370,120,3)
card('Checkout stays visible','The total and payment action are anchored below the item scroller, including on smaller windows.',870,275,370,120,4)
para('A large-screen layout should use the available width intentionally. At compact sizes, categories move above the grid and spacing tightens; the checkout position remains stable.',40,185,790,16,ink,leading=25)
footer();end('Layout principles','principles')
# 3 — foundations
top('One component language','02 / Foundations','Use the bundled tokens and stylesheet as the precise visual reference.')
colors=[('Brand',orange),('Canvas',bg),('Ink',ink),('Success','#047857'),('Pending','#B45309'),('Danger','#BE123C')]
for i,(name,col) in enumerate(colors):
 x=40+i*202;rect(x,590,180,90,col,12,stroke=line if col==bg else None);text(name,x,570,12,'InterB');text(col,x,550,11,'Inter',muted)
text('Type & rhythm',40,495,21,'Jakarta');text('Billing workspace',40,451,28,'Jakarta');text('Inter for controls, content and numbers',40,420,16);text('₹945.00',40,371,34,'Jakarta');para('4px spacing rhythm · 10px control radius · 14–16px panels · 20px dialogs. Dark text on bright orange keeps the primary action legible.',40,333,505,13)
text('Desktop dimensions',650,495,21,'Jakarta')
rows=[('1920 × 1080','96px rail','492px bill','4 item columns'),('1366 × 768','80px rail','404px bill','3 item columns'),('1280 × 720','72px rail','380px bill','3 item columns')]
for i,row in enumerate(rows):
 y=446-i*58;rect(650,y-17,590,48,bg,8)
 for xx,val in zip([666,828,950,1064],row):text(val,xx,y,12,'InterB' if xx==666 else 'Inter')
para('Dialog widths: 540 / 640 / 860px. Payment: 1040px, or 980px at short heights. Right drawer: 580px, compact 540px. Headers and footers remain outside scrolling bodies.',650,253,570,13)
card('Input density','44px default actions; 48–50px checkout. Compact secondary controls need enlargement for a touch-first deployment.',40,233,505,135)
card('Status has a name','Pair color with “KOT sent”, “Pending”, “Paid” and other explicit labels. Pending payment is never rendered as success.',650,173,590,100)
footer();end('Visual foundations and dimensions','foundations')
# 4–5 — screen index
page_for={};n=7
for s in screens:
 page_for[s['id']]=n;n+=1+sum(x['screen']==s['id'] for x in cont)
for part in range(2):
 top('Screen index'+(' / continued' if part else ''),'03 / Explore the reference','Click a row to jump to its full-screen design. Screens retain their numbers in the HTML explorer and PNG names.')
 batch=screens[part*36:(part+1)*36]
 for k,s in enumerate(batch):
  col=k//18;row=k%18;x=40+col*620;y=677-row*33
  text(f"{s['number']:02d}",x,y,11,'InterB',orange);text(s['title'],x+34,y,12,'InterB');text(str(page_for[s['id']]),x+569,y,11,'Inter',muted)
  c.setStrokeColor(HexColor(line));c.line(x,y-10,x+590,y-10);c.linkRect('',s['id'],(x,y-10,x+590,y+17),relative=0,thickness=0)
 footer();end('Screen index'+(' continued' if part else ''),'index'+str(part))
# 6 — evidence / sources
top('How to use this reference','04 / Build handoff','Visual structure is ready to reference. Business and device behavior must be bound to the application’s real state.')
text('Translate the system, then bind the behavior',40,677,20,'Jakarta')
y=642
for title,body in [
 ('01  Shell and reusable controls','Build navigation, panels, fields, bill rows, totals and dialogs before individual pages.'),
 ('02  Core order and payment flows','Keep modifier state, KOT changes, discounts, split bills and split tender explicit. Preserve the active bill when navigating.'),
 ('03  Recovery and permissions','Pending, failed and successful payments have separate screens. A failed receipt print does not reverse a paid bill. Approvals stay scoped.'),
 ('04  Native acceptance','Check actual Windows scaling, keyboard focus, Narrator, scanner input, printers, offline recovery and provider callbacks.')]:
  text(title,40,y,13,'InterB');y=para(body,40,y-14,548,12)-23
text('Measured for this delivery',40,219,19,'Jakarta')
para('216 browser layout measurements: 72 states × 3 sizes. No measured horizontal overflow, off-screen dialog footer or script error. 29 representative prototype interaction checks passed.',40,187,548,13,ink)
para('No production integration, native Windows hardware, accessibility-conformance or physical printer claim is made by those checks. Full detail and the 33-page source mapping are in the implementation guide.',40,112,548,10.5)
text('Research that informed the design',670,677,20,'Jakarta')
sources=[
 ('Petpooja','Restaurant billing, KOT and operator controls.','https://www.petpooja.com/poss/restaurant-billing-software'),
 ('Square','Table and floor-plan organization.','https://squareup.com/help/us/en/article/6427-building-your-floor-plan'),
 ('Lightspeed','Splitting and merging orders.','https://o-series-support.lightspeedhq.com/hc/en-us/articles/31329418475419-Merging-or-splitting-orders'),
 ('Microsoft','Effective pixels and adaptive Windows layouts.','https://learn.microsoft.com/en-ca/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design')]
y=636
for label,desc,url in sources:
 text(label+' ↗',670,y,15,'InterB',orange);c.linkURL(url,(670,y-4,900,y+18),relative=0,thickness=0)
 y=para(desc,670,y-13,548,12)-29
rect(650,111,590,157,bg,14,stroke=line)
text('Scope and provenance',670,239,14,'InterB')
para('The supplied tablet PDF informs theme, modules and terminology. It does not show core item-entry or payment screens; these are proposals. This kit includes synthetic data and a concept “b” mark. Replace it with approved assets before shipping. The live Windows codebase was not modified.',670,219,548,12)
footer();end('Implementation, sources and evidence','handoff')
# Full screen reference pages and scroll continuations.
for s in screens:
 def screenpage(file,continued=False):
  rect(0,0,W,H,bg);text(f"{s['number']:02d} / {s['group'].upper()}",40,790,10,'InterB',orange)
  text(s['title']+(' · continued' if continued else ''),40,760,24,'Jakarta')
  text('1920 × 1080',1120,790,10,'InterB',muted)
  c.drawImage(str(r/'screens'/file),40,76,width=1200,height=675)
  note=('Scrolled content · ' if continued else '')+s['note']+'  |  '+s['source']
  para(note,40,65,1200,9,muted,leading=12)
  footer(s['group'].upper());end(s['title']+(' · continued' if continued else ''),None if continued else s['id'])
 screenpage(f"{s['number']:02d}-{s['id']}.png")
 for extra in cont:
  if extra['screen']==s['id']:screenpage(extra['file'],True)
# Responsive proof examples.
for size in ['1366x768','1280x720']:
 for id in ['billing','tables','payment-cash','item-customize','printers','day-close']:
  s=next(s for s in screens if s['id']==id);rect(0,0,W,H,bg)
  text('RESPONSIVE REFERENCE',40,790,10,'InterB',orange)
  text(s['title']+' · '+size.replace('x',' × '),40,760,24,'Jakarta')
  c.drawImage(str(r/'responsive'/(id+'-'+size+'.png')),40,76,width=1200,height=675,preserveAspectRatio=True,anchor='c')
  para('Compact layout. Content scrolls within its panel; totals and dialog actions remain available. Effective-pixel browser reference, not a native Windows DPI certification.',40,65,1200,9,muted,leading=12)
  footer('RESPONSIVE');end(s['title']+' · '+size,'responsive-'+id+'-'+size)
c.save()
(artifact_dir/'pdf-page-map.json').write_text(json.dumps(pages,indent=2))
print(json.dumps({'pdf':str(out),'pages':len(pages),'screenStates':len(screens),'continuations':len(cont),'responsiveExamples':12,'bytes':out.stat().st_size}))
