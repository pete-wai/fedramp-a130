# A-130: history and authority

[Read the report](https://pete-wai.github.io/fedramp-a130/).

A buildless, primary-source research site tracing OMB Circular A-130, federal computer-security legislation, NIST standards and guidance, and cloud/FedRAMP policy through October 10, 2026.

Open `site/index.html` directly for offline reading, or use `mise exec -- pnpm preview` and visit http://127.0.0.1:4176/. Original-source links need the internet; local downloads and report interactions do not. No backend, analytics, external fonts or runtime network dependencies.

The report includes six approximately 300-word revision summaries, an aligned chronology, qualitative authority analysis, NIST publication lineages, a searchable inventory with combined filters and sorting, original files, term passages and downloadable JSON/CSV provenance manifests. The complete narrative works without JavaScript.

## Research boundaries

178 records, including 173 downloaded source documents, plus explicitly identified recovery gaps. The memorandum discovery pass searched six official indexes: 721 distinct candidates, 717 successful downloads and 89 extracted direct A-130 matches. Additional policy extensions are included. This is a bounded historical inventory, not an exhaustive current-law checklist.

Missing standalone originals: A-71's 1978 security transmittal and OMB Bulletins 88-16 and 90-08. The original FIPS 201 download also remains unresolved. A-71 (1965) is reproduced within the preserved FIPS 12. Selected NIST editions and documented withdrawals are included; every revision/erratum is not. Extracted term flags identify literal occurrences, which can be in a title, footnote or glossary rather than an operative requirement. Related terminology is separately labeled. See the report's methodology for limits.

The 1985 circular is in the preserved whole Federal Register issue, PDF pages 288–309. The 1994 notice is original GovInfo HTML. The complete 1994 daily-issue scan was downloaded and inspected but is retained only in the local research cache because it exceeds GitHub's per-file limit. No reconstructed PDF is represented as an original.

## Authoring and checks

Runtime pins: Node 24.21.0, pnpm 12.6.0, Python 3.13.7. Inspect `mise.toml`, then trust this checkout with mise if required.

```sh
uv sync --locked
uv run --locked python scripts/build.py
mise exec -- pnpm install --frozen-lockfile
mise exec -- pnpm test
mise exec -- pnpm preview
```

In another terminal, with the preview running:

```sh
mise exec -- pnpm exec playwright install chromium
mise exec -- node scripts/browser-check.mjs
```

On the dedicated Mac, the existing browser may be used with `CHROME_PATH='/Users/codex/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' mise exec -- node scripts/browser-check.mjs`. Browser checks create `output/` evidence. No browser is required to run static link/hash checks.

Edit narrative in `scripts/content.py`, the page assembly in `scripts/build.py`, reviewed evidence in `data/records.json`, and UI assets in `site/`. After changing evidence, synchronize `site/manifest.json` from `data/records.json` and rebuild. Source bytes and recorded hashes must agree. `collect.py` and `memos.py` are manual research helpers, not build steps: fetch into a separate staging checkout, verify identity and scope, then merge reviewed records. Never replace reviewed evidence blindly with extraction output. Raw discovery indexes and candidate metadata are preserved in `data/`.

GitHub Actions checks local links and source hashes, then publishes the committed `site/` to GitHub Pages. No research refresh runs automatically. The revised plan is in `docs/plan.md`; the user's original plan is preserved separately.

## Source rights

Government-origin materials are preserved for research with source URLs and hashes. Third-party material embedded in government publications may have separate rights. No license is asserted over third-party source content.
