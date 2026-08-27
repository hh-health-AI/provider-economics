---
name: nonprofit-990-scan
description: >
  This skill should be used when the user asks about "nonprofit hospitals", "990",
  "Schedule H", "charity care", "health system financials", "private competitor
  benchmarking", or needs to see the economics of the non-listed part of the provider
  market.
metadata:
  version: "0.1.0"
  layer: "Financial"
---

# Nonprofit 990 scan

Read the non-listed majority of the US hospital market through IRS Form 990 filings.

## Workflow

1. **Find the filer** (`scripts/propublica_990.py --search "Advocate Health"`). Large
   systems file through many related entities; the parent's 990 is not the whole system,
   and obligated-group financial statements on EMMA (municipal bond disclosure) often
   give a better system-wide view than any single 990.
2. **Pull the financial summary**: total revenue, total expenses, net income, total
   assets, net assets. Trend across the available years.
3. **Go into the full filing for Schedule H.** The API summary does not carry it. The
   XML filing does, and Schedule H is where the interesting content is: charity care at
   cost, unreimbursed Medicaid, community health improvement, and the financial
   assistance policy. Charity care as a share of expenses is the number that carries
   both regulatory risk and demand information.
4. **Read executive compensation (Schedule J)** as a governance and cost-discipline
   signal, not for its own sake.
5. **Benchmark.** A single system's margin means little; the same system against its
   regional peers and against MedPAC's all-hospital margin benchmark means a lot.
6. **Convert to the investment question.** Non-profit system margin and balance-sheet
   strength drive: capital equipment purchasing, willingness to take risk-based
   contracts, and receptivity to new technology with a payback period. That is the
   read-through for listed suppliers and for value-based-care enablers.
7. Emit the brief, with the lag stated plainly.

## Caveats

Roughly one year or more of lag, and filings arrive irregularly. Entity structures are
complex and consolidations differ from GAAP. Schedule H definitions of charity care
changed over time and are applied inconsistently between systems, so cross-system
comparison of charity care needs care. ProPublica's API is free subject to their data
terms of use; respect them and cache rather than re-querying.

## Not-automatic

A non-profit system's 990 margin does not license a conclusion about a listed
competitor's pricing power in the same market without local share and payer data.

Contract: `../../references/evidence-brief.md`.
