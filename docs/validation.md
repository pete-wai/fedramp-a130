# Validation — October 10, 2026

Completed in this chat, as self-review:

- 178 records; 173 downloaded source files verified by SHA-256 and PDF signatures where applicable.
- 654 local links/anchors checked before the withdrawal-index addition; final exact count in output/static-check.json. Unique HTML IDs; no remote runtime scripts/styles.
- All six substantive update summaries are 294–313 words.
- Original 1985 Federal Register dating checked against the notice. The 1994 discovery candidate with the wrong FR document number was rejected and replaced with 94-18007. Exact 1994 notice HTML verified against the complete daily-issue scan. The scan exceeded GitHub's file limit and is not packaged; the original HTML is.
- 2000 main circular PDF and separate appendices retained distinctly. The April proposal is not labeled final.
- Six memo-heading dates corrected after extraction review; fiscal-year numbers are not used as issuance years. FedRAMP legislation locator corrected to §5921 and exact-term flags restricted to its subtitle, not unrelated omnibus provisions.
- Withdrawal/supersession distinctions added from NIST's archive index and original PDF archive covers. Original FIPS 46 edition withdrawal distinguished from final DES revision withdrawal.
- Chromium desktop (1440 px) and phone (390 px): rendering, no viewport overflow, empty search, combined type/term/era filters, sorting, reset, timeline selection, print styles and no JavaScript exceptions. Offline file:// with JavaScript disabled: all 178 records and six summaries present. See output/browser-check.json.
- Desktop and mobile screenshots visually inspected. Print layout exported and first page visually inspected (99 pages in the pre-withdrawal-index validation export). Original A-130 2016 cloud passage visually checked at PDF page 14. Additional flagged original pages rendered for inspection. Extracted-only flags remain labeled as such.
- Impeccable mechanical detector ran once. Its static scan reported heading line-height, font-choice and source-quotation wording warnings; some calculated font sizes were false positives from clamp parsing. Actual rendered headings and body text were reviewed. Source quotations were preserved; typography follows the user-pinned restrained report direction. No claim of zero detector warnings.

Limits: no independent legal review, screen-reader session, physical-device test, exhaustive OCR correction, or universal memorandum completeness claim. Browser tests used the existing Chrome installation. Tooling/browser failures during setup were corrected before the passing run.

Deployment verification is appended after GitHub Pages completes.

Final interaction pass: compact-table combined filters, newest-first sorting, table-to-record navigation, keyboard skip link and Enter activation, same-origin PDF download, and file:// JavaScript filtering passed. Offline report made zero HTTP requests; zero browser exceptions. The table navigation initially exposed a hash/visibility timing issue; revealing and scrolling the target record was fixed and the complete pass succeeded. Evidence: output/final-interaction-check.json and output/table-mobile.png. Direct file:// PDF links may open the browser viewer rather than emit a browser download event; the HTTP download behavior was verified separately.

Initial Pages runs 38057621457 and 38057629595 succeeded; public URL returned HTTP 200. Final UI revision deployment is verified in the delivery chat and output/live-check.json.

Final Pages publication: commit ff792fd, Actions run 38057785165, succeeded October 10, 2026. Live HTTPS bytes for index.html, app.js, styles.css, manifest.json, original 2016 PDF and original 1994 HTML match the local release hashes. The public phone-sized table → filtered FedRAMP results → detailed record journey passed. See output/live-check.json. Final static check: 835 local links/anchors, 173 original-file hashes, zero duplicate IDs.

## Responsive source-reader update — October 10, 2026
- 160 formatted PDF readers; source/anchor crawl and exact excerpt-boundary assertions pass.
- All 173 original SHA-256 hashes pass; raw extracts preserved.
- Reader checks pass at 1440px and 390px without JavaScript: no viewport overflow, page-index navigation, GitHub Pages subpath, file:// reading and return to source record.
- Existing report browser suite passes: search, combined filters, sorting, reset, timeline, print, no-JavaScript reading.
- Self-review of representative 1985 Federal Register and older NBS reader screenshots; readable measure, clear page links, conservative OCR warning. This was self-review, not a verified transcription of every source page.
- Pages deployment run 38059578187 succeeded for commit d89bcaa. Live 1985 reader HTML and reader CSS matched the tested local files byte-for-byte after deployment.

## Clear section headings — October 10, 2026
- Four heading regression tests cover mixed-case sections, inline headings, lettered subsections, wrapped questions, and rejection of page headers and prose references.
- Source hash, scoped-reader and all local anchor/link checks pass for 160 readers.
- Reader browser checks pass at 1440px and 390px, with JavaScript disabled, including keyboard activation of section links, page links, file:// navigation and no horizontal overflow.
- Existing report browser regression suite passes. Visually self-reviewed the 2016 reader's mobile heading/body hierarchy; captures saved as `output/reader-heading-*.png`.

## Narrative editorial revision — October 10, 2026

Rewrote the overview, prehistory, six revision summaries, responsibility comparisons, NIST histories, memorandum overview, methodology, and all 178 library descriptions. Added 36 numbered notes and three source quotations. Reader notices are shorter and collapsed under “About this text”; excerpt boundaries and source bodies are unchanged.

Completed checks:
- `scripts/editorial-check.py`: 506 protected source-file/source-body hashes unchanged (173 originals, 173 raw extracts, 160 reader bodies); all 178 descriptions populated; six summaries of 274–298 words; three quotations match source text.
- Original record IDs, dates, titles, types, relationships, URLs, locators, source paths, hashes, sizes, retrieval dates, term matches and reference passages compared with the pre-edit records and unchanged.
- Quotation image review: 1985 Federal Register printed page 52730/PDF 288; 1996 Federal Register printed page 6439/PDF 12; 2016 circular PDF page 3. The 1996 quotation is linked to the equivalent Appendix III definition in the original HTML copy.
- Static links, original hashes, and reader scope checks pass. Existing report and reader browser suites pass at 1440px and 390px.
- `scripts/notes-check.mjs`: all 36 note targets, keyboard note/backlink round trips, timeline uniqueness, stable relationship filtering, print visibility, mobile overflow, and file:// navigation without JavaScript pass.
- Visual self-review of the overview and 1985 summary on desktop/mobile. Separate editorial self-review removed generic descriptions, explained introductory acronyms, and corrected the descriptions of DATA Act memo M-17-04 and health/environment risk memo M-07-24. Historical source metadata and source passages were not rewritten.

Editorial review used existing source statements, authority/introductory sections, and the previously cited evidence. This is a prose and presentation revision, not a new source-collection pass or a determination that historical requirements remain in force. No independent reviewer was used.
- Live deployment 38061501486 succeeded for commit d76521b. Live index, stylesheet, script, source manifest, and 1985 reader matched local files byte-for-byte. The live mobile report showed all 178 descriptions and three quotations; footnote/backlink navigation and overflow checks passed. Evidence: `output/editorial-live-check.json`.

## Law explorer and A-130 responsibilities — October 10, 2026

- Full source-text comparison passed for 100 selected Code sections against the preserved official XML. Complete chapter 35/36 section sets verified. The A-130 source sequence covers the preserved reader from its introduction through the end of Appendix II without omissions or rewritten source text.
- New-page checks passed for 207 HTML pages, local files and fragment targets, unique IDs, source hashes, annotation locators, offline assets, duplicate §3505(c) handling, future FedRAMP repeal, DHS termination date, and the GISRA/FISMA evaluation predecessors.
- Desktop (1440px) and mobile (390px) browser checks passed: search, combined filters, empty/reset states, keyboard details, history selection, mobile overflow, file:// operation, no-JavaScript reading, and print. `output/law-browser-check.json` and `output/law-*.png` contain evidence. The IG print check produced a readable seven-page PDF with expanded context and sources.
- Existing report browser and footnote regression suites passed using installed Chrome. Protected-source verification confirmed all 506 original files/raw extracts/reader bodies unchanged and original source metadata unchanged.
- Separate editorial self-review corrected the optional independent-assessment wording in §3611, the §3555 reporting/protection subsection references, the scope of §3517, and the distinction between periodic testing under GISRA and the annual floor in 2002. Direct lineage and commentary keys are checked against actual Code locators.
- Visual self-review retained the existing paper/ink reading style, reduced mobile contents navigation to a disclosure, and corrected skipped heading levels in the new source displays. The Impeccable detector's display-size warning misread the clamp expression as 4000px; browser inspection confirmed the actual heading size. Its buzzword/em-dash warnings included unchanged source text and statutory headings, which were preserved. No independent reviewer or subagent was used.
- Currency: OLRC release 119-118 through September 30, retrieved October 10. The official presidential approved-acts list retrieved for the later-law check also ended September 30. Enrolled S.766/H.R.5345 texts were checked and do not amend included Code sections; their enrolled status alone was not treated as proof of enactment. The interface does not claim a fully verified October 10 consolidation.

- Published commit `10dddada2beb174a92edee54a8c5938603ea3fdb` through successful Pages workflow [38068750821](https://github.com/pete-wai/fedramp-a130/actions/runs/38068750821). All 13 representative live pages, assets, manifests, and source downloads matched tested local bytes; evidence: `output/law-live-check.json`. The browser suite also passed against the live Pages URL at desktop/mobile sizes, including search, filters, history comparisons, and source disclosures.

## Continuous law readings — October 10, 2026

The law index now leads with 12 subject readings covering all 100 collected sections exactly once. Full section text stays visible; substantive clause context and source/amendment notes open inline. Section pages and full chapters remain available. `scripts/reading_groups.py` owns grouping and introductory navigation copy; `scripts/law_build.py` reuses the existing section renderer. No research or law snapshot changed.

Verified with `pnpm test`, `scripts/editorial-check.py`, `scripts/reading-check.py`, the existing law browser suite, and `scripts/reading-browser-check.mjs`. Reading tests cover 1440, 768, 390, and 320px, subsection/section navigation, keyboard context expansion, inline source notes, no overflow, offline reading with and without JavaScript, and print styles. All 506 protected original files/source bodies remain unchanged; all 100 reading texts match their section pages. Visual self-review covered desktop and phone captures in `output/reading-*`. The design detector reported only a phrase in unchanged statutory text; it was preserved.

Published feature commit `c4eacb1` through successful Pages run `38071557817`. All 12 reading pages, the index, CSS, and JavaScript matched tested local bytes; live 390px contents navigation and overflow checks passed. Evidence: `output/reading-live-check.json`.

## On behalf of government — October 24, 2026 (local only)

Completed implementation and separate self-review. No deployment was performed.

- Normal build passed: 45 cited sources, 51 sourced discussions, five scenarios. Existing generated navigation links to the addition.
- `pnpm test` passed, including new `behalf-check.mjs`: 451 protected source-file hashes, all 45 cited source hashes, 1,085 new local links/anchors, unique IDs, scenario presence, source locators, no remote runtime assets, and expanded print disclosures. Existing 178 records, 160 readers, and 219 law pages also pass.
- `editorial-check.py` passed: all 506 protected original files/raw extracts/reader bodies unchanged. `law-check.py` passed for 100 sections, 240 sources, and 18,718 links.
- `behalf-browser-check.mjs` passed at 1440, 768, 390, and 320px: no viewport overflow, scenario selection, browser Back, source and history filters/reset/empty states, deep-link visibility, keyboard disclosures, and no JavaScript exceptions. Computed typography checks passed (heading no larger than 70px; body line-height at least 1.5).
- Offline file:// reading passed with JavaScript enabled and disabled. Skip-link keyboard behavior, 200% text size, complete print content, and the repository URL prefix passed.
- Existing history-report and law-explorer browser regression suites passed. Installed Chrome was used; no new browser/runtime dependency was added.
- Desktop/mobile screenshots were visually self-reviewed for the overview, wording comparison, and Figma scenario. Representative pages of the 48-page print edition were reviewed; the final print CSS uses a white root background. The print version expands all evidence and all five scenarios.
- Source-page review confirmed NARA's outsourced/incidental text at 81 FR 63341 and DHS's definition response at 88 FR 40571. The report's DHS locator was corrected. Other source/editorial corrections and limits are recorded in `docs/on-behalf.md`.
- One Impeccable detector pass produced 48 warnings, retained in `output/on-behalf/design-detector.json`. False numeric parses (4320px heading, 0.24 leading) were checked against computed browser styles. Arial is intentional for controls/metadata; Georgia is prose. Bibliographic separators and source titles account for repeated em dashes. No automated style changes were applied.
- `git diff --check` reports trailing whitespace within the existing minified historical index line that was regenerated for navigation. It is existing source-title whitespace; source text was preserved rather than rewritten to silence the warning.

Evidence: `output/on-behalf/static-check.json`, `browser-check.json`, responsive PNG captures, original-source page captures, and `report-print.pdf`. Authoring/research handoff: `docs/on-behalf.md`. Research gaps are visible in the report: incomplete 2015 comment docket, differing legal editions, incomplete later-law verification, and no actual vendor compliance review. The law snapshot and public-comment evidence must not be represented as exhaustive through October 24.

## Publication verified — October 24, 2026

Published report commit `eb2eaf0e71d87407e9e30b1a6a6340d422ebd72d` through successful Pages workflow [40095459639](https://github.com/pete-wai/fedramp-a130/actions/runs/40095459639). Live report: https://pete-wai.github.io/fedramp-a130/on-behalf/index.html . Eleven live files, including HTML, assets, evidence manifests, and two source PDFs, matched tested local hashes. Live desktop (1440px) and phone (390px) checks passed for overflow, scenario selection, public-comment filtering, and source deep links. Evidence: `output/on-behalf/live-check.json`; repeat with `mise exec -- node scripts/behalf-live-check.mjs`. This supersedes the earlier local-only delivery status.

## Quotation-led replacement — October 24, 2026

Replaced the on-behalf narrative with “Federal information in private services.” Completed checks:

- Normal build passed: 40 visible quotations, 42 cited sources, 45 retained source-library entries, 53 sourced discussions, nine comparison rows, and five scenarios. Old published anchors are preserved.
- `pnpm test` passed: 451 protected source-file hashes, 45 library source hashes, 1,405 report-local links and anchors, unique IDs, 40 quotation figures in both editions, and all existing site checks.
- `behalf-quotes-check.py` passed: all 40 quotes match bounded original PDF pages or original HTML/XML text; all are visible in both editions; the two 2014 FISMA clauses match the collected current Code. Evidence: `output/on-behalf/quotation-check.json`.
- `editorial-check.py` passed: all 506 protected files/source bodies unchanged. No source PDF, HTML, XML, raw extract, or existing statutory reader body was rewritten.
- Revised browser suite passed at 1440, 768, 390, and 320px, including visible quotations, no viewport overflow, filters/reset/empty states, scenarios and Back, source deep links, keyboard controls, and computed typography. Offline file:// with and without JavaScript, 200% text, print disclosure expansion, and the repository prefix passed.
- Existing historical-report and law-explorer browser suites passed after shared navigation changed.
- Visual self-review covered the mobile overview and duty quotations, desktop statutory excerpts and comparison, and representative printed pages. Print-only confirmation after keeping comparison rows together produced a 59-page complete edition. Final print captures use `revised-print-*`; earlier captures are historical evidence.
- Source/editorial self-review checked A-130 PDF 51 and NIST RMF PDF 133 visually, verified the original statute passages and CUI XML, corrected the Privacy Act locator to 88 Stat. 1904, retained the CUI exceptions, and corrected report-specific NIST/FIPS publication dates. The source library now identifies retained but uncited entries.
- One design-detector pass produced heuristic warnings for leading, small comparison notes, repeated em dashes, Arial, and the quotation rule. Comparison notes were enlarged. Browser-computed body leading is at least 1.5. Arial remains intentional for metadata; repeated reference separators and quoted punctuation remain; the left rule identifies block quotations. The print comparison uses 9pt text and 8pt citations. No automatic style changes were applied.

Research checks: official NIST publication pages confirmed the cited revisions. The official current OLRC endpoint returned an error; current-law consolidation beyond the preserved editions is not claimed. The existing incomplete 2015 comment-docket limitation remains visible. This was source/editorial and visual self-review, not independent legal review.

Publication was explicitly requested. The following deployment entry records the actual delivered commit and live checks.

## Revised report published and verified — October 24, 2026

Published commit `63a6a3f8a6165b760922099e86d386d2c442986c` through successful Pages workflow [40097651531](https://github.com/pete-wai/fedramp-a130/actions/runs/40097651531). Live replacement: https://pete-wai.github.io/fedramp-a130/on-behalf/index.html . Twelve live files—including both editions, CSS/JS, source/claim/quotation exports, navigation entry points, and two original PDFs—matched local hashes. Live desktop and phone checks verified the new title, all 40 visible quotations, no overflow, scenario selection, public-comment filtering, and source deep links. Evidence: `output/on-behalf/live-check.json`. The earlier on-behalf report has been replaced at its existing URL.
