from PIL import Image
import numpy as np

im = Image.open('keyboard.jpg')
arr = np.array(im)

crop_power = im.crop((1100, 900, 1380, 1040))
crop_power.save('crop_power.jpg')

# Let's inspect bright pixels (icons / text) in that crop
cr_arr = np.array(crop_power)
white_pts = np.where(cr_arr > 200)
print(f"Bright pixels found: {len(white_pts[0])}")
