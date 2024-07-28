import RPi.GPIO as GPIO
import time

pin = 7
pin1 = 11

def setup():
  GPIO.setmode(GPIO.BOARD)       
  
  GPIO.setup(pin, GPIO.IN)   # Set LedPin's mode is output
  GPIO.setup(pin1, GPIO.OUT)   # Set LedPin's mode is output
  
  
  GPIO.output(pin1, GPIO.HIGH)

def loop():
  while True:
    print(GPIO.input(pin))
    time.sleep(1)

def destroy():
  GPIO.output(pin1, GPIO.LOW)   # led off
  GPIO.cleanup()                  # Release resource

if __name__ == '__main__':     # Program start from here
  setup()
  try:
    loop()
  except KeyboardInterrupt: 
    destroy()