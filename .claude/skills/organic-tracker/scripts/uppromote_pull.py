#!/usr/bin/env python3
"""Pull UpPromote data for the Organic Marketing Tracker.

Reads the MCP key from the UPPROMOTE_MCP_KEY environment variable and only calls
read tools (review_affiliate is blocked). Writes JSON to the output directory:

  affiliates.json  one row per affiliate (facility program excluded):
                   [name, email, program, joined (YYYY-MM-DD, CT), status, upline_email]
  weekly.json      one row per affiliate per period with any activity:
                   [period_start, period_end, email, clicks, signups]

Periods are Mon to Sun weeks in America/Chicago, from --start through today
(the current week is partial). A week that crosses into a new month is split
in two so monthly and quarter to date totals start on the 1st.

Signups = referrals that are not denied, not refund reversals and not network
(upline) credit. Clicks = total_clicks from get_top_affiliates.

Usage: uppromote_pull.py --start 2026-08-03 --out <dir>
"""
import argparse
import json
import os
import urllib.request
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

URL = "https://mcp.uppromote.com/mcp"
CT = ZoneInfo("America/Chicago")
EXCLUDED_PROGRAMS = {"Facility Referral Program (External)", "Facility Referral Program",
                     "Facility Affiliate Program", "Non-Affiliate Facilities"}


class Client:
    def __init__(self):
        self.h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                  "Authorization": os.environ["UPPROMOTE_MCP_KEY"]}
        self.sid = None
        self._post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                               "clientInfo": {"name": "organic-tracker", "version": "1"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _post(self, body):
        h = dict(self.h)
        if self.sid:
            h["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=h, method="POST")
        with urllib.request.urlopen(req, timeout=120) as r:
            self.sid = r.headers.get("Mcp-Session-Id") or self.sid
            txt = r.read().decode()
        for line in txt.splitlines():
            if line.startswith("data: "):
                return json.loads(line[6:])
        return json.loads(txt) if txt.strip() else None

    def call(self, name, args):
        if name == "review_affiliate":
            raise SystemExit("review_affiliate writes to UpPromote and is never called")
        r = self._post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                        "params": {"name": name, "arguments": args}})
        text = r["result"]["content"][0]["text"]
        data = json.loads(text) if text.lstrip().startswith("{") else None
        if data is None:
            raise SystemExit(f"{name} failed: {text[:300]}")
        return data

    def all_pages(self, name, args):
        page, rows = 1, []
        while True:
            d = self.call(name, {**args, "page": page, "per_page": 100})
            rows += d["data"]
            if not d.get("has_more"):
                return rows
            page += 1


def iso_utc(d, end=False):
    t = time(23, 59, 59) if end else time(0, 0, 0)
    return datetime.combine(d, t, CT).astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")


def ct_date(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(CT).date()


def periods(start, today):
    out, d = [], start - timedelta(days=start.weekday())
    while d <= today:
        end = d + timedelta(days=6)
        split = date(end.year, end.month, 1) if end.month != d.month else None
        if split:
            out += [(d, split - timedelta(days=1)), (split, end)]
        else:
            out.append((d, end))
        d += timedelta(days=7)
    return [(s, min(e, today)) for s, e in out if s <= today]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    c = Client()
    today = datetime.now(CT).date()

    affs = c.all_pages("list_affiliates", {})
    aff_rows = [[f"{x.get('first_name') or ''} {x.get('last_name') or ''}".strip(), (x["email"] or "").lower(),
                 x.get("program_name"), ct_date(x["created_at"]).isoformat(), x.get("status"),
                 (x.get("up_line_affiliate_email") or "").lower()]
                for x in affs if x.get("program_name") not in EXCLUDED_PROGRAMS]
    excluded = {(x["email"] or "").lower() for x in affs if x.get("program_name") in EXCLUDED_PROGRAMS}

    pers = periods(date.fromisoformat(a.start), today)
    signups = defaultdict(int)
    refs = c.all_pages("list_referrals", {"from_date": iso_utc(pers[0][0]), "to_date": iso_utc(today, True)})
    for r in refs:
        if r["status"] == "denied" or r.get("refund_id") or "network" in (r.get("tracking_type") or "").lower():
            continue
        email = (r["affiliate"]["email"] or "").lower()
        d = ct_date(r["created_at"])
        for s, e in pers:
            if s <= d <= e:
                signups[(s, email)] += 1
                break

    clicks = defaultdict(int)
    for s, e in pers:
        for x in c.all_pages("get_top_affiliates", {"from_date": iso_utc(s), "to_date": iso_utc(e, True),
                                                    "exclude_network_sales": True}):
            clicks[(s, (x["email"] or "").lower())] += x.get("total_clicks") or 0

    weekly = []
    for s, e in pers:
        emails = {k[1] for k in list(signups) + list(clicks) if k[0] == s} - excluded
        for em in sorted(emails):
            cl, su = clicks.get((s, em), 0), signups.get((s, em), 0)
            if cl or su:
                weekly.append([s.isoformat(), e.isoformat(), em, cl, su])

    os.makedirs(a.out, exist_ok=True)
    json.dump(aff_rows, open(os.path.join(a.out, "affiliates.json"), "w"))
    json.dump(weekly, open(os.path.join(a.out, "weekly.json"), "w"))
    print(f"affiliates={len(aff_rows)} referrals={len(refs)} weekly_rows={len(weekly)} "
          f"periods={pers[0][0]}..{pers[-1][1]} data_through={today}")


if __name__ == "__main__":
    main()
