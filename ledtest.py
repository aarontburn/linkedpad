import neopixel
import time
import board

pixels = neopixel.NeoPixel(board.D18, 2)

while True:
    print('white')
    pixels[0] = (255, 255, 255)
    pixels[1] = (255, 255, 255)
    time.sleep(1)
    print('off')
    pixels[0] = (0, 0, 0)
    pixels[1] = (0, 0, 0)
    time.sleep(1)
    
    