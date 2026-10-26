# Proposed FedRAMP use workbook

Requested October 26, 2026. Add `/proposed-fedramp-use/` without replacing the historical report. User authorizes publishing to the existing GitHub Pages site. No subagents.

## Direction contract

THESIS: Explain an agency workflow through primary quotations and decision records. The report distinguishes provider assurance from agency risk acceptance and connects their monitoring.

OWN-WORLD: Extend the existing cream, ink, blue, Georgia/Arial research interface. Thin authority-colored quote borders; amber concerns with explicit text labels. No decorative imagery or external runtime assets.

STORY: Read the premise, compare the original six steps, examine authority, then complete eight practical records. Readers can inspect sources without abandoning their place.

FIRST VIEWPORT: Compact research-site navigation, proposal label, plain heading, short premise, and links to review or workbook. Desktop contents rail; native mobile contents disclosure.

FORM: Existing report extension with a working form beside the relevant evidence. No new visual world or randomized layout. Narrative remains in static HTML. Browser storage is opt-in; JSON and Markdown exports are local.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Research method

Inforegs archive generation `1792925048-9046:vectors-631348-1792925274499112000` was available with complete indexed corpus and semantic index. Exact NIST ATU passage retrieved: `d00c596c20bc8716c52538c7070723f97b5218a8f0c27e09127686fe3f2ce7fe`, with neighbors including footnote 142. Broader search initially returned irrelevant oversight reports; these were not used as support. Quotes were selected and verified against retained primary PDF originals, not search excerpts.

FedRAMP MCP snapshot had October 13 rules/Markdown and October 20 community data. Some agency rules carried `placeholder` metadata. Current official pages were therefore fetched directly on October 26, preserved as original HTML plus extracted article text and SHA-256 hashes. The live Agency Use page identifies the rules as required, effective July 4, 2026. The report distinguishes that published status from stale MCP metadata. No community statements are used as requirements.

Current NIST landing pages confirm SP 800-37 Rev. 2 and SP 800-53 Rev. 5 with Release 5.2.0 planning note. SA-9 text and SA-4 control statement used here are unaffected by that release; SA-4 discussion was changed, so it is not quoted as current text. Current law cross-check uses the site's retained OLRC collection; legal currency is disclosed rather than claiming a comprehensive October 26 statutory update.

## Implementation and checks

Completed checks and self-review are recorded below.

### Completed implementation

- Authoring: `scripts/use_content.py`, `scripts/use_build.py`, and the explicitly run `scripts/use_quote_selection.py`. Normal builds render the fixed quote bank without reselection or network requests.
- Runtime: `site/proposed-fedramp-use/index.html`, `report.css`, and `workbook.js`. Eighteen fields across eight steps; opt-in storage; validated JSON import; JSON and Markdown exports; report or workbook printing. One worksheet per agency use/service, with related records linked by the user.
- Evidence: 41 displayed quotations from 14 retained source records (including the linked scope reference), five captured official program pages, nine statutory clauses checked against retained current Code. Whitespace and line-end normalization only.
- Navigation: report linked from the site homepage and both editions of the information/system history. That report's body and all original-source files are preserved.

### Self-review and completed checks

Completed in the current chat, without subagents or independent legal review. The separate self-review checked the proposal against statutory process authority, retained agency FISMA duties, presumption of adequacy, scope, SA-9, the older ATU prerequisites, and current FedRAMP ATO language. Added an explicit warning against inventing certification-class/FIPS equivalence. A separate service-use record remains a proposal, not a newly established authorization category.

- Normal full build succeeded. `mise exec -- pnpm test` passes all site/source/link checks, including the new workbook.
- `scripts/use-quotes-check.py` passes 41 original-matched and rendered quotations, 14 source hashes, five article extractions, and nine current-Code clause checks. `scripts/editorial-check.py` passes 506 protected files/source bodies.
- Browser checks pass at 1440, 768, 390, and 320 px; no viewport overflow or JavaScript errors. All 41 quotes and 18 fields present; keyboard toggle and skip link; citation target revealed from workbook-only mode; 200% text sizing; Pages prefix route.
- Session-only default, opt-in save/restore, storage removal, JSON round trip, Markdown export, invalid JSON/version/unknown-field rejection without losing answers, clearing, and blocked-storage fallback pass. Imported markup is retained as text.
- Offline `file://` reading passes with JavaScript on and off. No runtime fetch is required.
- Full-report print: 31 pages with test answers. Workbook-only print: seven pages. The final line of a long test answer is present in each PDF. Rendered first report page and long-answer workbook page visually inspected; no clipping found.
- Screenshots and reports: `output/proposed-fedramp-use/`. Visually inspected desktop/390px headers, phone evidence and fields, and print captures. Detector ran once: 32 repeated border-accent findings and one Arial finding; retained as intentional source/concern distinction and established interface typography.
- Initial checks caught a duplicate section ID and two test timing/expectation issues (asynchronous import and deliberately unchecked unavailable storage). Fixed; the passing browser result is the final evidence.

Limitations: browser emulation rather than a physical phone or screen-reader session; no independent legal opinion; no blanket assertion of current law beyond the disclosed Code snapshot. The workbook is not an official FedRAMP submission tool or signed authorization. Publication verification will be appended after deployment.
