from PIL import Image
import numpy as np

im = Image.open('freigestellt.jpg')
im_small = im.resize((70, 35))
chars = " .:-=+*#%@"
arr = np.array(im_small.convert('L'))
for row in arr:
    line = "".join([chars[int(val / 256 * len(chars))] for val in row])
    print(line)
