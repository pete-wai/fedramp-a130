# fedramp-a130

Read README.md and docs/handoff.md before editing. This is independent of fedramp-web; do not import from or modify sibling projects. No subagents unless explicitly requested by the user.

Keep the report buildless and usable through file://, with no network dependencies for reading. Keep primary-source originals immutable, preserve SHA-256 provenance and exact date/edition distinctions, and label missing originals, OCR problems and scope limits. Do not infer causation from chronology or treat every NIST publication as a binding requirement. Record explicit authority relationships and separate literal term hits from related terminology.

Edit scripts/content.py and data/records.json, rebuild with uv run --locked python scripts/build.py, and run mise exec -- pnpm test. For functional changes, run browser-check.mjs against the loopback preview. Verify mobile, keyboard and offline behavior. Update docs/handoff.md and docs/validation.md with actual checks. Research refreshes are manual. Publishing to this requested public repository/Pages site is authorized for this initial delivery; future scope follows the user's request.
