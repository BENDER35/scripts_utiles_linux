from PIL import Image

for name in ['freigestellt', 'open_view', 'front', 'left', 'right', 'keyboard']:
    im = Image.open(f"{name}.jpg")
    print(f"{name}: {im.size}")
