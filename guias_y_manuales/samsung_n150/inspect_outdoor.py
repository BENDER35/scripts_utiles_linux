from PIL import Image
import numpy as np

im = Image.open('frontal_outdoor.jpg')
print("frontal_outdoor size:", im.size)
arr = np.array(im)
# let's see what is in the center
print("center color:", arr[500, 700])
