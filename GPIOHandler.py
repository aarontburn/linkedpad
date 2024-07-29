import RPi.GPIO as GPIO
import time
from Key import Key

def setup_keys() -> dict[str, Key]:
	out: dict[str, Key] = {}
	out['A3'] = Key(3, 5, "A3");
	
key_map: dict[str, Key] = setup_keys()

# GPIO setup
INPUT_PIN = 3
OUTPUT_PIN = 5


def setup_gpio():
	print("Initializing GPIO handler...")
	
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(OUTPUT_PIN, GPIO.OUT)
	GPIO.output(OUTPUT_PIN, GPIO.LOW)
	setup_keys()
 
	print("GPIO initialization finished.")



def gpio_listen():
	print("GPIO listener started.")
 
	while True:
		for row_col in key_map:
			key: Key = key_map[row_col]
			key.handle_input(GPIO.input(key._input_pin))
			

def destroy_gpio():
	GPIO.cleanup()



