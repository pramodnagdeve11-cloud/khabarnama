import json, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Public RSS feeds. Add/remove feeds here as needed.
FEEDS = [
 ("India","https://news.google.com/rss/search?q=India+when:1d&hl=hi&gl=IN&ceid=IN:hi"),
 ("Madhya Pradesh","https://news.google.com/rss/search?q=Madhya+Pradesh+when:1d&hl=hi&gl=IN&ceid=IN:hi"),
 ("World","https://news.google.com/rss/search?q=World+when:1d&hl=hi&gl=IN&ceid=IN:hi"),
 ("Sports","https://news.google.com/rss/search?q=Sports+when:1d&hl=hi&gl=IN&ceid=IN:hi"),
 ("Entertainment","https://news.google.com/rss/search?q=Entertainment+when:1d&hl=hi&gl=IN&ceid=IN:hi"),
 ("Business","https://news.google.com/rss/search?q=Business+when:1d&hl=hi&gl=IN&ceid=IN:hi"),
 ("Technology","https://news.google.com/rss/search?q=Technology+when:1d&hl=hi&gl=IN&ceid=IN:hi")
]

items=[]
for category,url in FEEDS:
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Khabarnama/1.0"})
        data=urllib.request.urlopen(req,timeout=20).read()
        root=ET.fromstring(data)
        for it in root.findall(".//item")[:10]:
            title=(it.findtext("title") or "").strip()
            link=(it.findtext("link") or "").strip()
            desc=(it.findtext("description") or "").strip()
            source=(it.findtext("source") or "News").strip()
            date=(it.findtext("pubDate") or "").strip()
            if title and link:
                items.append({"title":title,"description":desc[:300],"category":category,
                              "source":source,"date":date,"url":link})
    except Exception as e:
        print("Feed failed:", category, e)

# Deduplicate
seen=set(); out=[]
for x in items:
    key=x["title"].lower()
    if key not in seen:
        seen.add(key); out.append(x)

# Add All as a separate category for the default view
for x in list(out):
    out.append({**x,"category":"All"})

with open("news.json","w",encoding="utf-8") as f:
    json.dump(out,f,ensure_ascii=False,indent=2)

print("Wrote",len(out),"items")
