"""Deterministic source verifier for the Hidden Acquisitions Index.

For every source in data/deals.json it fetches the page (or PDF), extracts the text,
and checks that the stored quote appears on it. No AI is involved: a quote either
appears in the page text or it does not. If the live page is blocked or the quote is
missing, it tries the archived copy (archive_url). Results go to reports/.
"""
import csv, io, json, os, re, sys, time, unicodedata, datetime, collections
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

UA = "AcquiryLabs-SourceVerifier/1.0 (+https://www.acquiry.com/labs/; research@acquiry.com)"
TIMEOUT = 40
HOST_DELAY = 2.0          # seconds between requests to the same host (be polite)
NEAR_THRESHOLD = 95       # partial-ratio score that counts as a near match (flagged for review)

def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
           .replace("–", "-").replace("—", "-").replace("‑", "-").replace(" ", " "))
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()

def extract(resp):
    ctype = resp.headers.get("content-type", "").lower()
    body = resp.content
    if "pdf" in ctype or body[:5] == b"%PDF-":
        from pdfminer.high_level import extract_text
        return extract_text(io.BytesIO(body))
    if "json" in ctype:
        return body.decode("utf-8", "ignore")
    soup = BeautifulSoup(body, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    return soup.get_text(" ")

def raw_archive(url):
    # Wayback: add id_ after the timestamp to get the original page without the toolbar.
    return re.sub(r"(web\.archive\.org/web/\d+)(/)", r"\1id_\2", url, count=1)

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "en"})

MAX_BYTES = 40_000_000      # stop reading a page after 40 MB
PAGE_DEADLINE = 60          # seconds allowed for one download, however slowly it arrives

def get_limited(url):
    r = session.get(url, timeout=(15, 30), allow_redirects=True, stream=True)
    start, chunks, size = time.time(), [], 0
    for chunk in r.iter_content(65536):
        chunks.append(chunk); size += len(chunk)
        if size > MAX_BYTES or time.time() - start > PAGE_DEADLINE:
            break
    r._content = b"".join(chunks); r.close()
    return r

def fetch(url):
    for attempt in range(3):
        try:
            r = get_limited(url)
            if r.status_code in (429, 503) and attempt < 2:
                time.sleep(10 * (attempt + 1)); continue
            return r.status_code, r.url, (extract(r) if r.status_code < 400 else "")
        except Exception as e:  # network error
            if attempt == 2:
                return 0, url, f"__ERROR__ {type(e).__name__}"
            time.sleep(5)

def check_quote(text, quote):
    nt, nq = norm(text), norm(quote)
    if not nq:
        return "no_quote", 0
    if nq in nt:
        return "exact", 100
    score = fuzz.partial_ratio(nq, nt) if len(nt) < 400_000 else 0  # exact match above covers long pages; fuzzy scoring on very long text is too slow
    return ("near" if score >= NEAR_THRESHOLD else "not_found"), round(score)

def main():
    deals = json.load(open("data/deals.json"))["deals"]
    jobs = []
    for d in deals:
        for s in d.get("sources", []):
            jobs.append({"deal_id": d["deal_id"], "tier": d.get("index_tier"), "n": s["n"], "grade": s.get("grade"),
                         "url": s["url"], "archive_url": s.get("archive_url") or "", "quote": s.get("quote", ""),
                         "supports": ";".join(s.get("supports", []))})
    # fetch each distinct URL once
    urls = sorted({j["url"] for j in jobs} | {j["archive_url"] for j in jobs if j["archive_url"]})
    by_host = collections.defaultdict(list)
    for u in urls:
        by_host[urlparse(u).netloc].append(u)
    pages = {}
    def run_host(host_urls):
        for u in host_urls:
            pages[u] = fetch(raw_archive(u) if "web.archive.org/web/" in u else u)
            time.sleep(HOST_DELAY)
    with ThreadPoolExecutor(max_workers=12) as ex:
        list(ex.map(run_host, by_host.values()))

    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    rows = []
    for j in jobs:
        status, final, text = pages.get(j["url"], (0, j["url"], ""))
        live_res, score = check_quote(text, j["quote"]) if status and status < 400 and not text.startswith("__ERROR__") else ("blocked" if status in (401, 403, 429) else ("gone" if status in (404, 410) else "error"), 0)
        method, result = "live", live_res
        if live_res not in ("exact",) and j["archive_url"]:
            a_status, _, a_text = pages.get(j["archive_url"], (0, "", ""))
            if a_status and a_status < 400:
                a_res, a_score = check_quote(a_text, j["quote"])
                if a_res == "exact" or (a_res == "near" and live_res != "near"):
                    method, result, score = "archive", a_res, a_score
        rows.append({**j, "http_status": status, "final_url": final, "method": method, "result": result,
                     "score": score, "checked_at_utc": now})

    os.makedirs("reports", exist_ok=True)
    with open("reports/source_check.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    c = collections.Counter(r["result"] for r in rows)
    core = collections.Counter(r["result"] for r in rows if r["tier"] == "core")
    by_method = collections.Counter((r["result"], r["method"]) for r in rows)
    lines = [f"# Source check, {now}", "",
             f"Sources checked: {len(rows)} ({len(urls)} distinct URLs)", "",
             "| Result | All | Core deals |", "|---|---|---|"]
    for k in ["exact", "near", "not_found", "blocked", "gone", "error", "no_quote"]:
        lines.append(f"| {k} | {c.get(k,0)} | {core.get(k,0)} |")
    lines += ["", f"Exact via archive copy: {by_method.get(('exact','archive'),0)}", "",
              "- exact: quote appears word for word (after normalising spaces, quote marks and dashes).",
              "- near: 95%+ similar; needs a human look.",
              "- not_found: page opened but quote not on it.",
              "- blocked / gone / error: page refused the robot, no longer exists, or failed to load; archive copy also not usable.",
              "", "Full detail: reports/source_check.csv"]
    worst = [r for r in rows if r["result"] in ("not_found", "near") and r["tier"] == "core"][:40]
    if worst:
        lines += ["", "## Core-deal sources needing attention", "", "| deal | source | result | score | url |", "|---|---|---|---|---|"]
        lines += [f"| {r['deal_id']} | {r['n']} | {r['result']} | {r['score']} | {r['url'][:90]} |" for r in worst]
    md = "\n".join(lines)
    open("reports/summary.md", "w").write(md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(md)
    print(md)

if __name__ == "__main__":
    main()
