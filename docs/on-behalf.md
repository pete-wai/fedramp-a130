# Federal information in private services

Revised October 24, 2026. Replaces the earlier “On behalf of government” narrative at the same public `/on-behalf/` URL. Publication is authorized; the handoff and validation log record actual deployment evidence.

## Purpose and conclusions

The user requested a quotation-led comparison of FISMA’s information and system duties, especially when an agency buys access to a commercially operated service rather than commissioning operation of an agency application. Ordinary federal information comes first. CUI, contract information, privacy, and records are separate additional triggers.

The report separates statutory classification, operational control, information stewardship, and authorization. It shows the federal authorizing official requirement without assuming that an authorization to use gives the government operational control of a provider. It also explains why private operation alone does not establish exclusion from the statutory “used or operated” clause.

A-130 Appendix I §4(j) supplies the central duty-by-duty analysis: information agreements; the alternative collection/maintenance trigger; access oversight; effective controls; inventory; interfaces; and incident procedures. The comparison names where duties overlap rather than inventing a universal lighter baseline for all externally held information. The CUI prohibition on treating qualifying nonfederal systems as agency systems is quoted with its outsourcing context and exceptions. SP 800-171’s information-on-behalf exclusion is also quoted directly.

## Content and authoring

- `scripts/behalf_analysis.py`: principal analysis, roles, duties, nine-row comparison, and additional information-specific regimes.
- `scripts/behalf_content.py`: supporting chronology, lifecycle, five examples, and coverage limits. The first three examples address SaaS access, IaaS workloads, and commissioned application operation; two contrasting examples cover incidental handling and internet transit.
- `data/on-behalf/quotations.json`: 40 exact excerpts, original-file references, PDF pages where applicable, source IDs, and locators. All 40 appear directly in both the main report and print edition.
- `scripts/behalf_build.py`: static renderer and evidence exports; normal `scripts/build.py` includes it. Runtime assets remain in `site/on-behalf/`.
- `data/on-behalf/retained-sources.json` and `prior-anchors.json`: snapshots supporting stable incoming links from the earlier edition. They are build inputs; the build does not depend on its previous output.

The replacement cites 42 sources in 53 discussions. The library retains 45 entries for stable source links; uncited retained entries are identified. Historical raw source metadata and all original bytes are unchanged. This report corrects three display dates using NIST publication history or the FIPS announcement: SP 800-37r2 December 20, 2018; SP 800-171r3 May 14, 2024; FIPS 200 March 9, 2006. FIPS 199/200 are labeled mandatory standards, not generic guidance.

## Quotation and research method

Inforegs discovery and exact-passage retrieval supplied the A-130 non-Federal-entity provisions and other source leads. The published excerpts were checked against preserved originals, not search-result summaries. Automated checking extracts only the specified PDF pages or original HTML/XML text and verifies each quotation. Normalization is limited to whitespace, punctuation spacing introduced by HTML extraction, and PDF line-end hyphenation; compound agency-/non-/organization- is preserved. No explanatory paraphrase appears inside quotation blocks. Both FISMA clauses also match the collected current Code.

A separate source/editorial self-review checked the original A-130 PDF page 51, NIST SP 800-37 PDF page 133, and the statute/other bounded passages; it corrected the Privacy Act printed locator to 88 Stat. 1904 and retained the CUI exceptions. No subagent or independent legal reviewer was used.

Official NIST publication pages for SP 800-37r2 and SP 800-171r3 were rechecked during this revision. Current OLRC retrieval returned an error, so the report retains the explicit legal-edition limits. The earlier check of SP 800-18r2 and SP 800-53 Release 5.2.0 remains part of the retained source history; NIST publication does not automatically update contract incorporation.

## Checks and preview

```sh
uv run --locked python scripts/build.py
mise exec -- pnpm test
uv run --locked python scripts/behalf-quotes-check.py
uv run --locked python scripts/editorial-check.py
mise exec -- pnpm preview
mise exec -- node scripts/behalf-browser-check.mjs
```

Preview: http://127.0.0.1:4176/on-behalf/index.html . Offline: open `site/on-behalf/index.html`. After publication: `mise exec -- node scripts/behalf-live-check.mjs`.

Static checks cover 1,405 local links/anchors, 451 protected original source files, the source hashes, and 40 visible quotations. The separate original-reader check protects 506 files/source bodies. Browser coverage includes 1440/768/390/320px, filtering, scenario selection, Back, keyboard controls, source links, offline use with and without JavaScript, text enlargement, and print. Existing report and law-browser regressions also passed. Current evidence is under `output/on-behalf/`; deployment evidence is recorded in `docs/validation.md`.

## Remaining limits

The Code collection is OLRC release 119-118 through September 30, 2026. Additional FOIA and records provisions use the 2024 Code; CUI uses the 2025 annual CFR. Later legal changes through October 24 are not fully verified. The complete 2015 A-130 comment docket was not recovered. Selected comments are not treated as adopted policy or evidence of causation.

The report concerns civilian, unclassified information and does not comprehensively cover DoD/CMMC, national security systems, sector-specific secrecy laws, or every agency supplement. Named vendors are hypothetical examples, not findings about actual contracts, offerings, or compliance. There is no categorical legal conclusion that every commercially sold service is nonfederal or that every such service is federal.
