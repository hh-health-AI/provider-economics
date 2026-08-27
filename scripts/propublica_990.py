#!/usr/bin/env python3
"""Query IRS Form 990 data through the ProPublica Nonprofit Explorer API.

Stdlib only, free, no key. Respect ProPublica's data terms of use and cache results
rather than re-querying.

Usage
-----
    python3 propublica_990.py --search "Advocate Health"
    python3 propublica_990.py --ein 361413480 --financials
"""
import argparse, json, sys, urllib.parse, urllib.request

from _ua import user_agent

BASE = "https://projects.propublica.org/nonprofits/api/v2"
UA = user_agent("propublica-990")


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--search")
    ap.add_argument("--state", help="two-letter code to narrow a search")
    ap.add_argument("--ein")
    ap.add_argument("--financials", action="store_true")
    a = ap.parse_args()

    if a.search:
        q = {"q": a.search}
        if a.state:
            q["state[id]"] = a.state.upper()
        res = get(f"{BASE}/search.json?" + urllib.parse.urlencode(q))
        orgs = [{"ein": o.get("ein"), "name": o.get("name"), "city": o.get("city"),
                 "state": o.get("state"), "ntee": o.get("ntee_code"),
                 "subsection": o.get("subseccd")} for o in res.get("organizations", [])]
        json.dump({"total": res.get("total_results"), "organizations": orgs,
                   "note": "Large systems file through many related entities. The parent "
                           "990 is not the whole system; obligated-group statements on "
                           "EMMA often give a better system-wide view."},
                  sys.stdout, indent=2)
        print(); return

    if not a.ein:
        ap.error("--search or --ein required")

    org = get(f"{BASE}/organizations/{a.ein}.json")
    if not a.financials:
        json.dump(org, sys.stdout, indent=2); print(); return

    filings = org.get("filings_with_data", []) or []
    rows = []
    for f in filings:
        rev, exp = f.get("totrevenue"), f.get("totfuncexpns")
        rows.append({
            "tax_year": f.get("tax_prd_yr"),
            "total_revenue": rev,
            "total_expenses": exp,
            "operating_margin": round((rev - exp) / rev, 4) if rev and exp else None,
            "total_assets": f.get("totassetsend"),
            "net_assets": f.get("totnetassetend"),
            "pdf_url": f.get("pdf_url"),
        })
    json.dump({
        "ein": a.ein,
        "name": (org.get("organization") or {}).get("name"),
        "years": sorted(rows, key=lambda r: r["tax_year"] or 0),
        "next_steps": [
            "Schedule H (charity care at cost, unreimbursed Medicaid, community benefit) "
            "is NOT in this API summary. Parse the full filing XML or the PDF above.",
            "Schedule J carries executive compensation -- a governance and cost-discipline "
            "signal, not an end in itself.",
            "Benchmark against regional peers and the MedPAC all-hospital margin; a single "
            "system's margin in isolation means little.",
            "Lag is a year or more and filings arrive irregularly. State the vintage.",
        ],
    }, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
