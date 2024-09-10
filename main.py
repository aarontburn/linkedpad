from time import sleep
import GPIOHandler
import DatabaseHandler
import LEDHandler
import SerialHandler
import WifiHandler
from Helper import start_thread, log

def init():
    log("Booting...")
    LEDHandler.init()
    GPIOHandler.setup_gpio()
    DatabaseHandler.init()
    
    # Do loading animation
    _await_boot_finish()
    WifiHandler.listen_to_wifi()
    
    
    LEDHandler.alert_boot_process(0)
    start_thread(LEDHandler.do_loading_pattern)
    DatabaseHandler.init_db()
    LEDHandler.alert_boot_process(1)

    start_thread(SerialHandler.init)
    start_thread(GPIOHandler.gpio_listen)
    start_thread(DatabaseHandler.db_listen)


    exiting = False
    try:
        while not exiting:
            sleep(0.5)
            # log("Temp: " + str(_get_temp()) + " C")
    except KeyboardInterrupt:
        log("Exiting program...")
        exiting = True
        _run_with_exception(LEDHandler.cleanup)
        _run_with_exception(SerialHandler.cleanup)
        _run_with_exception(DatabaseHandler.close)
        _run_with_exception(GPIOHandler.destroy_gpio)




def _await_boot_finish() -> None:
    log("Starting boot")
    
    log("\tAwaiting Wifi or PC connection...")
    
    
    start_thread(LEDHandler.do_loading_pattern)
    
    MAX_POLLING_SECS: int = 15
    
    i: int = 0
    while True:
        log('\t\tCONNECTION ATTEMPT #' + str(i))
        if WifiHandler.attempt_wifi_connection():
            log("\tWifi connection found.")
            LEDHandler.alert_boot_process(1)
            break
        
        if SerialHandler.is_connected():
            log("\tConnected to PC.")
            LEDHandler.alert_boot_process(1)
            break
        
        i += 1
        if i == MAX_POLLING_SECS:
            log(f"\tNo connections found after {MAX_POLLING_SECS} seconds.")
            LEDHandler.alert_boot_process(2)
            start_thread(LEDHandler.do_error_pattern)
        sleep(1)
    
    log("\tBoot processed finished.")
    
    
    

def _run_with_exception(target) -> None:
    try:
        target()
    except Exception as e:
        log(e)
    

    
    
if __name__ == '__main__':
    init()




# Pins 4, 6, 12 for LED
# Pins 29, 31, 33, 35, 37 for Key Rows
# Pins 32, 36, 38, 40 for Key Columns

# 32, 29 for H0
