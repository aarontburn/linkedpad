import serial


PORT: str = '/dev/ttyGS0'
BAUD: int = 115200


ser: serial.Serial = None


def main():
    global ser
    ser = serial.Serial(
        port=PORT,
        baudrate = BAUD,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.25
    )
    
    print("Listening")
    

    while True:
        x = str(ser.readline())[2:-1]
        if x != '':
            print(x)
            

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e.__class__.__name__)
        print(e)
        print("Closing serial connection.")
        ser.close()