#!/usr/bin/env python3
"""Rebuild the Phase 2 book from its editable reference's captured PNGs."""
from pathlib import Path
import json, html, logging, math
logging.getLogger('fontTools').setLevel(logging.ERROR)
from fontTools.ttLib import TTFont as FontTool
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'phase-2-remaining-screens'
OUT = ROOT / 'artifacts/phase2-pdf'
OUT.mkdir(parents=True, exist_ok=True)
for name, source, weight in [('Inter', 'Inter', 400), ('InterB', 'Inter', 650), ('Jakarta', 'PlusJakartaSans', 700)]:
    target = OUT / (name + '.ttf')
    font = FontTool(str(ROOT / 'reference/design/assets' / (source + '.ttf')))
    instantiateVariableFont(font, {'wght': weight}, inplace=True).save(target)
    pdfmetrics.registerFont(TTFont(name, str(target)))
pdfmetrics.registerFontFamily('Inter', normal='Inter', bold='InterB')
screens = json.loads((D / 'screen-manifest.json').read_text())
cont = json.loads((D / 'continuations.json').read_text())
responsive = json.loads((D / 'responsive.json').read_text())
W, H = 1280, 900
INK, MUTED, BRAND, LINE, BG = '#0F172A', '#64748B', '#F97316', '#E2E8F0', '#F8FAFC'
out = OUT / 'Biteaze-Windows-Phase-2-Reference.pdf'
c = canvas.Canvas(str(out), pagesize=(W, H), pageCompression=1)
c.setTitle('Biteaze Windows · Phase 2 · Remaining screens')
c.setAuthor('Biteaze · Desktop design reference')
c.setSubject('Source-informed remaining workflows; editable demo and Gemini implementation handoff')
pages = []

def rect(x, y, w, h, color, radius=0, stroke=None):
    c.setFillColor(HexColor(color)); c.setStrokeColor(HexColor(stroke or color)); c.setLineWidth(.7)
    if radius: c.roundRect(x, y, w, h, radius, fill=1, stroke=bool(stroke))
    else: c.rect(x, y, w, h, fill=1, stroke=bool(stroke))

def text(t, x, y, size=12, font='Inter', color=INK, max_width=None):
    if max_width:
        while pdfmetrics.stringWidth(t, font, size) > max_width: size -= .5
    c.setFillColor(HexColor(color)); c.setFont(font, size); c.drawString(x, y, t)

def para(t, x, y, w, size=12, color=MUTED, font='Inter', leading=None):
    p = Paragraph(html.escape(t).replace('\n', '<br/>'), ParagraphStyle('p', fontName=font, fontSize=size, leading=leading or size*1.45, textColor=HexColor(color)))
    _, h = p.wrap(w, 1000); p.drawOn(c, x, y-h); return y-h

def top(title, kicker, sub=''):
    rect(0, 0, W, H, BG)
    text(kicker.upper(), 40, 871, 10, 'InterB', BRAND)
    text(title, 40, 836, 27, 'Jakarta', max_width=1170)
    if sub: para(sub, 40, 812, 1170, 12)

def footer(label='PHASE 2 / IMPLEMENTATION REFERENCE'):
    c.setStrokeColor(HexColor(LINE)); c.line(40, 36, 1240, 36)
    text('BITEAZE  /  '+label, 40, 20, 8.5, 'InterB', MUTED)
    text('29 OCT 2026', 1090, 20, 8.5, color=MUTED)
    text(f'{c.getPageNumber():03d}', 1213, 20, 8.5, 'InterB')

def end(title, key=None):
    if key: c.bookmarkPage(key); c.addOutlineEntry(title, key, 0, False)
    pages.append({'page': c.getPageNumber(), 'title': title, 'key': key}); c.showPage()

def file_for(s): return f"{s['number']:03d}-{s['id']}.png"

# Cover.
rect(0, 0, W, H, BG); rect(0, H-10, W, 10, BRAND)
rect(52, 813, 38, 38, BRAND, 11); text('b', 65, 822, 23, 'Jakarta', '#431407')
text('BITEAZE / WINDOWS', 106, 826, 14, 'InterB')
text('DESIGN REFERENCE 02', 1010, 826, 11, 'InterB', MUTED)
para('The rest of\nthe workspace.\nOne clear system.', 52, 724, 330, 38, INK, 'Jakarta', 47)
para('Everyday operations, detailed forms and recovery states — ready for the next implementation pass.', 54, 536, 290, 16, leading=24)
for y, n, label in [(382, '213', 'additional screen states'), (322, '174', 'audited workflow requirements'), (262, '03', 'effective viewport sizes')]:
    text(n, 54, y, 29, 'Jakarta', BRAND); text(label, 128, y+6, 12, 'InterB')
hero = next(s for s in screens if s['id'] == 'food-service-workspace')
rect(390, 270, 840, 479, '#FFFFFF', 14, LINE)
c.drawImage(str(D/'screens'/file_for(hero)), 398, 278, width=824, height=463.5)
para('A complete directory + 213 screen states. Numbering continues from Phase 1: 73–286.', 398, 244, 820, 13, INK)
para('Purchasing · Documents · GST · Stock · Customers · Marketing\nSetup · Printing · Recovery · Staff · Services · Food · QR · Checkout', 398, 196, 820, 12)
para('Use after the current Phase 1 build is accepted. Reuse its shell and components, then bind these views to the existing Windows contracts.', 54, 139, 1168, 15, INK)
footer(); end('Start Phase 2', 'phase2-cover')

top('Continue the product. Preserve its behavior.', 'Build handoff', 'The design defines visual hierarchy. The existing Windows application remains the authority for business rules and data.')
items = [
 ('01 / Reconcile the current build', 'Read the Gemini prompt and current application source. Preserve local work. Finish and verify Phase 1 before beginning Phase 2. Compare the live source to inspected commit 7932bbbedabdd0cef4295919a91674f35fa815cf.'),
 ('02 / Reuse the component system', 'Use the same orange, slate, white, Inter and Plus Jakarta Sans system. Match page, drawer, dialog, form, table and status treatments. Copy visual intent into the existing TypeScript DOM/Electron renderer.'),
 ('03 / Work through the coverage ledger', 'Every numbered design has an editable screen body, PNG and source seam. The 174 requirement rows include fields, actions and finite admission outcomes. Shared scanner and updater requirements map to a single implementation, not duplicate modules.'),
 ('04 / Bind real states and recovery', 'Main-process totals, permissions, revisions, document identity, stock, tax and named IPC contracts remain authoritative. Unknown outcomes stay unknown until reconciled. A queued receipt is not proof of paper output.'),
 ('05 / Verify before declaring completion', 'Use screenshots at 1920×1080, 1366×768 and 1280×720 effective pixels; exercise loading, empty, denied, stale, conflict, unknown and success states. Run repository-required full checks. Mark unavailable native/hardware tests NOT_MEASURED.')]
y = 755
for title, body in items:
    text(title, 52, y, 17, 'Jakarta'); y = para(body, 52, y-17, 1130, 13, leading=20)-32
rect(40, 83, 1200, 116, '#FFFFFF', 14, LINE)
text('Reference only · synthetic records · no production actions', 60, 169, 15, 'InterB')
para('This book and demo do not implement the Windows app, contact customers, authenticate accounts, process payments or operate devices. The original tablet PDF and Phase 1 remain in the parent reference folder. Visual and source coverage are documented separately from native qualification.', 60, 147, 1150, 12)
footer(); end('How to implement Phase 2', 'phase2-handoff')

# Clickable index; there are always two front pages, then the full index.
index_count = math.ceil(len(screens)/36)
page_for = {}; page_no = 3 + index_count
for s in screens:
    page_for[s['id']] = page_no
    page_no += 1 + sum(x['screen'] == s['id'] for x in cont)
for start in range(0, len(screens), 36):
    top('Screen directory'+(' / continued' if start else ''), 'Explore', 'Select a row to jump to a full-screen design. IDs match the demo, screenshots and implementation ledger.')
    for i, s in enumerate(screens[start:start+36]):
        x = 40 + (i//18)*620; y = 760 - (i%18)*36
        text(str(s['number']), x, y, 11, 'InterB', BRAND)
        text(s['title'], x+36, y, 11.5, 'InterB', max_width=490)
        text(str(page_for[s['id']]), x+566, y, 10, color=MUTED)
        c.setStrokeColor(HexColor(LINE)); c.line(x, y-11, x+590, y-11)
        c.linkRect('', s['id'], (x, y-10, x+590, y+17), relative=0, thickness=0)
    footer('SCREEN DIRECTORY'); end('Screen directory '+str(start//36+1), 'phase2-index-'+str(start//36+1))

for s in screens:
    def screen_page(filename, continued=False):
        top(s['title']+(' · continued' if continued else ''), f"{s['number']} / {s['group']}")
        text('1920 × 1080', 1132, 871, 10, 'InterB', MUTED)
        c.drawImage(str(D/'screens'/filename), 40, 130, width=1200, height=675)
        para(('Scrolled content. ' if continued else '')+s.get('description',''), 40, 115, 1200, 10, INK, leading=14)
        para('Application seam: '+s.get('source','')+'  ·  '+s.get('basis','source-backed'), 40, 76, 1200, 9, leading=12)
        footer(s['group'].upper()); end(s['title']+(' · continued' if continued else ''), None if continued else s['id'])
    screen_page(file_for(s))
    for extra in cont:
        if extra['screen'] == s['id']: screen_page(extra['file'], True)

for r in responsive:
    s = next(s for s in screens if s['id'] == r['screen'])
    size = ' × '.join(map(str,r['size']))
    top(s['title']+' · '+size, 'Compact / scaling reference')
    c.drawImage(str(D/'responsive'/r['file']), 40, 130, width=1200, height=675, preserveAspectRatio=True, anchor='c')
    para('Content scrolls within the workspace or dialog body. Local data tables can scroll horizontally. Dialog actions remain outside the scrolling body. The browser viewport models effective pixels; native Windows DPI, Narrator and physical devices still require separate verification.', 40, 111, 1200, 10, leading=14)
    footer('RESPONSIVE'); end(s['title']+' · '+size, 'responsive-'+r['file'])
c.save()
(OUT/'pdf-page-map.json').write_text(json.dumps(pages, indent=2)+'\n')
print(json.dumps({'pdf':str(out),'pages':len(pages),'screens':len(screens),'continuations':len(cont),'responsive':len(responsive),'bytes':out.stat().st_size}))
