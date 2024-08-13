import serial

_PORT: str = '/dev/ttyGS0'
_BAUD: int = 9600

_ser: serial.Serial = None

def init():
    _establish_serial()
    establish_connection()

def establish_connection() -> None:
    log("Attempting to establish connection with PC...")
    while True:
        try:
            data: str = str(_ser.readline())[2:-3]
        except serial.SerialException:
            log("")
            _establish_serial()
            
        if data == 'pc_ready':
            log("Connection with PC formed.")
            send('pi_ready')
            break
        

def listen() -> None:
    log("Listening...")
    while True:
        try:
            data: str = str(_ser.readline())[2:-1]
            if data != '':
                log("Received: " + data)
        except Exception:
            _establish_serial()


def send(data: str) -> None:
    if _ser != None:
        log("Sending " + str(data))
        try:
            _ser.write((str(data) + "\n").encode())
        except Exception:
            _establish_serial()
            _ser.write((str(data) + "\n").encode())
            


def _establish_serial() -> None:
    cleanup()
        
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

def cleanup() -> None:
    if _ser != None:
        _ser.close()
        
def log(message) -> None:
    print(__file__.split('\\')[-1].split('.')[0] + ": " + str(message))
    
if __name__ == '__main__':
    try:
        init()
        listen()
    except KeyboardInterrupt:
        cleanup()