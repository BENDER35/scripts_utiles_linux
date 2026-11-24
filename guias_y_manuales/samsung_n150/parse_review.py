
import urllib.request, re
url = "https://www.notebookcheck.net/Review-Samsung-NP-N150-Eom-Netbook.31589.0.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8", errors="ignore")
# split by headers or text blocks
text = re.sub(r"<[^>]+>", "\n", html)
lines = [l.strip() for l in text.split("\n") if l.strip()]
for i, l in enumerate(lines):
    if "Connectivity" in l or "Eingabeger" in l or "Anschl" in l or "Front" in l:
        print("\n".join(lines[max(0, i-2):min(len(lines), i+20)]))
        print("*"*40)
