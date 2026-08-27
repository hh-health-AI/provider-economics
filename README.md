# provider-economics

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

Built to **institutional investor standards: rigorous and auditable.** That is a claim
about specific mechanisms, not a tone — the full list is in
`references/auditability.md`. In short: every finding carries a source, a retrieval
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
