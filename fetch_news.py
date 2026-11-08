import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def gnews(q):
    return ("https://news.google.com/rss/search?q=" + urllib.parse.quote(q)
            + "&hl=ja&gl=JP&ceid=JP:ja")


FEEDS = {
    "要人発言": [gnews("(FRB議長 OR 日銀総裁 OR 財務長官 OR 財務相 OR パウエル OR 植田総裁 OR トランプ) 発言 when:1d")],
    "Bloomberg": ["https://feeds.bloomberg.com/markets/news.rss"],
    "Reuters": [gnews("site:reuters.com when:1d")],
    "WSJ": ["https://feeds.a.dowjones.com/rss/RSSMarketsMain"],
    "日経": [gnews("site:nikkei.com when:1d")],
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def parse(xml_bytes):
    items = []
    root = ET.fromstring(xml_bytes)
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        pub = it.findtext("pubDate") or ""
        try:
            ts = parsedate_to_datetime(pub).astimezone(timezone.utc)
        except Exception:
            ts = datetime.now(timezone.utc)
        if title and link:
            items.append({"title": title, "link": link, "date": ts.isoformat()})
    return items


def main():
    result = {"updated": datetime.now(timezone.utc).isoformat(), "tabs": {}}
    total = 0
    for name, urls in FEEDS.items():
        items = []
        for url in urls:
            try:
                items += parse(fetch(url))
            except Exception as e:
                print("ERROR", name, e)
        seen = set()
        uniq = []
        for i in sorted(items, key=lambda x: x["date"], reverse=True):
            if i["link"] not in seen:
                seen.add(i["link"])
                uniq.append(i)
        result["tabs"][name] = uniq[:30]
        total += len(uniq[:30])
        print(name, len(uniq[:30]))
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    if total == 0:
        sys.exit(1)


main()
