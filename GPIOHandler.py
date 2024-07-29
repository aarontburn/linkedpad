import RPi.GPIO as GPIO
import DatabaseHandler

# GPIO setup
INPUT_PIN = 3
OUTPUT_PIN = 5

def setup_gpio():
    print("Initializing GPIO handler...")
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(OUTPUT_PIN, GPIO.OUT)
    GPIO.output(OUTPUT_PIN, GPIO.LOW)
    
    print("GPIO initialization finished.")

def gpio_loop():
    print("GPIO listener started.")
    while True:
        if GPIO.input(INPUT_PIN) == 0:
            DatabaseHandler.on_key_press('A', '3')

def destroy_gpio():
    GPIO.cleanup()
