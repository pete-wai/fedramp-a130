# On behalf of government — research and implementation

Updated October 24, 2026. Publication to the existing GitHub repository and Pages site was authorized October 24, 2026. See validation.md for deployment evidence.

## Brief

Extend the existing A-130 site with a primary-source account of information handling and system operation on behalf of government. Test the tenant-only hypothesis rather than assume it. Explain where duties attach to agencies, services, information, components, and private counterparties. The central comparison is FISMA's information limb versus its system limb, followed by A-130 lifecycle language, CUI, and FedRAMP scope.

Read-mode design preserves the site's paper/ink identity. A persistent desktop contents list becomes a phone disclosure. Readers can filter history by authority and topic, compare five stated scenarios, search the evidence library, open exact source references, follow stable links, or print the complete report. All substantive content is HTML and remains available offline without JavaScript. Figma and AWS are hypothetical service-model illustrations, not vendor assessments.

## Authoring

- `scripts/behalf_content.py`: reviewed analysis, chronology, wording comparison, information flows, scenarios, and source locators.
- `scripts/behalf_build.py`: static HTML, complete print edition, JSON/CSV evidence, and claim-to-source map. Included in the normal build.
- `site/on-behalf/report.css` and `report.js`: responsive presentation and optional filters/navigation.
- `data/on-behalf/new-sources.json`: acquired-source metadata, SHA-256 hashes, and failed acquisition records. Only successfully acquired and cited sources enter the public evidence manifest.
- `data/on-behalf/archive-research.json`: Inforegs discovery/passages, retained as internal research evidence.
- `data/on-behalf/protected-baseline.json`: 451 existing source files protected from mutation.

The report cites 45 sources across 51 discussions, with 14 chronology entries and five examples. Existing source originals are linked in place; newly acquired originals and extracts are under `site/on-behalf/sources/`. Shared navigation was regenerated across the existing report, law explorer, and A-130 guide; existing statutory text and reader bodies remain unchanged.

Build: `uv run --locked python scripts/build.py`. Static checks: `mise exec -- pnpm test`. Preview: `mise exec -- pnpm preview`, then http://127.0.0.1:4176/on-behalf/index.html . Offline: open `site/on-behalf/index.html`.

## Research method and findings

Used the machine's Inforegs archive MCP for discovery and exact passages, then checked original documents and official publication records. Semantic indexing was incomplete, so archive retrieval was lexical. Source metadata does not by itself establish current law. Preserved PDFs, HTML/XML, extracts, publisher URLs, editions, retrieval dates, and hashes are distinct evidence fields.

The source-backed conclusion is that a tenant boundary can allocate implementation work but is not a general legal exemption. FISMA separately addresses information collected or maintained and systems used or operated. OMB's 1993 explanation distinguishes agency duties from contractor/grantee duties and points to agreements. NARA's 2016 CUI rule distinguishes outsourced processing from information received incidentally for other work. DHS's 2023 response expressly declines to treat that definition as the government-wide FISMA definition. NIST addresses external systems beyond direct control, separate authorizations, and inherited controls.

Current-publication review caught SP 800-18 Revision 2 (June 2026) replacing Revision 1 and SP 800-53 Release 5.2.0 (August 2025). The site preserves historical sources as historical sources. NIST publication is distinguished from contractual adoption.

## Limits and next research

- The existing law collection is OLRC release 119-118 through September 30, 2026. Added FOIA and records definitions use the 2024 Code; CUI uses the 2025 annual CFR. Live OLRC/eCFR retrieval failed during this task. Do not claim every legal amendment through October 24 was verified.
- The complete 2015 A-130 docket and a complete OMB response-to-comments account were not recovered. Selected EPIC and RAND comments are labeled as comments; chronology does not prove influence.
- The official current FedRAMP scope Markdown was retrieved from the program's public source repository after the rendered scope page returned no usable text. This is program guidance, not a statutory amendment.
- Civilian, unclassified focus. Not an exhaustive treatment of national security systems, DoD/CMMC, every agency supplement, or sector-specific confidentiality laws.
- No actual Figma/AWS contract, architecture, authorization, or private documentation was assessed. Agency-specific application needs those facts.

## Self-review

Research, implementation, and review occurred in this chat without subagents. A separate source/editorial pass corrected A-130 §6(a)(1), NARA Bulletin questions 6–8, and the DHS definition response at 88 FR 40571. The table labels condensed wording rather than implying every cell is a quotation. Source-page images checked included NIST's external-system discussion and the NARA/DHS boundary provisions. Source originals were not edited.

Visual review covered desktop and phone overview, wording comparison, a phone scenario, and representative print pages. The design detector produced heuristic warnings: it read the heading clamp as 4320px and body leading as 0.24; browser-computed checks confirm heading sizes at or below 70px and body line-height at least 1.5. Arial is retained for controls and metadata; prose uses Georgia. Repeated em dashes are predominantly source-reference separators and bibliographic titles. These are retained deliberately. The print root background was made white after review.

Completed checks and output locations are in `docs/validation.md`. This was self-review, not independent legal review.
