from time import sleep
import board
import neopixel

# https://github.com/markkleeb/raspberrypi-ws2812
# https://docs.circuitpython.org/projects/neopixel/en/latest/




# GPIO10, GPIO12, GPIO18 or GPIO21
#   Pin 19, 32, 12, 40

#   To use GPIO18 (or pin 12), sound needs to be disabled


# PWM
#   Requires blacklisting and file config i think

# PCM
#   Doesn't require anything?

# SPI
#   Nothing else can be added to the SPI bus.
 
# Pin 33 (PWM1)
# Pin 40 (PCM)

# D18 refers to GPIO18, or pin 12

	

TOTAL_LIGHTS = 3

PIN_5 = 4
PIN_GROUND = 6
GPIO = board.D18 	# pin 12

pixels = None

def init():
	print("Initializing LED Handler...")
	global pixels
	pixels = neopixel.NeoPixel(GPIO, TOTAL_LIGHTS)

	print("LED Handling initialized.")
	_loop()


def _loop(): # This should only be for debugging
	print("Beginning loop")
	while (True):
		set_light(0, (255, 0, 0))
		sleep(1)
		set_light(0, (0, 0, 255))
		sleep(1)


def set_light(index, color):
	print("Setting light at:", index, "with color:", color)
	pixels[index] = color


if __name__ == "__main__":
	init()
	