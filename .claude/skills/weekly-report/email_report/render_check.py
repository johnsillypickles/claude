#!/usr/bin/env python3
"""Render-check a report in Chromium: script errors, broken images, image count. Optional full-page screenshot.
Usage: python3 render_check.py report.html [screenshot.png]"""
import sys, pathlib
from playwright.sync_api import sync_playwright
path = pathlib.Path(sys.argv[1]).resolve()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_page(viewport={'width': 1280, 'height': 900})
    errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    pg.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' else None)
    pg.goto(path.as_uri(), wait_until='load')
    pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
    pg.wait_for_timeout(1500)
    n = pg.evaluate("document.querySelectorAll('img').length")
    broken = pg.evaluate("[...document.querySelectorAll('img')].filter(i=>!i.complete||i.naturalWidth===0).length")
    ph = pg.evaluate("[...document.querySelectorAll('.ph')].map(e=>e.closest('.card')?.querySelector('.nm')?.textContent)")
    rows = pg.evaluate("document.querySelectorAll('#sumtab tbody tr').length")
    cards = pg.evaluate("document.querySelectorAll('.card').length")
    pg.click('#sumtab th[data-k=rpr]'); pg.click('#sumtab th[data-k=rpr]')
    pg.select_option('#csort', 'rpr'); pg.click('#filters button:nth-child(2)'); pg.click('#filters button:nth-child(1)')
    if len(sys.argv) > 2: pg.screenshot(path=sys.argv[2], full_page=False)
    print({'errors': [e for e in errs if 'fonts.googleapis' not in e], 'font_errors_ignored': len([e for e in errs if 'fonts.googleapis' in e]),
           'images': n, 'broken': broken, 'placeholders': ph, 'table_rows': rows, 'cards': cards})
    b.close()
