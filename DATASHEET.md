# Datasheet: The Hidden Acquisitions Index, version 1.1.0

Following the "Datasheets for Datasets" questions (Gebru et al.).

## Motivation
- **Why was it created?** Large companies have gained AI companies' people, technology or influence through licences, hires and minority stakes rather than purchases. These deals sit outside merger statistics built on completed company purchases. Other public trackers exist (for example by SOMO and GenAI Brief); this index adds per-field sourcing, exact quotes, recorded quote checks, archived copies and outcome tracking.
- **Who created it?** Joash Boyton (editor), Acquiry Labs, the research arm of Acquiry Pty Ltd, Melbourne, Australia.
- **Who funded it?** Acquiry Pty Ltd, a company that advises on acquisitions. No company pays to be included or excluded. Deals Acquiry has advised on are excluded.

## Composition
- **Instances:** 109 deals (36 core, 63 related, 10 on hold), announced 23 January 2023 to 30 October 2026, involving 33 buyers.
- **Also included:** 1,700 sources, 82 regulator events, 62 money components, outcome observations at 6, 12 and 24 months, and 168 excluded candidates with reasons.
- **Fields:** 110, defined in codebook.csv.
- **Missing values:** "not disclosed" means no eligible source states the value. It is not a zero or a "no".
- **Confidential or personal data:** none beyond names of executives and founders as published by their employers or major newsrooms.

## Collection
- **How:** candidates from regulator registers (including EU Digital Markets Act Article 14 notices), company announcements, filings, court records and major newsroom reporting, tested against written inclusion rules.
- **Source standard:** every coded fact needs an official source (grade A) or two independent major newsrooms (grade B).
- **Quotes:** every source carries an exact quote of at most 20 words.
- **Checking:** an automated checker fetched every page (or its archived copy) and looked for the quote word for word: 1,385 exact. Pages that need JavaScript were checked as rendered in a browser (82). Round 6 additions were also checked separately for quote, value and date before merging. Each source records its check results.
- **Research round 6 (November 2026):** every blank field of every live deal was researched again; the trail is in research_log.csv.

## Uses
- **Suitable for:** descriptive research on AI deal structures, regulator responses, outcomes and transparency of terms; teaching; journalism.
- **Not suitable for:** totals of "money spent" (components must not be summed); inference about legality or competitive effects without further evidence; treating "not disclosed" as "no".

## Distribution and maintenance
- **Licence:** CC BY 4.0.
- **Where:** https://www.acquiry.com/labs/hidden-acquisitions/ and Zenodo, DOI 10.5281/zenodo.24244788.
- **Updates:** versioned releases with a public changelog; sources are re-checked weekly by the automated checker.
