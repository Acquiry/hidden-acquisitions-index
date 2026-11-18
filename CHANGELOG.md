# Changelog

## 1.1.0 (19 November 2026)

**Research round 6.** Every blank field of every live deal was researched again from scratch under the same source standard, in four parallel runs, then checked before merging.

- **368 field values added**, each with its own source, exact quote and check record. Sources rose from 1,288 to 1,700.
- **Biggest gains:** lead investors (7 to 70 deals), outcomes at 6, 12 and 24 months (16, 12 and 6 to 74, 58 and 36), status after the deal (63 to 85), pre-deal valuation (12 to 33), exclusivity terms (7 to 18), equity stake (6 to 12).
- **Checks before merging:** each new row was checked by rule (source eligibility, grade, quote length) and by a separate live check of quote, value and date. 22 rows were rejected and 67 held back (paywalled, unreadable or single-outlet newsroom facts). No existing value was overwritten; 5 disagreements between sources are recorded in the conflict field.
- **Money:** new amounts are stored as separate components, as stated, labelled where they are whole funding-round totals rather than the buyer's share. Nothing was summed or converted.
- **Corrections to existing records (18):** see corrections in the release notes; includes value-basis wording for Amazon–Anthropic (2024) and Google–Anthropic (2026), MiniMax round figures from the prospectus, Disney–Character.AI's separate retention pool, status codes for Corpusant and Alex, Japan Post Bank's stake labelled as voting rights, SMART Global's announcement date (15 July 2024), and removal of two editorial notes left in v1.0.1.
- **Quote checks recorded per source:** sources.csv now shows the automated checker's result, a rendered-page check for the EU DMA register (which needs JavaScript), and the separate second check.
- **Archived copies:** 1,635 of 1,700 sources (96%) now have a Wayback Machine copy, up from 43%. The other 65 come from sites that block or limit archiving; each says so in the new `archive_note` column of sources.csv.
- **New file:** research_log.csv, the round 6 trail of where each field was searched.

## 1.0.1 (17 November 2026)

First public release.
