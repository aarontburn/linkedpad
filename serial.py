import RPi.GPIO as GPIO
import time

pin = 7
pin1 = 37

def setup():
  GPIO.setmode(GPIO.BOARD)       
  
  GPIO.setup(pin, GPIO.IN)
  GPIO.setup(pin1, GPIO.IN)
  

def loop():
  while True:
    print(pin, GPIO.input(pin))
    print(pin1, GPIO.input(pin1))
    print()
    time.sleep(0.2)

def destroy():
  GPIO.cleanup()

if __name__ == '__main__':
  setup()
  try:
    loop()
  except KeyboardInterrupt: 
    destroy()