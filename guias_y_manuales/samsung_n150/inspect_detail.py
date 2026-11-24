from PIL import Image
import numpy as np

for name in ["frontal_outdoor", "view_05", "view_61", "keyboard", "front", "left", "right", "freigestellt"]:
    im = Image.open(f"{name}.jpg")
    print(f"{name}: size={im.size}, mode={im.mode}")
