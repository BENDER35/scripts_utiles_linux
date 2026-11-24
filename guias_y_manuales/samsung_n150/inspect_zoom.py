import urllib.request, re

url = "https://www.notebookcheck.net/Review-Samsung-NP-N150-Eom-Netbook.31589.0.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8", errors="ignore")

for num in ["54", "55", "56", "57", "10", "89", "26"]:
    m = re.search(r'Samsung_N150_' + num + r'\.jpg"[^>]*title="([^"]*)"', html)
    if m:
        print(f"{num}: {m.group(1)}")
