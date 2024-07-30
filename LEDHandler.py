from time import sleep
import board
import neopixel


PIN_GPIO = 8


pixels = neopixel.NeoPixel(PIN_GPIO, 5)
	

while (True):
    pixels[0] = (255, 0, 0)
    sleep(1)
    pixels[0] = (0, 0, 0)
    sleep(1)
    
    