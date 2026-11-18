"""Find or create a Wayback Machine copy for every source that has no archive_url.
Writes reports/archive_map.json: {url: archived_url or null}. Never edits the data file.
"""
import json, time, os, requests

UA = "AcquiryLabs-ArchiveLookup/1.0 (+https://www.acquiry.com/labs/)"
s = requests.Session(); s.headers["User-Agent"] = UA
path = "data/deals_v15_draft.json" if os.path.exists("data/deals_v15_draft.json") else "data/deals.json"
deals = json.load(open(path))["deals"]
urls = sorted({x["url"] for d in deals for x in d.get("sources", []) if not str(x.get("archive_url", "")).startswith("http")})
out = {}

def available(u):
    for k in range(3):
        try:
            r = s.get("https://archive.org/wayback/available", params={"url": u}, timeout=30)
            c = r.json().get("archived_snapshots", {}).get("closest")
            return c["url"].replace("http://", "https://") if c and c.get("available") and str(c.get("status", "")).startswith("2") else None
        except Exception:
            time.sleep(5 * (k + 1))
    return "ERR"

for u in urls:
    if "web.archive.org/web/" in u:
        out[u] = u; continue
    out[u] = available(u); time.sleep(1)

missing = [u for u, v in out.items() if v is None]
for u in missing:  # ask the Wayback Machine to save pages it does not hold yet
    try:
        s.get("https://web.archive.org/save/" + u, timeout=90)
    except Exception:
        pass
    time.sleep(6)
time.sleep(60)
for u in missing:
    out[u] = available(u); time.sleep(1)

os.makedirs("reports", exist_ok=True)
json.dump(out, open("reports/archive_map.json", "w"), indent=0)
found = sum(1 for v in out.values() if v and v != "ERR")
print(f"{len(out)} URLs without an archive link; {found} now have one; {sum(1 for v in out.values() if v is None)} still missing")
