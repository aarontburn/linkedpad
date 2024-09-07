from threading import Thread
import inspect


def start_thread(target, args = ()):
    thread = Thread(target=target, args=args)
    thread.daemon = True
    thread.start()


def get_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return round(int(f.read().strip()) / 1000, 2)


def log(*message) -> None:
    
    filename = inspect.stack()[1].filename.replace("\\", '/').split("/")[-1].split('.')[0]
    
    out: str = ''
    
    for s in message:
        out += ' ' + str(s)
    
    print(filename + ": " + out[1:], flush=True)
    