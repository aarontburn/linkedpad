import neopixel
import time
import board

pixels = neopixel.NeoPixel(board.D18, 1)

while True:
    print('white')
    pixels[0] = (255, 255, 255)
    time.sleep(1)
    print('off')
    pixels[0] = (0, 0, 0)
    time.sleep(1)
    
    