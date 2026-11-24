from PIL import Image

im = Image.open('freigestellt.jpg')
w, h = im.size

# Let's save a reduced version with a grid so we can see coordinates accurately
# Or let's print bounding areas of key colored components
import numpy as np
arr = np.array(im)

# Screen area is usually grayish matte [140-160, 140-160, 140-160]
screen_mask = (arr[:,:,0] > 120) & (arr[:,:,0] < 180) & (arr[:,:,1] > 120) & (arr[:,:,1] < 180) & (arr[:,:,2] > 120) & (arr[:,:,2] < 180)
y_sc, x_sc = np.where(screen_mask)
print(f"Screen mask: x=[{x_sc.min()}, {x_sc.max()}], y=[{y_sc.min()}, {y_sc.max()}]")

# Keyboard area has key gaps / dark keys
dark_mask = (arr[:,:,0] < 80) & (arr[:,:,1] < 80) & (arr[:,:,2] < 80)
y_dk, x_dk = np.where(dark_mask)
print(f"Dark body mask: x=[{x_dk.min()}, {x_dk.max()}], y=[{y_dk.min()}, {y_dk.max()}]")

