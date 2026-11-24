from PIL import Image
import numpy as np

front = Image.open('front.jpg')
arr = np.array(front)

gray = np.mean(arr, axis=2)
diff_x = np.abs(np.diff(gray, axis=1))

for seg, (x1, x2) in enumerate([(0, 350), (350, 700), (700, 1050), (1050, 1400)]):
    seg_grad = diff_x[50:250, x1:x2]
    peaks = np.where(seg_grad > 40)
    print(f"Segment {seg} ({x1}-{x2}): max gradient={seg_grad.max():.1f}, num peaks={len(peaks[0])}")

