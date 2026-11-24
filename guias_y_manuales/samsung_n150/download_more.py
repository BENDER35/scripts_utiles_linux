import urllib.request
from PIL import Image

urls = {
    "frontal_outdoor": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_87.jpg",
    "main_pic": "https://www.notebookcheck.net/fileadmin/_processed_/csm_Samsung_N150_06_a98bbde25b.jpg",
    "view_05": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_05.jpg",
    "view_02": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_02.jpg",
    "view_60": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_60.jpg",
    "view_61": "https://www.notebookcheck.net/fileadmin/_migrated/pics/Samsung_N150_61.jpg",
}

headers = {'User-Agent': 'Mozilla/5.0'}
for k, u in urls.items():
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req) as r, open(f"{k}.jpg", "wb") as f:
            f.write(r.read())
        im = Image.open(f"{k}.jpg")
        print(f"{k}: size={im.size}")
    except Exception as e:
        print(f"Error {k}: {e}")
