import urllib.request
import os
from PIL import Image

urls = {
    "open_view": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_30.jpg",
    "open_view2": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_31.jpg",
    "freigestellt": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung-N150_Freigestellt_02.jpg",
    "front": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_54.jpg",
    "left": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_55.jpg",
    "right": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_57.jpg",
    "keyboard": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_26.jpg",
    "touchpad": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_89.jpg",
    "cardreader": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_10.jpg",
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for name, url in urls.items():
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as r, open(f"{name}.jpg", "wb") as f:
            f.write(r.read())
        im = Image.open(f"{name}.jpg")
        print(f"Downloaded {name}.jpg: size={im.size}, format={im.format}")
    except Exception as e:
        print(f"Failed {name}: {e}")
