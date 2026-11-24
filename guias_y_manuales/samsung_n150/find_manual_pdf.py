import urllib.request, re

# Let's search duckduckgo for official pdf
url = "https://html.duckduckgo.com/html/?q=filetype:pdf+Samsung+N150+User+Guide"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'href="([^"]+\.pdf)"', html)
        if not matches:
            matches = re.findall(r'uddg=([^"&]+\.pdf)', html)
        for m in matches[:5]:
            import urllib.parse
            print(urllib.parse.unquote(m))
except Exception as e:
    print("Error:", e)
