import serial
import time


PORT: str = '/dev/ttyGS0'
BAUD: int = 9600


ser: serial.Serial = None


def main():
    global ser
    ser = serial.Serial(
        port=PORT,
        baudrate = BAUD,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,  
        timeout=0.25,
        rtscts=True  # Enable RTS/CTS flow control
    )
    
    print("Listening")
    
    counter = 0
    while True:
        print(counter)
        ser.write(("Hello\n").encode())
        time.sleep(1)
        counter += 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        ser.close()