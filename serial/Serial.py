import serial


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
    

    try:
        while True:
            x = str(ser.readline())[2:-1]
            if x != '':
                print(x)
    except serial.SerialException:
        ser.close()
        main()
    except Exception as e:
        print(e)
        print("Closing serial connection.")
        ser.close()

if __name__ == '__main__':
    main()