#!/usr/bin/env python3
"""Build the weekly email report (single attachable HTML) from a prepared data JSON.

Usage:
  python3 build_email_report.py --data email_data.json --template report_template.html \
      --out email_report_MM.DD.html [--take takeaways.html] [--gen "Nov 18, 2026"] [--stats-out stats.json]

The data JSON (see prep_email_week.py) holds campaigns, each with variations carrying raw counts
(recipients, delivered, opens, clicks, orders, revenue, unsubs), an arm (test / control / single / other),
a design label and an embedded image. This script adds rates, totals, KPIs and the pooled design test,
then fills __DATA__, __GEN__ and __TAKE__ in the template. It holds no business data.
"""
import argparse, datetime as dt, json, math, re

def rate(n, d): return (n / d) if d else None

def agg(rows):
    keys = ("recipients", "delivered", "opens", "clicks", "orders", "revenue", "unsubs")
    t = {k: sum((r.get(k) or 0) for r in rows) for k in keys}
    t["open_rate"] = rate(t["opens"], t["delivered"]); t["click_rate"] = rate(t["clicks"], t["delivered"])
    t["order_rate"] = rate(t["orders"], t["delivered"]); t["rpr"] = rate(t["revenue"], t["delivered"])
    t["unsub_rate"] = rate(t["unsubs"], t["delivered"]); t["aov"] = rate(t["revenue"], t["orders"])
    return t

def ztest(x1, n1, x2, n2):
    """Two-proportion z-test, pooled standard error. Positive z = first group higher."""
    if not n1 or not n2: return None
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return (x1 / n1 - x2 / n2) / se if se else None

def pooled(camps, label):
    pairs = [c for c in camps if any(v["arm"] == "test" for v in c["variations"]) and any(v["arm"] == "control" for v in c["variations"])]
    if not pairs: return None
    def side(cs, arm): return agg([v for c in cs for v in c["variations"] if v["arm"] == arm])
    T, C = side(pairs, "test"), side(pairs, "control")
    out = {"label": label, "sends": len(pairs), "test": T, "control": C}
    for m, k in (("clicks", "clicks"), ("orders", "orders"), ("opens", "opens")):
        out["z_" + m] = ztest(T[k], T["delivered"], C[k], C["delivered"])
    # leave-one-send-out: is the result carried by one campaign?
    loo = {}
    for m in ("clicks", "orders"):
        zs = []
        for c in pairs:
            rest = [x for x in pairs if x is not c]
            t, k2 = side(rest, "test"), side(rest, "control")
            zs.append((ztest(t[m], t["delivered"], k2[m], k2["delivered"]), c["short"]))
        zs = [z for z in zs if z[0] is not None]
        loo[m] = {"min": min(zs)[0], "min_send": min(zs)[1], "max": max(zs)[0], "max_send": max(zs)[1]} if zs else None
    out["loo"] = loo
    def verdict(m):
        z, l = out["z_" + m], loo.get(m)
        if z is None: return "n/a"
        if abs(z) < 1.96: return "No winner (|z| under 1.96)"
        lead = "Test" if z > 0 else "Control"
        if l and ((z > 0 and l["min"] < 1.96) or (z < 0 and l["max"] > -1.96)):
            send = l["min_send"] if z > 0 else l["max_send"]
            return f"{lead} ahead, but not a clean win: dropping {send} takes |z| under 1.96"
        return f"{lead} wins (|z| 1.96+ and holds when any one send is dropped)"
    out["verdict_clicks"], out["verdict_orders"] = verdict("clicks"), verdict("orders")
    out["rpr_lift"] = rate((T["rpr"] or 0) - (C["rpr"] or 0), C["rpr"]) if C["rpr"] else None
    return out

def short_name(name):
    s = re.sub(r"^(Early Winter|Late Fall|Fall|Winter|Spring|Summer)\s*(\d{4})\s*", lambda m: "".join(w[0] for w in m.group(1).split()) + m.group(2)[2:] + " ", name)
    s = re.sub(r"^(\S+)\s*_", r"\1 ", s)
    s = s.replace("_Metro All_Open Registration", " open reg").replace("_Metro All", " open reg").replace("_Last Call", " last call")
    return s.replace("_", " ").strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--template", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--take"); ap.add_argument("--gen"); ap.add_argument("--stats-out")
    a = ap.parse_args()
    D = json.load(open(a.data))
    camps = D["campaigns"]
    for c in camps:
        c.setdefault("short", short_name(c["name"]))
        for v in c["variations"]:
            v.update({k: val for k, val in agg([v]).items() if k not in v})
        c["total"] = agg(c["variations"])
        dv = c.get("device")
        if dv:
            ck, op = dv["clicks"], dv["opens"]
            known_c = ck["mobile"] + ck["web"]; known_o = op["mobile"] + op["web"]
            c["device_pct"] = {"click_mobile": rate(ck["mobile"], known_c), "click_web": rate(ck["web"], known_c), "click_known": known_c,
                "open_mobile": rate(op["mobile"], known_o), "open_web": rate(op["web"], known_o), "open_known": known_o,
                "open_known_share": rate(known_o, known_o + op["unknown"])}
    allv = [v for c in camps for v in c["variations"]]
    T = agg(allv)
    dsum = {"cm": 0, "cw": 0, "co": 0, "om": 0, "ow": 0, "ou": 0}
    for c in camps:
        dv = c.get("device")
        if not dv: continue
        dsum["cm"] += dv["clicks"]["mobile"]; dsum["cw"] += dv["clicks"]["web"]; dsum["co"] += dv["clicks"]["other"]
        dsum["om"] += dv["opens"]["mobile"]; dsum["ow"] += dv["opens"]["web"]; dsum["ou"] += dv["opens"]["unknown"]
    T["device"] = {"click_mobile": rate(dsum["cm"], dsum["cm"] + dsum["cw"]), "click_web": rate(dsum["cw"], dsum["cm"] + dsum["cw"]),
        "click_known": dsum["cm"] + dsum["cw"], "click_other": dsum["co"],
        "open_mobile": rate(dsum["om"], dsum["om"] + dsum["ow"]), "open_web": rate(dsum["ow"], dsum["om"] + dsum["ow"]),
        "open_known": dsum["om"] + dsum["ow"], "open_known_share": rate(dsum["om"] + dsum["ow"], dsum["om"] + dsum["ow"] + dsum["ou"])}
    T["campaigns"] = len(camps); T["variations"] = len(allv)
    T["split_campaigns"] = sum(1 for c in camps if len(c["variations"]) > 1)
    D["total"] = T
    tests = [pooled(camps, "All split sends")]
    for typ in sorted({c["type"] for c in camps}):
        p = pooled([c for c in camps if c["type"] == typ], typ)
        if p and p["sends"] != (tests[0] or {}).get("sends"): tests.append(p)
    D["tests"] = [t for t in tests if t]
    gen = a.gen or dt.date.today().strftime("%b %-d, %Y")
    take = open(a.take).read() if a.take else "<li>[takeaways pending]</li>"
    html = open(a.template).read()
    payload = json.dumps(D, separators=(",", ":")).replace("</", "<\\/")
    html = html.replace("__DATA__", payload).replace("__GEN__", gen).replace("__TAKE__", take)
    for bad in ("\u2014", "\u2013"):
        if bad in html: raise SystemExit("em or en dash found in output; fix the inputs")
    open(a.out, "w").write(html)
    if a.stats_out:
        S = {"total": T, "tests": D["tests"], "campaigns": [{k: c[k] for k in ("short", "type", "cities", "send", "total", "device_pct") if k in c} | {"variations": [{k: v[k] for k in v if k != "img"} for v in c["variations"]]} for c in camps]}
        json.dump(S, open(a.stats_out, "w"), indent=1, default=str)
    print(f"wrote {a.out} ({len(html)/1e6:.2f} MB), {len(camps)} campaigns, {len(allv)} variations")

if __name__ == "__main__":
    main()
