
from socket import setdefaulttimeout, socket, error, AF_INET, SOCK_STREAM
from main import start_thread
from time import sleep

DELAY_SECONDS: float = 1 # Every second

listeners: list = []

_connected: bool = False


def listen_to_wifi():
    start_thread(_wifi_listener)


def add_listener(callback) -> None:
    listeners.append(callback)

def is_connected() -> bool:
    return _connected


def _wifi_listener(): 
    global _connected
    while True:
        current_status = attempt_wifi_connection()
        if _connected != current_status:
            for listener in listeners:
                listener(current_status)

        _connected = current_status

        sleep(DELAY_SECONDS)



def attempt_wifi_connection() -> bool:
    try:
        setdefaulttimeout(3)
        socket(AF_INET, SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except error:
        return False
    

