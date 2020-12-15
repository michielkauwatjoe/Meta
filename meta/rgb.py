#!/usr/bin/env python3
'''
bm = sd.Bitmap(Width,Height)

for x in xrange(Height*Width):
    j= x // Width
    i= x % Width
    col = Color[x]
    bm.SetPixel(i,j,col)

bm.Save(PathWrite,sd.Imaging.ImageFormat.Bmp)
'''

from PIL import Image
w = h = 255
img = Image.new( 'RGB', (w, h), "black") # Create a new black image
pixels = img.load() # Create the pixel map

for i in range(img.size[0]):    # For every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100) # Set the colour accordingly

img.show()
