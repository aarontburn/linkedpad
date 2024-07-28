import RPi.GPIO as GPIO
import time

pin = 7

def setup():
  GPIO.setmode(GPIO.BOARD)       
  GPIO.setup(pin, GPIO.IN)   # Set LedPin's mode is output
  
  GPIO.output(pin, GPIO.HIGH)

def loop():
  while True:
    print(GPIO.input(7))
    time.sleep(1)

def destroy():
  GPIO.output(pin, GPIO.LOW)   # led off
  GPIO.cleanup()                  # Release resource

if __name__ == '__main__':     # Program start from here
  setup()
  try:
    loop()
  except KeyboardInterrupt: 
    destroy()