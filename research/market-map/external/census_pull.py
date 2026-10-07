"""Pull ACS 5-year demographics for CBSAs and counties.

Requires CENSUS_API_KEY in the environment. Writes census_cbsa.csv and
census_county.csv next to this script. Uses the newest vintage the API
serves among CANDIDATE_VINTAGES and the vintage 5 years earlier for growth.
"""
import csv
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ["CENSUS_API_KEY"]
CANDIDATE_VINTAGES = [2024, 2023]
CBSA_GEO = "metropolitan statistical area/micropolitan statistical area"
MICRO_KEEP_POP = 150_000

AGE_25_44 = [f"B01001_{i:03d}E" for i in (11, 12, 13, 14, 35, 36, 37, 38)]
BA_PLUS = [f"B15003_{i:03d}E" for i in (22, 23, 24, 25)]
VARS = (["NAME", "B01003_001E", "B19013_001E", "B01002_001E", "B01001_001E"]
        + AGE_25_44 + ["B15003_001E"] + BA_PLUS)
FIELDS = ["pop", "income", "median_age", "share_25_44", "share_ba_plus",
          "pop_growth_5y", "vintage"]


def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def query(vintage, get_vars, geo, extra=""):
    url = (f"https://api.census.gov/data/{vintage}/acs/acs5?get={','.join(get_vars)}"
           f"&for={urllib.request.quote(geo)}:*{extra}&key={KEY}")
    rows = get(url)
    return [dict(zip(rows[0], r)) for r in rows[1:]]


def num(v):
    """Census sentinels (-666666666, -999999999, etc.) and blanks become None."""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x < 0 else x


def derive(r):
    pop, tot_age, tot_ed = num(r["B01003_001E"]), num(r["B01001_001E"]), num(r["B15003_001E"])
    age = [num(r[k]) for k in AGE_25_44]
    ba = [num(r[k]) for k in BA_PLUS]
    share_age = (round(sum(age) / tot_age, 4)
                 if tot_age and None not in age else None)
    share_ba = round(sum(ba) / tot_ed, 4) if tot_ed and None not in ba else None
    income = num(r["B19013_001E"])
    return {"pop": int(pop) if pop is not None else None,
            "income": int(income) if income is not None else None,
            "median_age": num(r["B01002_001E"]),
            "share_25_44": share_age, "share_ba_plus": share_ba}


def growth(now, then):
    if now is None or not then:
        return None
    return round(now / then - 1, 4)


def pick_vintage():
    for v in CANDIDATE_VINTAGES:
        try:
            get(f"https://api.census.gov/data/{v}/acs/acs5?get=NAME&for=us:1&key={KEY}")
            return v
        except Exception:
            continue
    raise SystemExit("No candidate ACS 5-year vintage available")


def split_cbsa_name(name):
    # e.g. "Dallas-Fort Worth-Arlington, TX Metro Area"
    base, _, kind = name.rpartition(" ")
    base = base.rsplit(" ", 1)[0] if base.endswith((" Metro", " Micro")) else base
    places, _, states = base.partition(", ")
    return places.split("-")[0].strip(), states.strip()


def write(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


def main():
    vintage = pick_vintage()
    base = vintage - 5
    print(f"vintage {vintage}, growth base {base}")

    # CBSA
    cur = query(vintage, VARS, CBSA_GEO)
    old = {r[CBSA_GEO]: num(r["B01003_001E"])
           for r in query(base, ["B01003_001E"], CBSA_GEO)}
    cbsa_rows, dropped_micro = [], 0
    for r in cur:
        name = r["NAME"]
        d = derive(r)
        is_metro = name.endswith("Metro Area")
        if not is_metro and (d["pop"] or 0) <= MICRO_KEEP_POP:
            dropped_micro += 1
            continue
        city, state = split_cbsa_name(name)
        code = r[CBSA_GEO]
        cbsa_rows.append({"cbsa_code": code, "name": name, "principal_city": city,
                          "state": state, **d,
                          "pop_growth_5y": growth(d["pop"], old.get(code)),
                          "vintage": vintage})
    cbsa_rows.sort(key=lambda x: -(x["pop"] or 0))
    write(os.path.join(HERE, "census_cbsa.csv"),
          ["cbsa_code", "name", "principal_city", "state"] + FIELDS, cbsa_rows)
    unmatched = sum(1 for x in cbsa_rows if x["pop_growth_5y"] is None)
    print(f"cbsa rows {len(cbsa_rows)} (dropped {dropped_micro} micro), "
          f"no growth match {unmatched}")

    # County
    cur = query(vintage, VARS, "county", "&in=state:*")
    old = {(r["state"], r["county"]): num(r["B01003_001E"])
           for r in query(base, ["B01003_001E"], "county", "&in=state:*")}
    county_rows = []
    for r in cur:
        d = derive(r)
        k = (r["state"], r["county"])
        county_rows.append({"state_fips": r["state"], "county_fips": r["county"],
                            "name": r["NAME"], **d,
                            "pop_growth_5y": growth(d["pop"], old.get(k)),
                            "vintage": vintage})
    county_rows.sort(key=lambda x: (x["state_fips"], x["county_fips"]))
    write(os.path.join(HERE, "census_county.csv"),
          ["state_fips", "county_fips", "name"] + FIELDS, county_rows)
    unmatched = sum(1 for x in county_rows if x["pop_growth_5y"] is None)
    print(f"county rows {len(county_rows)}, no growth match {unmatched}")


if __name__ == "__main__":
    main()
