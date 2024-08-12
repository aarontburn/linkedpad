import time
import serial   

ser = serial.Serial("COM3", 115200)

counter = 0  
while True:
    print("Writing:", counter)
    ser.write((str(counter) + "\n").encode())
    counter += 1
    time.sleep(1)
    
    