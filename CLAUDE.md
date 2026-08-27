# provider-economics — standing instructions

**Layers covered:** Financial + Commercial (services, payors, providers).
**Connector:** none hosted. Scripts call CMS bulk files and the ProPublica Nonprofit
Explorer API directly.

## What this engine is for

Reading the financial health of the *customers* — hospitals, health systems and health
plans — because in this sector the customer's margin is the supplier's demand.

Three distinct uses:

1. **Direct**, for listed hospital operators and managed-care names.
2. **Cross-read**, for medtech and tools names whose capital-equipment demand depends
   on hospital operating margin and capex capacity. This is the underrated one.
3. **Private-competitor benchmarking**, because most of the US hospital market is
   non-profit and files a 990 rather than a 10-K, so the open data covers the part of
   the market that no listed filer discloses.

## The lag problem, stated honestly

Nothing here is timely.

- **HCRIS** cost reports post four times a year (roughly mid-to-late January, April,
  July and October), but the underlying reports cover fiscal years that ended months
  earlier, arrive as-submitted, and are **restated** after audit. A two-year-old
  settled cost report and a six-month-old as-submitted one are different objects.
- **IRS 990** runs a year or more behind, and Schedule H (community benefit and
  charity care) requires parsing the full filing rather than the summary API.
- **MA enrolment** is monthly and timely; **Star Ratings** are annual (October) and
  determine bonus payments two years forward.

This engine therefore produces **structural** evidence — margin trajectory, payer mix,
capacity, capex headroom — not quarterly nowcasts. Say so in every brief, and never
let a cost-report finding be used to handicap a print.

## Chaining

a reimbursement engine → ma-bid-cycle and rule-cycle-calendar (rates drive everything
here) · a procedure-exposure engine → exposure-map (volume against the facility footprint) ·
a provider-adoption engine → provider-footprint (which facilities, which systems) ·
`sec-forensics` → edgar-forensics (compare the listed operator's reported margin to its
own facilities' cost reports — divergence is a finding) · your view layer.

## Anchored prompt-library IDs

SUB-SVC-01 (Hospital Operator Earnings Cross-Read) · SUB-SVC-03 (Vertical Integration
MLR Shifting) · SUB-SVC-04 (Value-Based Care Capitation Tracking).
## Connector

**Declares nothing at plugin level.** Two sources, both handled elsewhere:

- **CMS Coverage** (`hcls.mcp.claude.com/cms_coverage`) — NCD, LCD and coverage
  articles. Account-level, authless, one click in the directory, and currently **not
  connected on this desk**. Connect it: coverage determinations are what decide whether
  a service is paid for at all, which sits upstream of every margin question here.
- **CMS Socrata** — through the `medicare` server that `rx-utilization` anchors.

**HCRIS has no MCP and will not get one.** The cost report is a fixed-format worksheet
extract, not an API; `hcris_extract.py` plus `references/hcris-codemap.md` is the path.
Same for ProPublica 990s and MA enrollment. This plugin stays script-first and that is
the correct design, not a shortfall.

## Standard of evidence

This engine is built to **institutional investor standards: rigorous and auditable.**
That is a claim about specific mechanisms, and the full list is in
`references/auditability.md`. The load-bearing ones:

- Every finding carries a source, a retrieval date and the **vintage of the underlying
  data** — a different and usually much earlier date.
- Confidence is gated by vintage, not by conviction.
- Scripts fail loudly on empty result sets. Silence is never a negative finding.
- Known limitations travel with the number, in-line, not in a footnote.
- Evidence and view stay separated. This engine does not issue recommendations.

## Desk conventions (all engines)

- **One connector, one plugin — for plugin-level servers only.** A self-hosted
  stdio server is declared in exactly one plugin's `.mcp.json`; co-installed
  plugins share every server session-wide, so a second declaration buys a
  duplicate process, not extra capability. **Account-level hosted connectors are
  different**: CMS Coverage, PopHIVE, ClinicalTrials.gov, PubMed, ChEMBL,
  bioRxiv and Scholar Gateway are connected once in the directory and are visible
  to every plugin. Plugins reference those; they never declare or own them.
  Full map in `references/mcp-setup.md`.
- **MCP for the analyst, scripts for the watcher.** Both paths ship in every
  plugin and they are not redundant. Interactive query refinement goes through
  the server; unattended scheduled evidence goes through the script, because a
  watcher has to be deterministic and re-runnable against the same vintage.
  Where the two disagree, the script wins for anything entering a brief — you
  cannot cite the internals of a third-party server.
- **Engines produce evidence, not views.** An engine skill ends at the brief. The
  your view layer is the only place a position
  is argued. Do not write a recommendation into an engine output.
- **Open data only.** Every input here is free and public. If an analysis needs
  IQVIA, Symphony, Definitive, EvaluatePharma or Citeline, say so and stop — do
  not silently substitute a proxy for the paid panel and present it as equivalent.
- **Cite the vintage every time.** See `references/evidence-brief.md`.
- **Chain, don't duplicate.** These eight engines cross-reference each other by
  name. Anything outside them — valuation models, single-name research, the
  portfolio view layer — is chained into, never reimplemented here. An engine
  that starts doing valuation has stopped being an engine.
- **Scripts are stdlib-only Python 3.** No pip installs. Every script takes
  `--help`, prints JSON or CSV to stdout, and fails loudly on an empty result set
  rather than returning silence that reads like a negative finding.
