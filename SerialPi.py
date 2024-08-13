import serial

_PORT: str = '/dev/ttyGS0'
_BAUD: int = 9600

_ser: serial.Serial = None

def init():
    _establish_serial()
    

def listen() -> None:
    while True:
        try:
            data: str = str(_ser.readline())[2:-1]
            if data != '':
                print("Received: " + data)
        except Exception:
            _establish_serial()


def send(data: str) -> None:
    if _ser != None:
        print("Sending " + str(data))
        try:
            _ser.write((str(data) + "\n").encode())
        except Exception:
            _establish_serial()
            _ser.write((str(data) + "\n").encode())
            


def _establish_serial() -> None:
    global _ser
    if _ser != None:
        _ser.close()
        
    _ser = serial.Serial(
        port=_PORT,
        baudrate = _BAUD,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,  
        timeout=0.25,
        rtscts=True
    )

    
if __name__ == '__main__':
    try:
        init()
        listen()
    except KeyboardInterrupt:
        if _ser != None:
            _ser.close()