from PIL import Image
import numpy as np

im = Image.open('freigestellt.jpg')
arr = np.array(im)

# Let's see the center of the webcam (top bezel of screen)
# Screen is at the top. Let's find top bezel center:
print("freigestellt size:", im.size)

# Let's inspect rows around screen top
# y around 80 to 200, x around 700 to 1100
for y in range(80, 160, 10):
    row = arr[y, :, :]
    mask = (row[:,0] < 240) | (row[:,1] < 240) | (row[:,2] < 240)
    idxs = np.where(mask)[0]
    if len(idxs) > 0:
        print(f"y={y}: min_x={idxs.min()}, max_x={idxs.max()}, center={(idxs.min()+idxs.max())//2}")
