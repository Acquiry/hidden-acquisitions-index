# Datasheet: The Hidden Acquisitions Index, version 1.1.0

Following the "Datasheets for Datasets" questions (Gebru et al.).

## Motivation
- **Why was it created?** Large companies have gained AI companies' people, technology or influence through licences, hires and minority stakes rather than purchases. These deals sit outside merger statistics built on completed company purchases. Other public trackers exist (for example by SOMO and GenAI Brief); this index adds per-field sourcing, exact quotes, recorded quote checks, archived copies and outcome tracking.
- **Who created it?** Joash Boyton (editor), Acquiry Labs, the research arm of Acquiry Pty Ltd, Melbourne, Australia.
- **Who funded it?** Acquiry Pty Ltd, a company that advises on acquisitions. No company pays to be included or excluded. Deals Acquiry has advised on are excluded.

## Composition
- **Instances:** 109 deals (36 core, 63 related, 10 on hold), announced 23 January 2023 to 30 October 2026, involving 33 buyers.
- **Also included:** 1,700 sources, 82 regulator events, 62 money components, outcome observations at 6, 12 and 24 months, and 168 excluded candidates with reasons (157 with a source).
- **Fields:** every column of every file is defined in codebook.csv (146 rows), with allowed values and, where a judgement is involved, the coding rule.
- **Missing values:** "not disclosed" means no eligible source states the value. It is not a zero or a "no".
- **Confidential or personal data:** none beyond names of executives and founders as published by their employers or major newsrooms.

## Collection
- **How:** candidates from regulator registers (including EU Digital Markets Act Article 14 notices), company announcements, filings, court records and major newsroom reporting, tested against written inclusion rules.
- **Source standard:** Grade A = the company, a filing, a regulator, a court or a registry. Grade B = a major newsroom with editorial standards. The facts that decide whether a deal is included and how it is classified (buyer, target, date, deal type and structure) rest on a grade A source or two independent grade B newsrooms for all 36 core deals; a date may also come from the first dated report naming both parties (16 deals). Other facts may rest on a single newsroom report: 208 such facts in 39 of the 99 core and related deals, each listed in `single_report_fields` so it can be excluded. In 2 related deals (alibaba-moonshot-2024, google-anthropic-2026) a key fact rests on one report; `headline_check` marks it.
- **Quotes:** every source carries an exact quote of at most 20 words.
- **Checking:** an automated checker fetched 1,699 of the 1,700 pages (or their archived copies) and looked for the quote word for word: 1,385 exact. Pages that need JavaScript were checked as rendered in a browser (82). Every quote is confirmed word for word by at least one check. Round 6 additions were also checked separately for quote, value and date before merging. Each source records its check results.
- **Research round 6 (November 2026):** every blank field of every live deal was researched again; the trail is in research_log.csv.

## Uses
- **Suitable for:** descriptive research on AI deal structures, regulator responses, outcomes and transparency of terms; teaching; journalism.
- **Not suitable for:** totals of "money spent" (components must not be summed); inference about legality or competitive effects without further evidence; treating "not disclosed" as "no".

## Distribution and maintenance
- **Licence:** CC BY 4.0.
- **Where:** https://www.acquiry.com/labs/hidden-acquisitions/ and Zenodo, DOI 10.5281/zenodo.24244788.
- **Updates:** versioned releases with a public changelog; sources are re-checked weekly by the automated checker.
