from PIL import Image
import numpy as np

front = Image.open('front.jpg')
arr = np.array(front)
gray = np.mean(arr, axis=2)

diff_x = np.abs(np.diff(gray, axis=1))

for x in range(1050, 1300, 10):
    grad = diff_x[80:200, x:x+10].max()
    if grad > 25:
        print(f"x={x:4d}: max grad={grad:.1f}")
