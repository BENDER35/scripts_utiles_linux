from PIL import Image, ImageDraw

img = Image.open('test_layout.jpg')
draw = ImageDraw.Draw(img)

laptop_x = 450
laptop_y = 230
scale = 1500 / 1560

points = [
    ("Webcam", 960, 70),
    ("Pantalla", 960, 450),
    ("Bisagra Izq", 370, 800),
    ("Teclado", 960, 900),
    ("Touchpad", 960, 1010),
    ("LEDs", 520, 1085),
    ("Lector SD", 960, 1100),
    ("Power Switch", 1380, 1090)
]

for name, ox, oy in points:
    cx = laptop_x + int((ox - 180) * scale)
    cy = laptop_y + int((oy - 15) * scale)
    draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=(255, 0, 0), outline=(255, 255, 255), width=2)
    draw.text((cx + 12, cy - 8), name, fill=(255, 0, 0))

img.resize((1200, 1300)).save('coords_check.jpg', 'JPEG')
print("Coords check saved")
