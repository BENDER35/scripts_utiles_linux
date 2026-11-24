from PIL import Image
import numpy as np

im = Image.open('keyboard.jpg')
arr = np.array(im)

# Let's check bottom-left (where LEDs are) and bottom-right (where power switch is)
# y=900 to 1050
print("Bottom left (LEDs) y=950..1020, x=50..250")
bl = arr[950:1020, 50:250]
print("bl min/max lum:", bl.min(), bl.max())

print("Bottom right (Power switch) y=950..1020, x=1150..1350")
br = arr[950:1020, 1150:1350]
print("br min/max lum:", br.min(), br.max())
