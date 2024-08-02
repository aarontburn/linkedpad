import GPIOHandler
import DatabaseHandler
from threading import Thread
import time


def init():
    print("Booting...")
    GPIOHandler.setup_gpio()
    DatabaseHandler.init_db()

    _start_thread(GPIOHandler.gpio_listen)
    _start_thread(DatabaseHandler.db_listen)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIOHandler.destroy_gpio()
        DatabaseHandler.close()


def _start_thread(target):
    thread = Thread(target=target)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    init()




# Pins 4, 6, 12 for LED
# Pins 31, 33, 35, 37 for Key Rows
# Pins 32, 36, 38, 40 for Key Columns