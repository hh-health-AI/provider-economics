---
name: ma-margin-normalization
description: >
  This skill should be used when the user asks about "Medicare Advantage margins",
  "MLR", "Star Ratings", "MA enrolment", "risk adjustment", "MedPAC benchmark",
  "payor margin normalisation", "value-based care economics", or is modelling a
  managed-care name. Anchors prompt-library IDs SUB-SVC-03 and SUB-SVC-04.
metadata:
  version: "0.1.0"
  layer: "Financial"
---

# MA margin normalisation

Normalise a managed-care name's reported margin against open enrolment, Star Ratings
and MedPAC benchmark data, so that the reported MLR can be read for what it actually
contains.

## Workflow

1. **Build the enrolment picture.** Monthly CMS MA enrolment files by contract, plan
   and county (`scripts/ma_enrollment.py`). Compute growth, and growth *mix*: which
   counties, which plan types (HMO, PPO, D-SNP, C-SNP), and which competitor lost the
   members. Special-needs-plan growth carries a different margin and acuity profile
   from general-enrolment growth and must be tracked separately.
2. **Layer Star Ratings.** Published each October, they determine quality bonus payments
   two years forward. A rating change is therefore a *dated, known* revenue event with a
   two-year lead — one of the cleanest forward-looking data points in the sector. Map
   the rating change to the share of membership in affected contracts, not to the
   headline company rating.
3. **Normalise the margin.** MedPAC publishes benchmark, bid and payment analysis for
   MA against fee-for-service spending. Use it to separate:
   - margin from **rate** (benchmarks, county rebasing, quality bonus),
   - margin from **risk-score coding intensity**,
   - margin from **actual medical management**.
   Only the third is durable, and it is the smallest of the three at most plans.
4. **Read the reserve development.** Reported MLR is a ratio containing prior-period
   reserve development. Read the development table in the 10-K rather than the ratio.
   Favourable development in consecutive years is the sector's most common source of
   flattering MLR. Route the accounting question to `sec-forensics` → edgar-forensics.
5. **Watch the policy calendar** through a reimbursement engine: the annual Advance Notice
   and Rate Announcement (February and April), risk-model changes, and RADV audit
   methodology. These reset the whole industry's economics at fixed dates.
6. **For vertically integrated names**, test whether margin is being shifted between the
   plan and the owned provider or pharmacy assets. Segment-level margin plus intersegment
   eliminations is where this shows; a consolidated MLR hides it entirely (SUB-SVC-03).
7. **For value-based care exposure**, identify the contract form — upside-only, two-sided
   risk, or full capitation — because the earnings quality differs completely between them
   (SUB-SVC-04).
8. Emit the brief.

## Not-automatic

Enrolment growth does not license a margin conclusion. Growth bought with benefit
richness is negative-margin growth, and the benefit design is in the plan filings, not
in the enrolment file.

Framework anchors: Kongstvedt, *Health Insurance and Managed Care*; MedPAC annual
reports; Porter and Teisberg, and Christensen, for the value-based-care framing.
Reference: `references/ma-mechanics.md`. Contract: `../../references/evidence-brief.md`.
