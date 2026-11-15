# Hidden Acquisitions Index (private draft)

**Draft. Data under verification. Do not cite or redistribute.**

Acquiry Labs, a research division of Acquiry Pty Ltd. A source-checked record of AI licensing, hiring, investment and related capability-transfer transactions.

## What runs here
- `scripts/check_data.py`: rule checks on `data/deals.json` (every fact linked to a source, quote length, banned wording, values graded).
- `scripts/verify_sources.py`: opens every source link, extracts the page or PDF text, and confirms each stored quote appears word for word. Falls back to the archived copy when the live page is blocked or changed. No AI is involved.
- `.github/workflows/verify.yml`: runs both on every data change, weekly, and on demand (Actions → Verify sources → Run workflow). Results are committed to `reports/`.

## Reports
- `reports/summary.md`: counts by result (exact, near, not_found, blocked, gone, error).
- `reports/source_check.csv`: one row per source.

"Hidden" means not classified as an acquisition in conventional M&A statistics. It does not mean secret or unlawful.
