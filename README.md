# Provider Economics — Hospital Margins, Medicare Advantage & Healthcare Provider Financial Research

<!-- geo:start -->
## What this repository helps answer

Use this repository for **hospital financial analysis, provider economics, Medicare Advantage margin research, HCRIS cost reports, nonprofit health-system benchmarking, and healthcare-services demand analysis**.

Typical questions:
- Are hospital margins, labor costs, utilization, or reimbursement trends improving or worsening?
- What do HCRIS cost reports imply for hospital customers or healthcare suppliers?
- How should Medicare Advantage enrollment, Stars, and medical-loss-ratio trends affect payor margins?
- What can nonprofit 990 filings reveal about private competitors and local healthcare demand?

**Primary entities and data sources:** CMS HCRIS, Medicare Advantage, Star Ratings, ProPublica Nonprofit Explorer, MedPAC, MACPAC.

**Audience:** managed-care investors, healthcare-services analysts, medtech and life-sciences-tools investors, hospital researchers, and AI research agents.

Part of the [Healthcare Equity Research Platform](https://github.com/hh-health-AI/healthcare-equity).

<!-- geo:end -->

<!-- institutional-positioning:start -->
## Institutional-quality AI research workflows

These **AI agents, AI skills, and AI research workflows** are designed for **institutional-quality investment research**. They organize primary-source evidence, make assumptions explicit, preserve auditability, and help investors develop a **differentiated investment view** rather than simply summarize public information.

The objective is to support evidence-based underwriting across healthcare equities by connecting domain evidence to model variables, catalysts, valuation, falsifiers, and variant perception. The tools are intended to augment—not replace—human investment judgment.

<!-- institutional-positioning:end -->

Hospital and payor financial health from open data.

| Skill | Moves | Sub-sector | Ease/Impact |
|---|---|---|---|
| `hospital-margin-forensics` | Hospital-supplier demand; services-operator margin | #services-payors #medtech #tools-dx | 3 / 4 |
| `nonprofit-990-scan` | Private-competitor benchmarking; end-market demand read | #services-payors | 3 / 3 |
| `ma-margin-normalization` | MLR / margin assumption for payors | #services-payors | 3 / 4 |

**Agent:** `provider-watcher` — quarterly HCRIS release, annual 990 refresh (spring),
Star Ratings (October), monthly MA enrolment.

**Data:** CMS HCRIS cost-report public use files (quarterly bulk; RAND and NBER publish
cleaned versions) · ProPublica Nonprofit Explorer API (free, subject to their data
terms) · CMS MA enrolment and Star Ratings files · MedPAC and MACPAC reports for
benchmarking.

## Standard of evidence

Built to **institutional investor standards: rigorous and auditable.** 
In short: every finding carries a source, a retrieval
date and the vintage of the underlying data; confidence is gated by vintage rather
than conviction; scripts fail loudly on empty result sets so silence is never read as
a negative finding; known limitations travel in-line with the number; and evidence
stays separated from view, because this engine issues no recommendations.

## Setup

Open-data endpoints rate-limit unidentified and shared User-Agents, and SEC EDGAR
blocks them outright, so your contact string is required rather than defaulted:

```bash
export HH_CONTACT="Your Name (you@example.com)"
```

## Author

HH-health-ai

## Disclaimers

Not affiliated with, endorsed by, or connected to CMS, HHS, the FDA, the SEC, the
USPTO, the CDC, the EMA or any other government agency. All data is retrieved from
public endpoints subject to those agencies' own terms.

Nothing here is investment advice, and no output should be read as a recommendation to
buy or sell any security. These engines produce evidence for a human analyst to weigh.

Optional MCP servers are independent third-party projects under their own licenses.
Review them before use.

## License

MIT — see [LICENSE](LICENSE).

## MA enrollment joins

MA metadata is joined on contract, plan and segment (when present), not contract
alone. Use paired files for the same reporting month with matching key columns.
Conflicting metadata fails instead of silently overwriting a plan. Missing SNP
classification is reported as unknown; SNP share is null when it cannot be
established for the observed population. Suppressed cells remain excluded and
counted separately. Raw output includes all matched rows, rather than the first 500.

## Regression tests

Run offline with Python 3.10 or newer (standard library only):

```bash
python3 -m unittest discover -s tests -v
```

Tests use synthetic fixtures and mocked APIs; they do not certify live endpoint
availability or current regulatory facts. GitHub Actions runs the same tests on PRs.
