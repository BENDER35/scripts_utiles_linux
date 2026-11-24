from PIL import Image
import numpy as np

front = Image.open('front.jpg').convert('L')
arr = np.array(front)

# find bottom edge of laptop profile across x columns
col_profiles = []
for x in range(0, 1400, 20):
    col = arr[:, x]
    dark_y = np.where(col < 240)[0]
    if len(dark_y) > 0:
        col_profiles.append((x, dark_y.min(), dark_y.max(), dark_y.max() - dark_y.min(), col[dark_y.min():dark_y.max()].mean()))
    else:
        col_profiles.append((x, -1, -1, 0, 255))

for cp in col_profiles:
    if cp[3] > 0:
        print(f"x={cp[0]:4d}: y=[{cp[1]:3d}, {cp[2]:3d}], h={cp[3]:3d}, avg_lum={cp[4]:.1f}")
