"""Pull Google Trends interest by DMA and city for pickleball terms.

Writes trends_dma.csv and trends_city.csv next to this script, plus
trends_log.json with per-request status. Scores are relative (0 to 100)
within each term and are not comparable across terms.
"""
import json
import os
import random
import time
from datetime import datetime, timezone

import pandas as pd
from pytrends.request import TrendReq

HERE = os.path.dirname(os.path.abspath(__file__))
TIMEFRAME = "today 12-m"
DMA_TERMS = ["pickleball", "pickleball league", "pickleball near me",
             "indoor pickleball", "pickleball lessons"]
CITY_TERMS = ["pickleball league", "pickleball near me"]
BUDGET_S = 30 * 60
MAX_TRIES = 6

start = time.time()
log = []


def fetch(pt, term, resolution):
    delay = 30
    for attempt in range(1, MAX_TRIES + 1):
        if time.time() - start > BUDGET_S:
            return None, "budget exhausted"
        try:
            pt.build_payload([term], geo="US", timeframe=TIMEFRAME)
            df = pt.interest_by_region(resolution=resolution, inc_low_vol=True,
                                       inc_geo_code=True)
            return df, f"ok after {attempt} tries"
        except Exception as e:  # pytrends raises generic errors on 429
            msg = f"{type(e).__name__}: {e}"[:200]
            print(f"  {term}/{resolution} attempt {attempt}: {msg}", flush=True)
            if attempt == MAX_TRIES:
                return None, msg
            time.sleep(delay + random.uniform(0, 10))
            delay = min(delay * 2, 300)


def main():
    pt = TrendReq(hl="en-US", tz=0, timeout=(10, 30))
    jobs = [(t, "DMA") for t in DMA_TERMS] + [(t, "CITY") for t in CITY_TERMS]
    out = {"DMA": [], "CITY": []}
    for i, (term, res) in enumerate(jobs):
        if i:
            time.sleep(random.uniform(20, 60))
        print(f"{term} / {res}", flush=True)
        df, status = fetch(pt, term, res)
        pulled_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        n = 0
        if df is not None and len(df):
            df = df.reset_index()
            name_col = df.columns[0]
            for _, r in df.iterrows():
                row = {"term": term, "score": int(r[term]), "pulled_at": pulled_at}
                if res == "DMA":
                    row = {"dma": r[name_col], "dma_code": r.get("geoCode", ""), **row}
                else:
                    row = {"city": r[name_col], **row}
                    for c in ("lat", "lng"):
                        if c in df.columns:
                            row[c] = r[c]
                out[res].append(row)
                n += 1
        log.append({"term": term, "resolution": res, "status": status,
                    "rows": n, "pulled_at": pulled_at})
        print(f"  -> {status}, {n} rows", flush=True)
    pd.DataFrame(out["DMA"]).to_csv(os.path.join(HERE, "trends_dma.csv"), index=False)
    pd.DataFrame(out["CITY"]).to_csv(os.path.join(HERE, "trends_city.csv"), index=False)
    with open(os.path.join(HERE, "trends_log.json"), "w") as f:
        json.dump(log, f, indent=2)


if __name__ == "__main__":
    main()
