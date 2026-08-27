#!/usr/bin/env python3
"""Extract facility economics from HCRIS hospital cost-report public use files.

Stdlib only. Works from the CMS quarterly zip for form 2552-10, which contains
<...>_RPT.CSV, <...>_NMRC.CSV and <...>_ALPHA.CSV.

Usage
-----
    python3 hcris_extract.py --zip HOSP10FY2024.zip --list-providers | head
    python3 hcris_extract.py --zip HOSP10FY2024.zip --ccn 050441 --extract
    python3 hcris_extract.py --zip HOSP10FY2024.zip --ccn 050441 --raw G300000

See references/hcris-codemap.md. NMRC is keyed by worksheet + line + column and is
unreadable without it. Confirm line numbers against the CMS form instructions for the
report year: 2552-96 and 2552-10 are not interchangeable.
"""
import argparse, csv, io, json, sys, zipfile

# Worksheet/line/column targets for form 2552-10. Verify against CMS instructions for
# the report year before trusting any single line -- CMS renumbers between versions.
TARGETS = {
    "net_patient_revenue":      ("G300000", "00300", "00100"),
    "total_operating_expense":  ("G300000", "00400", "00100"),
    "net_income_total":         ("G300000", "02900", "00100"),
    "beds":                     ("S300001", "01400", "00200"),
    "bed_days_available":       ("S300001", "01400", "00300"),
    "total_discharges":         ("S300001", "01400", "01500"),
    "medicare_discharges":      ("S300001", "01400", "01300"),
    "medicaid_discharges":      ("S300001", "01400", "01400"),
    "total_patient_days":       ("S300001", "01400", "00800"),
    "charity_care_cost":        ("S100000", "02300", "00300"),
    "bad_debt_cost":            ("S100000", "02900", "00100"),
}


def read_csv(zf, suffix):
    for n in zf.namelist():
        if n.upper().endswith(suffix):
            return list(csv.reader(io.StringIO(zf.read(n).decode("utf-8", errors="replace"))))
    raise SystemExit(f"No file ending {suffix} in zip. Members: {zf.namelist()[:10]}")


def load(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        rpt = read_csv(zf, "_RPT.CSV")
        nmrc = read_csv(zf, "_NMRC.CSV")
    # RPT layout: rpt_rec_num, prvdr_ctrl_type_cd, prvdr_num, npi, rpt_stus_cd,
    #             fy_bgn_dt, fy_end_dt, proc_dt, initl_rpt_sw, last_rpt_sw, trnsmtl_num,
    #             fi_num, adr_vndr_cd, fi_creat_dt, util_cd, npr_dt, spec_ind, fi_rcpt_dt
    reports = {}
    for row in rpt:
        if len(row) < 8:
            continue
        reports[row[0]] = {"rpt_rec_num": row[0], "control_type": row[1], "ccn": row[2],
                           "status": row[4], "fy_begin": row[5], "fy_end": row[6],
                           "processed": row[7]}
    # NMRC layout: rpt_rec_num, wksht_cd, line_num, clmn_num, itm_val_num
    values = {}
    for row in nmrc:
        if len(row) < 5:
            continue
        values.setdefault(row[0], {})[(row[1].strip(), row[2].strip(), row[3].strip())] = row[4]
    return reports, values


STATUS = {"1": "as-submitted", "2": "settled", "3": "settled with audit",
          "4": "reopened", "5": "amended"}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zip", required=True)
    ap.add_argument("--ccn", help="6-digit CMS certification number")
    ap.add_argument("--list-providers", action="store_true")
    ap.add_argument("--extract", action="store_true")
    ap.add_argument("--raw", metavar="WKSHT", help="dump every value for a worksheet code")
    a = ap.parse_args()

    reports, values = load(a.zip)

    if a.list_providers:
        seen = {}
        for r in reports.values():
            seen.setdefault(r["ccn"], r)
        json.dump(sorted(seen.values(), key=lambda r: r["ccn"]), sys.stdout, indent=2)
        print(); return

    if not a.ccn:
        ap.error("--ccn required unless --list-providers")

    mine = [r for r in reports.values() if r["ccn"].strip() == a.ccn.strip()]
    if not mine:
        sys.stderr.write("No reports for that CCN in this file. CCNs change on ownership "
                         "change or re-certification -- reconcile across years before "
                         "trending.\n")
        sys.exit(2)

    out = []
    for r in sorted(mine, key=lambda x: x["fy_end"]):
        vals = values.get(r["rpt_rec_num"], {})
        if a.raw:
            rows = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in vals.items() if k[0] == a.raw}
            out.append({**r, "raw": rows})
            continue
        rec = {**r, "status_read": STATUS.get(r["status"], r["status"])}
        for name, key in TARGETS.items():
            raw = vals.get(key)
            try:
                rec[name] = float(raw) if raw not in (None, "") else None
            except ValueError:
                rec[name] = None
        npr, opex = rec.get("net_patient_revenue"), rec.get("total_operating_expense")
        if npr and opex:
            rec["operating_margin"] = round((npr - opex) / npr, 4)
        if rec.get("net_income_total") and npr:
            rec["total_margin"] = round(rec["net_income_total"] / npr, 4)
        days, bed_days = rec.get("total_patient_days"), rec.get("bed_days_available")
        if days and bed_days:
            rec["occupancy"] = round(days / bed_days, 4)
        td, md, cd = rec.get("total_discharges"), rec.get("medicare_discharges"), rec.get("medicaid_discharges")
        if td:
            rec["medicare_discharge_share"] = round(md / td, 4) if md else None
            rec["medicaid_discharge_share"] = round(cd / td, 4) if cd else None
        out.append(rec)

    json.dump({
        "ccn": a.ccn,
        "reports": out,
        "mandatory_reads": [
            "Report OPERATING margin separately from total margin. Non-operating "
            "investment income turns loss-making systems profitable on paper.",
            "Never mix as-submitted and settled reports in one trend -- see status_read.",
            "Fiscal years vary by system; align on fy_end, not on posting date.",
            "Critical-access hospitals are cost-reimbursed; segment them out.",
            "For a multi-year panel start from the RAND or NBER cleaned HCRIS files and "
            "use raw HCRIS to verify specific facilities.",
        ],
    }, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
