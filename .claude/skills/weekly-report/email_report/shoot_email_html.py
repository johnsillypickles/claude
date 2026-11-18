#!/usr/bin/env python3
"""Fallback when Klaviyo's screenshot_url is missing: screenshot rendered email HTML with Chromium.
Usage: python3 shoot_email_html.py <folder>   (reads <folder>/html_<template_id>.html, writes <folder>/shot_<template_id>.png at 600px wide, full page)
prep_email_week.py prefers shot_<id>.png over thumb_<id>.png when both exist."""
import sys, pathlib
from playwright.sync_api import sync_playwright
folder = pathlib.Path(sys.argv[1])
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_page(viewport={'width': 600, 'height': 900})
    for f in sorted(folder.glob('html_*.html')):
        pg.goto(f.resolve().as_uri(), wait_until='networkidle'); pg.wait_for_timeout(300)
        out = folder / f.name.replace('html_', 'shot_').replace('.html', '.png')
        pg.screenshot(path=str(out), full_page=True); print(out)
    b.close()
