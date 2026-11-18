#!/usr/bin/env python3
"""Turn a week's raw Klaviyo pulls into the data JSON that build_email_report.py renders.

Inputs (all saved from Klaviyo MCP tool results, read only):
  --report     get_campaign_report result (group_by campaign_id, campaign_message_id,
               send_channel, variation, variation_name; conversion metric = Placed Order)
  --messages   messages_slim.json: {message_id: {name, send_time, strategy, variations:[{id,name,template_id,subject,preview}]}}
  --device     device.json: {"clicks": {msg: {M,B,L,U}}, "opens": {msg: {M,B,E,O,U}}}  (query_metric_aggregates by $message x Client Type)
  --delivery   delivery.json: {msg: {hours_since_week_start: received_count}}  (Received Email, hourly)
  --thumbs     folder with thumb_<template_id>.png (Klaviyo screenshot_url) or shot_<template_id>.png (Playwright)
  --week-start YYYY-MM-DD (Monday, local report time zone)
  --tz-label   label for the report time zone, e.g. CT
  --designs    optional JSON: {"rules": [{"match": "<substring of variation or template name>", "arm": "test|control|single", "design": "<label>"}]}
Output: data JSON (no business data lives in this script).
"""
import argparse, base64, io, json, os, re, datetime as dt
from PIL import Image

STATES = {"Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE",
"Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA",
"Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE",
"Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH",
"Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX",
"Utah":"UT","Vermont":"VT","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY","District of Columbia":"DC",
"Australia":"Australia","Canada":"Canada","Ontario":"ON","New South Wales":"NSW"}
DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def place_from_segment(name):
    """'Maryland - White Marsh Subscribers' -> ('White Marsh','MD'); 'Lexington - Kentucky Subscribers' -> ('Lexington','KY').
    Returns None when the name is not a '<place> - <place> <suffix>' audience."""
    m = re.match(r"^\s*(.+?)\s+-\s+(.+?)(?:\s+(Subscribers|All|Players|Leads))?\s*$", name)
    if not m: return None
    a, b = m.group(1).strip(), m.group(2).strip()
    if "_" in b: return None            # e.g. 'Oregon - Portland_Late Fall 2026 Players' (a player list, not a place audience)
    if a in STATES and b not in STATES: return (b.replace("Greater ", ""), STATES[a], b.startswith("Greater "))
    if b in STATES and a not in STATES: return (a, STATES[b], False)
    return None

def metro_from_campaign(name):
    m = re.search(r"_([^_]+?),\s*([A-Z]{2,3})_", name)
    return (m.group(1), m.group(2)) if m else None

def cities_text(camp_name, included):
    """Plain-English places from the included audience names; metro comes from the campaign name when it has '_City, ST_'."""
    metro = metro_from_campaign(camp_name)
    places, unmapped = [], []
    for a in included:
        p = place_from_segment(a["name"])
        if p: places.append(p)
        else: unmapped.append(a["name"])
    if places:
        names = [p[0] for p in places]
        if metro:
            txt = f"{metro[0]}, {metro[1]} metro"
            if any(n.lower() != metro[0].lower() for n in names):
                lst = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
                txt += f" ({lst} list{'s' if len(names) > 1 else ''})"
        else:
            txt = "; ".join(f"{p[0]}, {p[1]}" for p in places)
        if unmapped: txt += "; plus " + ", ".join(unmapped)
        return txt, (not unmapped), "segment names"
    if unmapped:
        return "National (all markets; audience is not a city list: " + "; ".join(unmapped) + ")", False, "not a city audience"
    return "n/a", False, "no audience"

def excluded_text(excluded):
    out = []
    for a in excluded:
        n = a["name"]
        if re.search(r"suppression|careers", n, re.I): continue
        out.append(n)
    return out

def thumb_uri(folder, tid, width=300, crop_ratio=1.5, quality=65):
    for fn in (f"shot_{tid}.png", f"thumb_{tid}.png"):
        p = os.path.join(folder, fn)
        if os.path.exists(p): break
    else:
        return None, "no image file"
    im = Image.open(p).convert("RGB")
    h = min(im.height, int(im.width * crop_ratio))   # 600 wide -> first 900px
    im = im.crop((0, 0, im.width, h))
    im = im.resize((width, int(h * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), os.path.basename(p)

def classify(var_name, template_name, rules, n_variations):
    for r in rules:
        if r["match"].lower() in (var_name or "").lower() or r["match"].lower() in (template_name or "").lower():
            return r["arm"], r["design"]
    if n_variations == 1: return "single", "Single version"
    if re.search(r"-\s*Test\s*$", var_name or ""): return "test", "Test"
    if re.search(r"-\s*Control\s*$", var_name or ""): return "control", "Control"
    return "other", var_name or "n/a"

def fmt_hour(h):
    h %= 24; s = "AM" if h < 12 else "PM"; return f"{(h % 12) or 12} {s}"

def delivery_text(hist, week_start, tz):
    if not hist: return None
    tot = sum(hist.values()); peak = max(hist, key=hist.get)
    d0 = week_start + dt.timedelta(hours=int(peak))
    share = hist[peak] / tot
    first, last = min(hist), max(k for k, v in hist.items() if v)
    main = [k for k, v in hist.items() if v / tot >= 0.05]
    lo, hi = min(main), max(main)
    if lo == hi: span = ""
    elif hi - lo >= 12:
        span = "; delivered in waves on different days: " + ", ".join(f"{round(hist[k]/tot*100)}% {DAYS[(week_start+dt.timedelta(hours=k)).weekday()]} {fmt_hour(k)}" for k in sorted(main))
    else:
        span = f"; {round(sum(v for k,v in hist.items() if lo<=k<=hi)/tot*100)}% between {fmt_hour(lo)} and {fmt_hour(hi)} {tz}"
    return {"day": DAYS[d0.weekday()], "date": f"{d0.month}/{d0.day}", "time": f"{fmt_hour(int(peak))} {tz}",
            "peak_share": round(share, 3), "sort": int(peak),
            "detail": f"{round(share*100)}% landed in the {fmt_hour(int(peak))} {tz} hour{span}"}

def main():
    ap = argparse.ArgumentParser()
    for a in ("report","messages","device","delivery","thumbs","week_start","out"): ap.add_argument("--"+a.replace("_","-"), required=True)
    ap.add_argument("--tz-label", default="CT"); ap.add_argument("--designs"); ap.add_argument("--template-names")
    ap.add_argument("--title", default="Weekly Email Report"); ap.add_argument("--channel", default="email")
    a = ap.parse_args()
    rep = json.load(open(a.report)); rep = rep.get("data", rep.get("result", {}).get("data"))
    rows = rep["attributes"]["results"]
    msgs = json.load(open(a.messages)); dev = json.load(open(a.device)); dlv = json.load(open(a.delivery))
    dlv = {k: {int(h): c for h, c in v.items()} for k, v in dlv.items()}
    rules = json.load(open(a.designs))["rules"] if a.designs else []
    tnames = json.load(open(a.template_names)) if a.template_names else {}
    ws = dt.datetime.strptime(a.week_start, "%Y-%m-%d")
    camps = {}
    for r in rows:
        g = r["groupings"]
        if g.get("send_channel") != a.channel: continue
        cd = r["campaign_details"]["attributes"]
        c = camps.setdefault(g["campaign_id"], {"id": g["campaign_id"], "message_id": g["campaign_message_id"], "name": cd["name"],
             "send_time_setting": cd.get("send_time"), "tags": cd.get("tags", []), "aud_in": cd["audiences"]["included"],
             "aud_ex": cd["audiences"]["excluded"], "rows": []})
        c["rows"].append(r)
    out = []
    for cid, c in camps.items():
        m = msgs.get(c["message_id"], {})
        vmeta = {v["id"]: v for v in m.get("variations", [])}
        cities, mapped, how = cities_text(c["name"], c["aud_in"])
        variations = []
        for r in c["rows"]:
            g, s = r["groupings"], r["statistics"]
            vm = vmeta.get(g.get("variation")) or (list(vmeta.values())[0] if len(vmeta) == 1 else {})
            tid = vm.get("template_id")
            arm, design = classify(g.get("variation_name") or vm.get("name"), tnames.get(tid), rules, len(c["rows"]))
            img, src = thumb_uri(a.thumbs, tid) if tid else (None, "no template id")
            variations.append({"variation_id": g.get("variation"), "variation_name": g.get("variation_name") or vm.get("name"),
                "arm": arm, "design": design, "template_id": tid, "template_name": tnames.get(tid),
                "subject": vm.get("subject"), "preview": vm.get("preview"), "img": img, "img_note": None if img else src,
                "recipients": s.get("recipients"), "delivered": s.get("delivered"), "opens": s.get("opens_unique"),
                "clicks": s.get("clicks_unique"), "orders": s.get("conversions"), "revenue": s.get("conversion_value"),
                "unsubs": s.get("unsubscribes")})
        order = {"test": 0, "control": 1}
        variations.sort(key=lambda v: order.get(v["arm"], 2))
        d = dev["clicks"].get(c["message_id"]); o = dev["opens"].get(c["message_id"])
        device = None
        if d is not None and o is not None:
            device = {"clicks": {"mobile": d.get("M", 0), "web": d.get("B", 0), "other": d.get("L", 0) + d.get("U", 0)},
                      "opens": {"mobile": o.get("M", 0), "web": o.get("B", 0) + o.get("E", 0), "unknown": o.get("O", 0) + o.get("U", 0)}}
        typ = "Open registration" if "Open Registration" in c["tags"] else ("Last call" if "Last Call" in c["tags"] else (c["tags"][-1] if c["tags"] else "Other"))
        out.append({"id": cid, "name": c["name"], "type": typ, "tags": c["tags"], "cities": cities, "cities_mapped": mapped, "cities_how": how,
            "audience_in": [x["name"] for x in c["aud_in"]], "audience_ex": excluded_text(c["aud_ex"]),
            "send_setting": c["send_time_setting"], "local_time_send": "local" in (m.get("strategy") or ""),
            "send": delivery_text(dlv.get(c["message_id"]), ws, a.tz_label), "device": device, "variations": variations})
    out.sort(key=lambda c: ((c["send"] or {}).get("sort", 9999), c["name"]))
    json.dump({"title": a.title, "week_start": a.week_start, "tz": a.tz_label, "campaigns": out}, open(a.out, "w"), indent=1)
    print(len(out), "campaigns;", sum(len(c["variations"]) for c in out), "variations;", sum(1 for c in out if not c["cities_mapped"]), "not mapped to a city")

if __name__ == "__main__":
    main()
