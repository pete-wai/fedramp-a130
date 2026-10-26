# Protecting federal information and systems

Replaced October 25, 2026 at the existing `/on-behalf/index.html` URL. This is the chronological replacement requested by the user, not the earlier scenario report. Publication to the existing repository and GitHub Pages is explicitly authorized. Actual deployment evidence is recorded in handoff.md and validation.md.

## Delivered scope

41 milestones, 80 visible direct quotations, 45 quoted sources, and 72 retained library sources. The main history spans 2000–2026, with PRA, Computer Security Act, and earlier A-130 foundations. Each milestone identifies its authority, origin, what changed or carried forward, quoted text, exact locations, and edition caveats. Thirteen explicit authority relationships distinguish requirements, implementation, incorporation, citations, derivation, and related context.

The report traces FISMA’s information and system clauses from 2002 to 2014; the direct statutory tasks for NIST and Commerce; FIPS 199 and 200; SP 800-60; RMF and control catalog revisions; OMB’s early incidental-equipment instructions; cloud and FedRAMP policy; A-130 2016’s contract and alternative oversight triggers; the CUI rule and SP 800-171 editions; information stewardship and exchange guidance; and SP 800-18 Revision 2 in 2026. Government public-comment responses are distinguished from operative rules.

All authored vendor/contractor scenarios were removed. Statutory or source references to contractors remain necessary evidence. The current-responsibility comparison stacks on phones. All quotation text is visible without disclosure clicks. Filters are optional enhancements; citations reveal filtered-out targets. The complete report works without JavaScript and through file:// offline. Print has all provenance disclosures open. Old source links and both previous editions’ fragment IDs remain available as aliases to related new sections.

## Authoring

- `scripts/history_content.py`: eras, milestone explanations, relationships, current comparison, coverage ledger.
- `data/on-behalf/history-quotations.json`: reviewed excerpts, source file, PDF pages, and locators.
- `scripts/history_quote_selection.py`: manual, deterministic selection boundaries in preserved originals; not a build-time research step.
- `scripts/history_sources.py`: source registry combining existing records and preserved acquisitions; presentation edition corrections do not modify originals.
- `scripts/behalf_build.py`: static renderer and JSON/CSV exports, included by the normal build.
- `site/on-behalf/report.css` and `report.js`: responsive typography, authority labels, filters, hash navigation, and print behavior.
- `data/on-behalf/history-acquisitions.json`, `history-60-acquisitions.json`, `history-web-sources.json`, and `history-research-log.json`: discovery and preservation records.
- `prior-anchors.json`, `replacement-anchors.json`, the old `quotations.json`, and `retained-sources.json`: stable-link inputs. Earlier `behalf_analysis.py` and `behalf_content.py` remain historical authoring files but are no longer imported by the build.

## Research and accuracy

Used the local Inforegs MCP archive for discovery, exact passage retrieval, metadata, and original documents, supplemented by official NIST, OMB, and government source pages. Copied archive files only after verifying SHA-256 identity. The semantic index was complete at the checked generation; this does not establish exhaustive historical coverage. Original-page text, not generated archive conclusions, supplies the published quotations.

The source checker matches every quote to its bounded original pages or saved HTML, and checks presence in both web editions. It separately verifies identical text across FISMA 2002/2014, SA-9 Revisions 1/2, and the 2010/2014 RMF excerpt. The two FISMA clauses also match the collected current Code. A separate self-review checked statutory sections, complete adjacent passages, footnotes, applicability exceptions, edition covers, and selected page images. It corrected the FISMA section allocation: §302 is Commerce/40 USC 11331; §303 is NIST. It also corrected printed locators in SP 800-18r1 and SP 800-53r1. OMB’s 2004 guidance quote includes its flexibility and stricter-policy qualifications.

Normalization only reflows whitespace, punctuation spacing, and line-end hyphenation. Clause breaks in HTML do not change text. Footnote markers remain; some PDF extraction places footnote text inline, so original page links are supplied. NIST’s 2024 comment-analysis PDF has a defective text layer; its original is retained as a reference but no corrupted extraction is presented as a quotation.

The existing original collection is unchanged. Publication dates are distinguished from updated files: 800-53r3 includes August 2010 updates; r4 January 2015; r5 December 2020; 800-171 original January 2016; r1 June 2018; r2 January 2021. The separate 2010 original and June 2014 RMF files permit an actual continuity comparison. The 2025 800-53 change list was checked in full and does not change SA-9.

## Coverage limits

Current-code comparison remains the collected OLRC 119-118 edition through September 30, 2026. No exhaustive later-October amendment check is claimed. The official NIST pages for 800-37r2, 800-171r3, and 800-18r2 and the OMB circular index were rechecked October 25. The 2025 800-53 release explanation/change list was also checked. Intermediate maintenance releases, every annual OMB instruction, all agency acquisition rules, and the complete 2015 A-130 comment docket are not reconstructed. The report includes a visible family-by-family coverage ledger and exports it as JSON.

Research, editorial review, visual review, and testing were performed in this chat. Self-review only; no independent legal review.

## Reproduce checks

```sh
uv run --locked python scripts/build.py
mise exec -- pnpm test
uv run --locked python scripts/behalf-quotes-check.py
uv run --locked python scripts/editorial-check.py
mise exec -- pnpm preview
mise exec -- node scripts/behalf-browser-check.mjs
```

Preview: http://127.0.0.1:4176/on-behalf/index.html . Confirm the listener rather than using a remembered PID. Browser suite uses installed Chrome and covers 1440, 768, 390, and 320px, filters and empty states, citation-target reveal, old URLs, keyboard, 200% text, offline JS on/off, print, and the Pages prefix. Evidence base: `output/on-behalf/history-*`; original-page images use `original-*`. Static and quotation check reports retain their stable filenames. After deployment, run `mise exec -- node scripts/behalf-live-check.mjs`.
