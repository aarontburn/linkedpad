from time import sleep
import board
import neopixel


PIN_5 = 4
PIN_GROUND = 6
PIN_GPIO = 8


pixels = neopixel.NeoPixel(board.D10 , 3)
	

while (True):
    print("red")
    pixels[0] = (255, 0, 0)
    sleep(1)
    print("blue")
    pixels[0] = (0, 0, 255)
    sleep(1)
    
    