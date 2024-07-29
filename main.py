import GPIOHandler
import DatabaseHandler
import threading
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
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    init()
