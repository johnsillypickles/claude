#!/usr/bin/env python3
"""Count league spots, not orders, in weekly.json.

UpPromote records one referral per order, so an order for 2 league spots counts
once. This adds the extra spots back using Shopify line item quantities.

  spots.json   {"<shopify order id>": <league spots in that order>, ...}

For each counted referral in referrals.json whose order is in spots.json, adds
(spots - 1) to that affiliate's signups for the period. Orders missing from
spots.json, and manual referrals with no order, stay at 1.

Usage: add_spots.py --dir <pull output dir> --spots <spots.json>
"""
import argparse
import json
import os
from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--spots", required=True)
    a = ap.parse_args()
    weekly = json.load(open(os.path.join(a.dir, "weekly.json")))
    refs = json.load(open(os.path.join(a.dir, "referrals.json")))
    spots = {str(k): int(v) for k, v in json.load(open(a.spots)).items()}

    extra = defaultdict(int)
    for period, email, order_id in refs:
        if order_id in spots and spots[order_id] > 1:
            extra[(period, email)] += spots[order_id] - 1
    for row in weekly:
        row[4] += extra.get((row[0], row[2]), 0)

    json.dump(weekly, open(os.path.join(a.dir, "weekly.json"), "w"))
    missing = sum(1 for _, _, o in refs if o and o not in spots)
    print(f"orders={len(refs)} extra_spots={sum(extra.values())} orders_missing_from_spots={missing}")


if __name__ == "__main__":
    main()
