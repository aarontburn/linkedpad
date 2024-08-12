import time
import serial   


ser: serial.Serial = None

def main():
    ser = serial.Serial(
        "COM3", 
        9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.25,
        rtscts=True  # Enable RTS/CTS flow control
    )


    while True:
        x = str(ser.readline())
        print(x)
                    
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        ser.close()