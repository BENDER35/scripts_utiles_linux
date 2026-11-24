from PIL import Image
import numpy as np

for side in ["front", "left", "right"]:
    im = Image.open(f"{side}.jpg")
    arr = np.array(im)
    # Check background color
    bg = arr[10, 10]
    print(f"{side}: bg={bg}")
    # find where the laptop profile is
    diff = np.abs(arr.astype(int) - bg.astype(int)).sum(axis=2)
    mask = diff > 30
    y_idxs, x_idxs = np.where(mask)
    if len(y_idxs) > 0:
        print(f"{side}: laptop area x=[{x_idxs.min()}, {x_idxs.max()}], y=[{y_idxs.min()}, {y_idxs.max()}]")
