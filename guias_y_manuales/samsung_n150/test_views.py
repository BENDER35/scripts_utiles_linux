from PIL import Image
import numpy as np

for fname in ['open_view.jpg', 'open_view2.jpg']:
    im = Image.open(fname)
    arr = np.array(im)
    print(f"=== {fname} ===")
    for y in [100, 300, 500, 700, 900]:
        mask = (arr[y,:,0] < 240) | (arr[y,:,1] < 240) | (arr[y,:,2] < 240)
        idxs = np.where(mask)[0]
        if len(idxs) > 0:
            print(f"y={y:4d}: xmin={idxs.min():4d}, xmax={idxs.max():4d}, width={idxs.max()-idxs.min():4d}")
        else:
            print(f"y={y:4d}: all white/empty")
