import neopixel
import time
import board

lights = 20
pixels = neopixel.NeoPixel(board.D18, lights, brightness=0.2)

while True:
    print('white')
    for i in range(lights):
        pixels[i] = (255, 255, 255)
    time.sleep(1)
    print('off')
    for i in range(lights):
        pixels[i] = (0, 0, 0)
    time.sleep(1)
    
     