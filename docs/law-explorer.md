# Law and A-130 explorer

The new collection extends the historical report without changing its 178 records or protected source bodies. It contains the full codified text of Title 44 chapters 35 and 36, plus selected connected authorities: 100 sections altogether. The A-130 guide organizes the complete 2016 circular into 71 reading topics. All pages are committed static HTML, with local assets and no runtime fetches.

## Authoring and data

- `scripts/law_content.py` contains section explanations, precise clause annotations, law display names, and selected implementation-document relationships. `scripts/lineage.py` contains separately reviewed duty origins and dated changes. Do not infer a duty's first appearance from the current section's source credit.
- `scripts/a130_content.py` identifies topic boundaries in the preserved reader, assigns actors/topics, and explains the responsibilities. The guide copies source passages from that reader; it never edits it. Boundary markers are verified against the original sequence. Appendix I's body uses section 5 for its discussion despite the circular's contents-page numbering discrepancy; guide locators follow the body.
- `data/law/sections.json` lists the included sections. Section XML files are exact serializations from the preserved OLRC title archives; only outer trailing whitespace differs. The six title ZIP archives remain unchanged. `data/law/sources.json` records official URLs, editions, retrieval dates, and SHA-256 hashes.
- `scripts/law_build.py` generates section pages, complete chapter readers, history comparisons, the IG guide, the A-130 guide, and public JSON exports. The main build imports it after regenerating the existing report.

Public structured exports: `law/provisions.json`, `law/history-data.json`, `law/duty-lineage.json`, `law/changes.json`, `law/relationships.json`, `law/source-manifest.json`, and `a130/expectations.json`. Provision IDs derive from Code locators. Title 44 §3505 has two enacted subsections (c); the second uses `~2` internally and `occurrence-2` in its HTML anchor. The statutory numbering is unchanged.

## Historical and currency boundaries

The base is OLRC release 119-118, current through September 30, 2026, retrieved October 10. The interface labels that date prominently. The official classification service was under maintenance, Congress.gov direct retrieval returned 403, and its search cache had older bill status. The retrieved official presidential acts-approved list ended with Public Law 119-118. Enrolled texts of S.766 and H.R.5345 were also inspected: they do not amend the included Code sections, but an enrolled bill alone does not establish enactment. Do not claim a fully verified October 10 consolidation.

The history views compare collected annual Code editions and the current release. They preserve exact wording and identify the edition. They are not reconstructed legal text for every effective date between editions. Official amendment instructions, earlier-provision notes, and effective-date notes remain available in full on each section page. Selected duty histories have separately verified first-enactment and transition explanations. Other clauses must not be assigned an unverified earliest origin.

The two 2002 security tracks are distinct. Enactment date is not effective date: the Homeland Security Act's general effective date was 60 days after November 25, whereas the E-Government Act security title took effect on December 17. Earlier provisions may have different numbering. Same-number comparisons are labeled accordingly and do not establish semantic continuity by themselves.

For Title 5's IG recodification and Title 40's 2002 codification, consult the source/revision tables and predecessor legislation. Missing pre-codification readings are not evidence of a newly created duty. Source retrieval failures and requests for sections before their current numbering existed are logged in `data/law/retrieval-gaps.json`; this is a collection log, not a legal coverage verdict.

## Manual refresh

1. Select a new official release point and review its release date and relevant later enacted laws. Save an immutable new source version; never overwrite a reviewed original.
2. Use `scripts/collect_law.py --stage <directory outside the repo>` to reproduce the existing source manifest or investigate changes. It only writes into staging and reports changed hashes. It does not import or update sources.
3. For a new release, extract selected section XML from its official archive. Review changes, update the section/source manifest deliberately, and retain prior versions. Check uncodified notes, future-effective provisions, sunsets, renamed institutions, and changed cross-references.
4. Update authored annotations only after checking the cited provision and original amending law. Keep section enactments, duty origins, and policy implementation distinct.
5. Build and run the checks below. Publish only the reviewed, tested generated output. No refresh runs automatically.

## Validation

```sh
uv run --locked python scripts/build.py
mise exec -- pnpm test
uv run --locked python scripts/law-check.py
uv run --locked python scripts/editorial-check.py
mise exec -- pnpm preview
mise exec -- node scripts/law-browser-check.mjs
```

`pnpm test` runs the existing report checks and the Node law-page validator, including in GitHub Actions. The Python check verifies XML provenance, complete chapter coverage, rendered text fidelity, A-130 source sequence, precise annotation targets, source hashes, local links, and selected historical edge cases. Browser checks cover desktop/mobile, keyboard expansion, search/filter reset, comparisons, no JavaScript, offline reading, and print.

Review screenshots and the PDF in `output/law-*`. The review is an in-thread self-review; no independent legal reviewer or subagent was used. Source excerpts and statutory text remain separate from authored explanations. Typography-only comparison changes must not be described as substantive amendments.
