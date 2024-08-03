from time import sleep
import board
import neopixel


TOTAL_LIGHTS = 3
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


def cleanup() -> None:
    for i in range(TOTAL_LIGHTS):
        pixels[i] = (0, 0, 0)
        
        
    


if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        cleanup()
        
    