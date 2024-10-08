
from socket import setdefaulttimeout, socket, error, AF_INET, SOCK_STREAM
from Helper import start_thread
from time import sleep


DELAY_SECONDS: float = 1 # Every second

listeners: list = []

_listener_started = False

_connected: bool = False
setdefaulttimeout(3)


def listen_to_wifi():
    global _listener_started
    _listener_started = True
    start_thread(_wifi_listener)


def add_listener(callback) -> None:
    listeners.append(callback)

def is_connected() -> bool:
    return _connected


def _wifi_listener(): 
    global _connected
    while True:
        attempt_wifi_connection()
        sleep(DELAY_SECONDS)


def attempt_wifi_connection() -> bool:
    global _connected
    
    current_status = False
    try:
        socket(AF_INET, SOCK_STREAM).connect(("8.8.8.8", 53))
        current_status = True
    except error:
        current_status = False
    
    if _connected != current_status:
        if _listener_started:
            for listener in listeners:
                listener(current_status)

    _connected = current_status
    return current_status
