# HCRIS codemap — the lines that matter

HCRIS public use files ship per form type (hospital cost report form 2552-10 is the one
you want) as three linked files:

- **RPT** — one row per report: provider CCN, fiscal year begin/end, report status
  (as-submitted vs settled), processing date.
- **NMRC** — the numbers: `rpt_rec_num`, `wksht_cd`, `line_num`, `clmn_num`, `itm_val_num`.
- **ALPHA** — text fields, same key structure.

Everything is keyed by **worksheet code + line + column**. Without the map, NMRC is
unreadable, which is why so few people use this data — and why it still has edge.

## Core extraction points (form 2552-10)

| Item | Worksheet | Notes |
|---|---|---|
| Net patient revenue | G-3 | Line for net patient revenues; the top of the income statement |
| Total operating expense | G-3 | Pair with revenue for operating margin |
| Net income / total margin | G-3 | Includes investment and non-operating income — separate it |
| Beds, bed days available | S-3 Pt I | Denominator for occupancy |
| Discharges and patient days by payer | S-3 Pt I | Medicare, Medicaid, total — the payer-mix backbone |
| Full-time equivalents | S-3 Pt II | Labour cost per adjusted discharge |
| Uncompensated and charity care | S-10 | Charity care, bad debt, cost-to-charge applied |
| Cost-to-charge ratios by department | C Pt I | Needed to convert charges to cost |
| Capital costs (buildings, fixtures, movable equipment) | A, A-7 | Age of plant and the capex-capacity read |
| Medicare settlement | E series | Medicare-specific reimbursement position |
| Provider identification and control type | S-2 Pt I | Ownership: voluntary non-profit, proprietary, government |

Column numbers vary by worksheet part; always confirm against the current CMS form
instructions for the report year, because line numbering has changed across form
versions (2552-96 vs 2552-10 are not interchangeable).

## Traps

1. **Total margin vs operating margin.** Non-operating investment income can be the
   difference between a reported loss and a reported profit for a large non-profit
   system. Always report operating margin separately.
2. **As-submitted vs settled.** Settlement can move Medicare reimbursement materially.
   A trend built from a mix of both is not a trend.
3. **Fiscal years are not calendar years** and vary by system. Align on fiscal-year end.
4. **Cost-to-charge ratios** are required to make charge data meaningful; raw charges
   are close to fiction.
5. **CCN changes** on ownership change, merger or re-certification, which silently
   breaks facility time series. Reconcile CCNs across years before trending.
6. **Critical-access hospitals** are cost-reimbursed, so their margins mean something
   structurally different. Segment them out.

## Cleaned alternatives

RAND Hospital Data and NBER both publish cleaned, harmonised versions of HCRIS with
consistent variable names across years. For a multi-year panel, start there and use raw
HCRIS to verify specific facilities — it will save days.
