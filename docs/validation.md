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
