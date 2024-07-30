import board
import neopixel


PIN_5 = 4
PIN_GROUND = 6
PIN_GPIO = 8


pixels = neopixel.NeoPixel(board.D8)
	
pixels[0] = (255, 0, 0)