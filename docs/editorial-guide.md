# Writing the A-130 history

Audience: general readers. Format: a short historical narrative supported by source notes. Write about the events and their consequences; leave the research process in the notes.

## Editorial foundation

- [National Archives: plain-language principles](https://www.archives.gov/open/plain-writing/10-principles.html): lead with the point, use familiar words, explain technical terms, and keep each paragraph on one subject.
- [GOV.UK: clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/): explain specialist language and use concrete actors and actions.
- [Office of the Historian: documentary editing](https://history.state.gov/historicaldocuments/frus1969-76v21/preface): use annotations for documentary context, omitted material, and related sources.

These guides inform the editorial method. They do not supply the report's historical claims.

## Working rules

Begin with what changed and why. Continue with the responsible agencies, relevant laws, and practical effect. Use dates where the sequence matters; put publication-versus-effective-date detail in notes when it interrupts the explanation. Define agencies and necessary technical terms on first use. Keep the six revision summaries approximately 250–350 words, without imposing identical paragraph templates.

Prefer “Congress assigned NIST…” or “OMB required agencies…” to abstract claims about frameworks and lineages. Explain real relationships affirmatively. Do not introduce an imaginary mistaken reading just to refute it. Avoid repeated instructions to the reader, self-references, boilerplate caveats, and descriptions of collection mechanics in the narrative.

Quotes should illuminate a policy change. Check them against the original image or original HTML and identify the edition and page/section. Never polish a quotation to match the narrative voice. Preserve meaningful uncertainty next to the affected claim; put file availability and archival detail in footnotes or source details. Do not turn unknown applicability into a claim that a policy is current.

Write one useful description for every library record. Repeated annual reporting documents may have similar descriptions, but must identify the correct reporting period and subject. A title mentioning “reporting” is not enough to classify a document as security reporting: M-17-04 concerns DATA Act spending reports.

## Examples from this revision

Before: “Because A-71 predates that enactment, the original A-71 cannot be described as a response to the enacted Brooks Act.”

After: “In March 1965, the Bureau of the Budget, OMB’s predecessor, issued Circular A-71 to divide those responsibilities among agencies, the General Services Administration, and the Department of Commerce. The Brooks Act followed in October.”

Before: “Original whole Federal Register issue preserved.”

Source detail: “The PDF contains the full Federal Register issue. A-130 occupies PDF pages 288–309 (printed pages 52730–52751); the reading excerpt covers those pages only.”

Before: “They therefore cannot have originated in response to the 1985 circular.”

After: “Technical standards were already available. The National Bureau of Standards had published guidance on physical security and risk analysis, along with an encryption standard.”

## Authoring boundary

`scripts/content.py` holds the narrative, structured paragraph/quote blocks, edition notes, and reader notice copy. `data/records.json` holds library descriptions and source metadata. Templates supply short UI labels and layout. Keep `matches[].passage`, `reference_passage`, all `site/sources/` files, and each reader's `<main id="text">` unchanged in editorial revisions.

Footnotes use numbered anchors with backlinks. Existing record identifiers and filter values are stable; friendlier labels may be mapped at render time. Never introduce new factual claims solely to make a passage sound fluent. Check substantive claims against the referenced documents.
