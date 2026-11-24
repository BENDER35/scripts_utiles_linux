from PIL import Image
import numpy as np

for name in ['open_view2', 'frontal_outdoor', 'view_05', 'view_02', 'view_60']:
    im = Image.open(f"{name}.jpg")
    im_small = im.resize((50, 20))
    chars = " .:-=+*#%@"
    arr = np.array(im_small.convert('L'))
    print(f"=== {name} ===")
    for row in arr[::2]:
        print("".join([chars[int(val / 256 * len(chars))] for val in row]))
