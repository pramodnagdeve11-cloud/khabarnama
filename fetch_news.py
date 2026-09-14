import json,urllib.request,xml.etree.ElementTree as ET
FEEDS=[("India","https://news.google.com/rss/search?q=India+when:1d&hl=hi&gl=IN&ceid=IN:hi"),("Madhya Pradesh","https://news.google.com/rss/search?q=Madhya+Pradesh+when:1d&hl=hi&gl=IN&ceid=IN:hi"),("World","https://news.google.com/rss/search?q=World+when:1d&hl=hi&gl=IN&ceid=IN:hi"),("Sports","https://news.google.com/rss/search?q=Sports+when:1d&hl=hi&gl=IN&ceid=IN:hi"),("Entertainment","https://news.google.com/rss/search?q=Entertainment+when:1d&hl=hi&gl=IN&ceid=IN:hi"),("Business","https://news.google.com/rss/search?q=Business+when:1d&hl=hi&gl=IN&ceid=IN:hi"),("Technology","https://news.google.com/rss/search?q=Technology+when:1d&hl=hi&gl=IN&ceid=IN:hi")]
out=[];seen=set()
for cat,url in FEEDS:
 try:
  r=urllib.request.Request(url,headers={"User-Agent":"Khabarnama/1.0"}); root=ET.fromstring(urllib.request.urlopen(r,timeout=20).read())
  for it in root.findall(".//item")[:12]:
   t=(it.findtext("title") or "").strip();u=(it.findtext("link") or "").strip()
   if t and u and t.lower() not in seen:
    seen.add(t.lower());out.append({"title":t,"description":(it.findtext("description") or "")[:300],"category":cat,"source":(it.findtext("source") or "News").strip(),"date":(it.findtext("pubDate") or "").strip(),"url":u})
 except Exception as e: print(cat,e)
json.dump(out,open("news.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("updated",len(out))
