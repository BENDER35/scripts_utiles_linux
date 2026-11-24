from PIL import Image
import numpy as np

# In left.jpg: size is (1400, 300)
# Caption from Notebookcheck: "Left: AC, USB, Line-Out, Mic"
# In right.jpg: size is (1400, 300)
# Caption from Notebookcheck: "Right: WLAN-switch, 2xUSB, VGA, Kensington"
# In front.jpg: size is (1400, 300)
# Caption: "Front: CardReader" and power switch!

left = Image.open('left.jpg')
right = Image.open('right.jpg')
front = Image.open('front.jpg')

print("All 3 profile images loaded successfully.")
