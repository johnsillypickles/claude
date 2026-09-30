#!/usr/bin/env python3
"""Aggregate UpPromote-tagged Shopify orders into Mon-Sun (America/Chicago) weeks.

Input file: one order per line -> "<name> <createdAt ISO UTC> <subtotal> <flag>"
flag is "BIX" when the order also carries the Referral-Bixgrow tag, else "-".

Usage: uppromote_weekly.py orders.txt <week_end YYYY-MM-DD> <qtd_start YYYY-MM-DD>
"""
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

CT = ZoneInfo("America/Chicago")


def load(path):
    rows = {}
    for line in open(path):
        if not line.strip():
            continue
        name, ts, amount, flag = line.split()
        day = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(CT).date()
        rows[name] = (day, float(amount), flag)  # dedupe on order name
    return rows


def summarize(rows):
    n = len(rows)
    paid = sum(1 for _, a, _ in rows if a > 0)
    net = sum(a for _, a, _ in rows)
    return {
        "orders": n,
        "paid_orders": paid,
        "zero_dollar": n - paid,
        "net": round(net, 2),
        "aov": round(net / paid, 2) if paid else None,
        "bixgrow_overlap": sum(1 for *_, f in rows if f == "BIX"),
    }


def main():
    path, week_end, qtd_start = sys.argv[1], date.fromisoformat(sys.argv[2]), date.fromisoformat(sys.argv[3])
    rows = [r for r in load(path).values() if qtd_start <= r[0] <= week_end]

    weeks = defaultdict(list)
    for r in rows:
        weeks[r[0] + timedelta(days=6 - r[0].weekday())].append(r)

    print("Week ending | orders | paid | net")
    for wk in sorted(weeks, reverse=True):
        s = summarize(weeks[wk])
        print(f"{wk} | {s['orders']} | {s['paid_orders']} | ${s['net']:,.2f}")

    prior = week_end - timedelta(days=7)
    for label, subset in (("Last week", weeks.get(week_end, [])), ("Prior week", weeks.get(prior, [])), ("QTD", rows)):
        print(label, summarize(subset))


if __name__ == "__main__":
    main()
