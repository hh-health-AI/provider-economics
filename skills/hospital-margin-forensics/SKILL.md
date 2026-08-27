---
name: hospital-margin-forensics
description: >
  This skill should be used when the user asks about "hospital margins", "cost
  reports", "HCRIS", "payer mix", "occupancy", "uncompensated care", "hospital capex
  capacity", "will hospitals buy", or wants a facility-level read on provider
  financial health as a cross-read for suppliers. Anchors prompt-library ID SUB-SVC-01.
metadata:
  version: "0.1.0"
  layer: "Financial"
---

# Hospital margin forensics

Extract facility-level operating economics from Medicare cost reports and turn them
into either an operator view or a supplier-demand cross-read.

## Workflow

1. **Define the facility set.** For a listed operator, the set is its CCNs — build it
   from the operator's own facility list and the CMS provider-of-services file. For a
   supplier cross-read, the set is the facility type that buys the product (academic
   medical centres, community hospitals, critical-access, IDNs in named states).
2. **Pull and extract** (`scripts/hcris_extract.py`). HCRIS ships as three files per
   report — RPT (report header), NMRC (numeric values), ALPHA (text) — keyed by
   worksheet, line and column. Use `references/hcris-codemap.md` to get the lines;
   without the codemap the numeric file is unreadable.
3. **Compute the panel**, per facility per fiscal year:
   - Total margin and **operating margin** (exclude investment income — this is the
     single most common error, and in a strong equity market it turns loss-making
     hospitals into profitable ones on paper).
   - Payer mix by discharges and by revenue: Medicare, Medicaid, managed care, other.
   - Occupancy, average length of stay, case-mix index.
   - Uncompensated care and charity care (Worksheet S-10).
   - Capital cost as a share of total cost, and the age of plant — **the direct capex
     capacity read that a medtech thesis needs**.
4. **Handle the vintage.** Mark each report as-submitted or settled, and never mix the
   two in a trend. Report the fiscal-year end, not the posting date.
5. **Aggregate carefully.** System-level conclusions require rolling up CCNs to the
   parent, which HCRIS does not do for you. Ownership changes mid-year make this
   genuinely difficult; state your roll-up method.
6. **Cross-read to the supplier thesis.** The chain is: hospital operating margin →
   capital budget → equipment replacement cycle → supplier order book. An ageing plant
   with improving margin is the bullish medtech setup; a young plant with deteriorating
   margin is the bearish one. Say which you found and in which facility segment.
7. **Test against the listed operator's own numbers.** If a listed operator's reported
   margin diverges materially from the sum of its facilities' cost reports, that is a
   finding — usually explained by corporate allocation, non-hospital segments or
   timing, but occasionally by something else. Hand it to `sec-forensics`.
8. Emit the brief.

## Not-automatic

Cost-report margins do not license a quarterly earnings conclusion for a listed
operator — the lag is too long and the accounting basis differs from GAAP. They license
a structural claim about the direction of provider financial health.

Framework anchor: Cleverley, *Essentials of Health Care Finance*.
Reference: `references/hcris-codemap.md`. Contract: `../../references/evidence-brief.md`.
