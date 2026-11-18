---
license: cc-by-4.0
pretty_name: The Hidden Acquisitions Index
language:
- en
tags:
- artificial-intelligence
- antitrust
- competition-policy
- mergers-and-acquisitions
- acquihire
- economics
size_categories:
- n<1K
configs:
- config_name: deals
  data_files: data/deals.csv
- config_name: sources
  data_files: data/sources.csv
- config_name: regulatory_events
  data_files: data/regulatory_events.csv
- config_name: money_components
  data_files: data/money_components.csv
- config_name: rejected
  data_files: data/rejected.csv
---

# The Hidden Acquisitions Index

The Hidden Acquisitions Index is an open, source-checked dataset of transactions in which large companies gained an AI company's people, technology or influence without buying the company: licence and team hires, team hires, minority stakes with control rights, investments tied to compute commitments, and investments with commercial partnerships. Version 1.1.0 records 109 deals (36 core, 63 related, 10 on hold) announced between 23 January 2023 and 30 October 2026, involving 33 buyers, with 1,700 sources (1,460 official records and 240 major-newsroom reports). Every coded fact is linked to a source with an exact quote of at most 20 words; 99.9% of quotes were confirmed word for word by at least one check between 15 and 18 November 2026 (live page, archived copy, rendered page or a separate second check), and the check result is recorded for every source. It also records 82 regulator events, 62 disclosed amounts kept as separate components (never summed), outcomes at 6, 12 and 24 months, and 168 candidates excluded with their reasons.

- **Website:** https://www.acquiry.com/labs/hidden-acquisitions/
- **Version:** 1.1.0 (2026-11-19)
- **DOI:** [10.5281/zenodo.24244788](https://doi.org/10.5281/zenodo.24244788)
- **Licence:** CC BY 4.0
- **Editor:** Joash Boyton (ORCID [0009-0000-2405-8766](https://orcid.org/0009-0000-2405-8766))
- **Publisher:** Acquiry Labs, the research arm of Acquiry Pty Ltd, Melbourne, Australia

## Files

| File | Rows | What it holds |
| --- | --- | --- |
| data/deals.csv | 109 | One row per deal: parties, dates, structure, rights, values, outcomes, tier |
| data/sources.csv | 1,700 | Every source: publisher, date, grade, URL, archived copy, exact quote, fields it supports, and the result of each quote check |
| data/regulatory_events.csv | 82 | Dated actions by competition authorities and other public bodies |
| data/money_components.csv | 62 | Each disclosed amount as stated, with its type. Never add these together. |
| data/rejected.csv | 168 | Candidates considered and excluded, with the reason code and a source |
| data/codebook.csv | 110 | Every field: type, allowed values, definition |
| data/research_log.csv | 2152 | Round 6 research trail: for each requested field, whether evidence was found and where the researcher looked |
| data/*.json | | The same data in nested form, plus meta |

## How to use it

- **Tiers:** core deals give the buyer at least one control lever (staff, a licence, a board seat or a veto). Related deals are investments with a commercial tie. On-hold deals have incomplete evidence and are excluded from counts on the website.
- **Money:** amounts are recorded as stated by the source, with their type. Do not sum components of one deal or across deals.
- **Unknowns:** "not disclosed" means no eligible source states the value. It does not mean none.
- **Sources:** grade A = the company, a filing, a regulator, a court or a registry. Grade B = a major newsroom with editorial standards; a grade B fact needs two independent newsrooms.
- **Quote checks:** `quote_status` gives the best result across all checks. 1,385 quotes were matched by the automated checker, 82 more on the rendered page (the EU DMA register needs JavaScript), and the rest by a separate manual or assisted check where recorded. 1 sources are not confirmed word for word by any check, usually because the site blocks automated access; they are listed with their result so you can exclude them.
- **Archived copies:** a Wayback Machine copy is recorded for 96.2% of sources (1,635 of 1,700). The other 65 come from sites that block or limit archiving; each says so in `archive_note`.

## Independence

Acquiry Pty Ltd, which publishes the index, is a company that advises on acquisitions. No company pays to be included or excluded, and deals Acquiry has advised on are left out. The index takes no position on whether these deals are good or bad for competition.

## Corrections

Report an error through https://www.acquiry.com/contact and mention "Hidden Acquisitions Index correction". Every correction is recorded in CHANGELOG.md.

## Limitations

- Only deals with public evidence can be included, so undisclosed arrangements are missing by design.
- Values and terms are often undisclosed: "not disclosed" is common and is not a "no".
- Grade B facts rely on newsroom reporting that the parties may not have confirmed.
- Coverage runs from 23 January 2023 to 30 October 2026; later deals are in later versions.

## Citation

Boyton, J. (2026). *The Hidden Acquisitions Index* (Version 1.1.0) [Data set]. Acquiry Labs. https://doi.org/10.5281/zenodo.24244788
