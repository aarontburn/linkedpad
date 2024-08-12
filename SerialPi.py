import serial

_PORT: str = '/dev/ttyGS0'
_BAUD: int = 9600

_ser: serial.Serial = None

def init():
    global _ser
    _ser = serial.Serial(
        port=_PORT,
        baudrate = _BAUD,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,  
        timeout=0.25,
        rtscts=True
    )
    

def listen() -> None:
    while True:
        data: str = str(_ser.readline())[2:-1]
        if data != '':
            print("Received: " + data)   


def send(data: str) -> None:
    if _ser != None:
        _ser.write((str(data) + "\n").encode())
    
    
if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        _ser.close()