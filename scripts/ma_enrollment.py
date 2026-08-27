#!/usr/bin/env python3
"""Aggregate CMS Medicare Advantage enrolment by contract, plan and county.

Stdlib only. Works from the CMS monthly enrolment public use files (CPSC Contract Info
and CPSC Enrollment Info CSVs, or the combined monthly county-level file).

Usage
-----
    python3 ma_enrollment.py --contract-csv CPSC_Contract_Info_2026_06.csv \
                             --enrollment-csv CPSC_Enrollment_Info_2026_06.csv \
                             --org "Humana" --summarise
    python3 ma_enrollment.py --enrollment-csv ... --contract H1036 --by-county

Enrolment is monthly and timely. Star Ratings are annual (October) and set bonus
payments roughly 14 months forward -- pair the two.
"""
import argparse, collections, csv, json, sys


def load(path):
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f))


def pick(row, *names):
    low = {(k or "").strip().lower(): v for k, v in row.items()}
    for n in names:
        if n in low:
            return (low[n] or "").strip()
    return ""


def to_int(v):
    v = (v or "").replace(",", "").strip()
    if v in ("", "*", "N/A"):
        return None  # CMS suppresses counts of 10 or fewer
    try:
        return int(float(v))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--enrollment-csv", required=True)
    ap.add_argument("--contract-csv")
    ap.add_argument("--org", help="parent organisation name substring")
    ap.add_argument("--contract", help="contract id, e.g. H1036")
    ap.add_argument("--by-county", action="store_true")
    ap.add_argument("--summarise", action="store_true")
    a = ap.parse_args()

    enrol = load(a.enrollment_csv)
    contracts = {}
    if a.contract_csv:
        for r in load(a.contract_csv):
            cid = pick(r, "contract id", "contract_id", "contractid")
            contracts[cid] = {
                "organisation": pick(r, "organization marketing name", "parent organization",
                                     "organization name"),
                "plan_type": pick(r, "plan type", "plan_type"),
                "snp": pick(r, "special needs plan", "snp plan"),
            }

    suppressed = 0
    rows = []
    for r in enrol:
        cid = pick(r, "contract id", "contract_id", "contractid")
        meta = contracts.get(cid, {})
        if a.contract and cid != a.contract:
            continue
        if a.org and a.org.lower() not in (meta.get("organisation", "") or "").lower():
            continue
        n = to_int(pick(r, "enrollment", "enrolled"))
        if n is None:
            suppressed += 1
            continue
        rows.append({"contract": cid, "plan": pick(r, "plan id", "plan_id"),
                     "state": pick(r, "state"), "county": pick(r, "county"),
                     "enrollment": n, **meta})

    if not rows:
        sys.stderr.write("No rows matched. Check the organisation name as CMS spells it "
                         "(marketing name and parent organisation often differ).\n")
        sys.exit(2)

    if a.summarise:
        by_contract = collections.Counter()
        by_type = collections.Counter()
        by_state = collections.Counter()
        snp = 0
        for r in rows:
            by_contract[r["contract"]] += r["enrollment"]
            by_type[r.get("plan_type") or "unknown"] += r["enrollment"]
            by_state[r["state"]] += r["enrollment"]
            if (r.get("snp") or "").strip().lower() in ("yes", "y", "true"):
                snp += r["enrollment"]
        total = sum(r["enrollment"] for r in rows)
        json.dump({
            "total_enrollment": total,
            "suppressed_cells": suppressed,
            "snp_enrollment": snp,
            "snp_share": round(snp / total, 4) if total else None,
            "top_contracts": by_contract.most_common(15),
            "by_plan_type": by_type.most_common(),
            "top_states": by_state.most_common(15),
            "reading": [
                "Track growth MIX, not just growth. D-SNP and C-SNP growth carries a "
                "different revenue, acuity and margin profile from general enrolment.",
                "Growth bought with benefit richness is negative-margin growth. The "
                "benefit design is in the plan benefit package filings, not here.",
                "Pair with the October Star Ratings: a rating change sets bonus payments "
                "about 14 months forward, mapped to membership in AFFECTED contracts.",
                "Counts of 10 or fewer are suppressed -- see suppressed_cells.",
            ],
        }, sys.stdout, indent=2)
        print(); return

    json.dump(rows if a.by_county else rows[:500], sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
