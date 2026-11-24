# Let's inspect the bounding boxes and visual layout of open_view.jpg and freigestellt.jpg
from PIL import Image

for name in ['open_view', 'freigestellt', 'keyboard', 'front', 'left', 'right']:
    im = Image.open(f"{name}.jpg")
    print(f"{name}: size={im.size}")
