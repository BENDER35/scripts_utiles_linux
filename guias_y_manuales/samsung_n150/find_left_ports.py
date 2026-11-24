from PIL import Image
import numpy as np

left = Image.open('left.jpg')
arr = np.array(left)
gray = np.mean(arr, axis=2)

diff_x = np.abs(np.diff(gray, axis=1))

for x in range(0, 1400, 50):
    grad = diff_x[60:220, x:x+50].max()
    print(f"left x={x:4d}: grad={grad:.1f}")
