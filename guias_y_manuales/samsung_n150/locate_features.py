from PIL import Image
import numpy as np

im = Image.open('freigestellt.jpg')
arr = np.array(im)

# Let's inspect where non-white pixels start on each horizontal row
row_bounds = []
for y in range(0, 1050, 20):
    row = arr[y, :, :]
    mask = (row[:,0] < 240) | (row[:,1] < 240) | (row[:,2] < 240)
    idxs = np.where(mask)[0]
    if len(idxs) > 0:
        row_bounds.append((y, idxs.min(), idxs.max(), idxs.max() - idxs.min()))

for y, xmin, xmax, width in row_bounds:
    if y % 100 == 0 or y in [60, 200, 400, 480, 500, 520, 600, 700, 800, 900, 1000]:
        print(f"y={y:4d}: xmin={xmin:4d}, xmax={xmax:4d}, width={width:4d}")

