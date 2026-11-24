from PIL import Image

tp = Image.open('touchpad.jpg')
print("touchpad:", tp.size)
# Let's crop bottom of touchpad and see what it shows
cr = Image.open('cardreader.jpg')
print("cardreader:", cr.size)
