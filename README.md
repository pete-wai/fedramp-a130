# A-130: history and authority

[Read the report](https://pete-wai.github.io/fedramp-a130/).

A buildless, primary-source research site tracing OMB Circular A-130, federal computer-security legislation, NIST standards and guidance, and cloud/FedRAMP policy through October 10, 2026.

Open `site/index.html` directly for offline reading, or use `mise exec -- pnpm preview` and visit http://127.0.0.1:4176/. Original-source links need the internet; local downloads and report interactions do not. No backend, analytics, external fonts or runtime network dependencies.

The report includes six approximately 300-word revision summaries, an aligned chronology, qualitative authority analysis, NIST publication lineages, a searchable inventory with combined filters and sorting, original files, term passages and downloadable JSON/CSV provenance manifests. The complete narrative works without JavaScript.

## Current-law and A-130 guides

- [Read the law](https://pete-wai.github.io/fedramp-a130/law/index.html): full Title 44 chapters 35 and 36 and connected authorities, with 100 section explanations and 2,819 indexed provisions.
- [A-130 responsibilities](https://pete-wai.github.io/fedramp-a130/a130/index.html): 71 topics covering the complete 2016 circular and both appendices, with source passages and statutory connections.
- [History comparisons](https://pete-wai.github.io/fedramp-a130/law/history.html): dated Code editions, original amendment notes, and reviewed origins of selected duties.
- [IGs and oversight](https://pete-wai.github.io/fedramp-a130/law/oversight.html): annual evaluations, management testing, reporting, and the roles of OMB, CIGIE, and GAO.

The law collection uses OLRC release 119-118, through September 30, 2026, retrieved October 10. It has a separate source manifest with 240 preserved files. Comparisons show collected editions rather than every intervening effective date. See [authoring, update procedures, and coverage boundaries](docs/law-explorer.md).

## Sources and coverage

The library includes 178 records and 173 downloaded documents. It covers major A-130 revisions, related laws, selected NIST publications, and OMB memoranda through October 10, 2026. Source notes identify editions, known replacements, and gaps in the collection.

Four standalone originals are unavailable: A-71’s 1978 security transmittal, OMB Bulletins 88-16 and 90-08, and the first edition of FIPS 201. Later government documents describe their history. The 1965 A-71 appears as a reproduction in FIPS 12.

Reading excerpts omit unrelated material in Federal Register issues and omnibus laws. The original PDFs remain available. The 1994 A-130 notice is supplied as original GovInfo HTML. Searchable text from older scans may contain transcription errors.

The memorandum search covered six official indexes, with 721 distinct candidates and 717 retrieved documents. It found 89 documents containing A-130 references; the library also includes selected related policies. Details of the search and source coverage are available in the report’s notes and source index.

## Editorial approach

The narrative is written for general readers, with short historical accounts, explanations of technical terms, and source quotations. Archival details appear in numbered notes or source details. See [the editorial guide](docs/editorial-guide.md) for the writing method and examples.

Original files, raw extracts, and the document text in formatted readers are unchanged by the editorial revision. Automated checks protect these materials and the source metadata.

## Authoring and checks

Runtime pins: Node 24.21.0, pnpm 12.6.0, Python 3.13.7. Inspect `mise.toml`, then trust this checkout with mise if required.

```sh
uv sync --locked
uv run --locked python scripts/build.py
mise exec -- pnpm install --frozen-lockfile
mise exec -- pnpm test
uv run --locked python scripts/editorial-check.py
mise exec -- pnpm preview
```

In another terminal, with the preview running:

```sh
mise exec -- pnpm exec playwright install chromium
mise exec -- node scripts/browser-check.mjs
```

On the dedicated Mac, the existing browser may be used with `CHROME_PATH='/Users/codex/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' mise exec -- node scripts/browser-check.mjs`. Browser checks create `output/` evidence. No browser is required to run static link/hash checks.

Edit structured paragraphs, quotations, and editorial notes in `scripts/content.py`, the page assembly in `scripts/build.py`, reviewed evidence in `data/records.json`, and UI assets in `site/`. After changing evidence, synchronize `site/manifest.json` from `data/records.json` and rebuild. Source bytes and recorded hashes must agree. `collect.py` and `memos.py` are manual research helpers, not build steps: fetch into a separate staging checkout, verify identity and scope, then merge reviewed records. Never replace reviewed evidence blindly with extraction output. Raw discovery indexes and candidate metadata are preserved in `data/`.

GitHub Actions checks local links and source hashes, then publishes the committed `site/` to GitHub Pages. No research refresh runs automatically. The revised plan is in `docs/plan.md`; the user's original plan is preserved separately.

## Source rights

Government-origin materials are preserved for research with source URLs and hashes. Third-party material embedded in government publications may have separate rights. No license is asserted over third-party source content.
