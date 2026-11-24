from PIL import Image
import numpy as np

for name in ["view_05", "view_61"]:
    im = Image.open(f"{name}.jpg")
    arr = np.array(im)
    bg = arr[10, 10]
    print(name, "top-left:", bg)
