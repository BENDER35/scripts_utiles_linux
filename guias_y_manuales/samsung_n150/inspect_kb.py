from PIL import Image
import numpy as np

im = Image.open('keyboard.jpg')
print("keyboard size:", im.size)
arr = np.array(im)
col = arr[:, 700]
for y in range(50, 1050, 50):
    print(f"y={y:4d}: RGB={col[y]}")
