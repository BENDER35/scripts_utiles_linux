from PIL import Image

ov = Image.open('open_view.jpg')
fr = Image.open('freigestellt.jpg')

print("open_view size:", ov.size)
print("freigestellt size:", fr.size)
