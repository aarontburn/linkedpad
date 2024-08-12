import serial


PORT: str = '/dev/ttyGS0'
BAUD: int = 9600


ser: serial.Serial = None




def main():
    ser = serial.Serial(
        port=PORT,
        baudrate = BAUD,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    
    print("Listening")
    

    while 1:
        x = str(ser.readline())
        print(x)
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Closing serial connection.")
        ser.close()