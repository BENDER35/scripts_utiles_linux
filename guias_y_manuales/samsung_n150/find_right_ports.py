from PIL import Image
import numpy as np

right = Image.open('right.jpg')
arr = np.array(right)
gray = np.mean(arr, axis=2)

diff_x = np.abs(np.diff(gray, axis=1))

for x in range(0, 1400, 50):
    grad = diff_x[60:220, x:x+50].max()
    print(f"right x={x:4d}: grad={grad:.1f}")
