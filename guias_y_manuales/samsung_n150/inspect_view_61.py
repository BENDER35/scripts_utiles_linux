from PIL import Image
import numpy as np

im = Image.open('view_61.jpg')
arr = np.array(im)
diff = np.abs(arr.astype(int) - 255).sum(axis=2)
mask = diff > 30
y_idxs, x_idxs = np.where(mask)
print(f"view_61 laptop bbox: x=[{x_idxs.min()}, {x_idxs.max()}], y=[{y_idxs.min()}, {y_idxs.max()}]")
for y in [100, 200, 300, 400, 500, 600, 700, 800, 900]:
    row_m = mask[y, :]
    if row_m.any():
        print(f"y={y}: x=[{np.where(row_m)[0].min()}, {np.where(row_m)[0].max()}]")
