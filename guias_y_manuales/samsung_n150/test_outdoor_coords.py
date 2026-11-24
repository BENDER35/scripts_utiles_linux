from PIL import Image
import numpy as np

im = Image.open('frontal_outdoor.jpg')
arr = np.array(im)
print("Image size:", im.size)

# The laptop is in the center
# Let's inspect rows to find screen top, screen bottom, keyboard, front lip
# Screen top is around row 150-200?
# Let's inspect vertical slices
col = arr[:, 700] # center column
for y in range(50, 1050, 50):
    print(f"y={y:4d}: RGB={col[y]}")
