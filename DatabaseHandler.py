import sys
import pymongo
import ColorHandler
import SerialHandler
from log import log
import socket

if __name__ != "__main__":
    import LEDHandler

_is_init: bool = False

_URI: str = "mongodb+srv://admin:j2MzVYcewmPjnzrG@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad"
_CLIENT = pymongo.MongoClient(_URI)
_DATABASE = _CLIENT.get_database('pad_data')
_COLLECTION = _DATABASE.get_collection('data')

_ACCESS_QUERY: dict[str, str] = {'accessID': ':3'}

_KEYS: list[str] = [row + col for row in ["A", "B", "C", "D"] for col in ["0", "1", "2", "3"]]



def _get_default_obj() -> dict:
    o = {}
    for key in _KEYS:
        o[key] = ColorHandler.OFF
    key = list(_ACCESS_QUERY.keys())[0]
    o[key] = _ACCESS_QUERY[key]
    return o


_DEFAULT_DB_OBJ: dict = _get_default_obj()

_local_state: dict[str, str] = {}



def init_db() -> None:
    log("Initializing database handler...")
    
    if _is_connected_to_internet() == False:
        log("Not connected to the internet.")
        return
    
    _check_database()
    _COLLECTION.find_one({})
    recalibrate()
    global _is_init
    _is_init = True
    LEDHandler.set_light('H0', ColorHandler.get_current_color())
    log("Database initialization finished.")


def db_listen() -> None:
    if _is_init == False:
        return
    
    log("Database listener started.")
    try:
        with _COLLECTION.watch() as stream:
            for change in stream:
                _on_database_change(change['updateDescription']['updatedFields'])
    except Exception as e:
        log("Database closing...")
        log(e)
        _CLIENT.close()


def on_key_press(row_col: str) -> None:
    is_off: bool = _local_state[row_col] == ColorHandler.OFF
    _COLLECTION.find_one_and_update(_ACCESS_QUERY, {"$set": {row_col: ColorHandler.get_current_color() if is_off else ColorHandler.OFF}})


def close() -> None:
    log('Closing...')
    _CLIENT.close()
    
    

def reset() -> None:
    _COLLECTION.find_one_and_update(
        _ACCESS_QUERY,
        {'$set': _DEFAULT_DB_OBJ},
        return_document=pymongo.ReturnDocument.AFTER, upsert=True,
    )
    
    recalibrate()


def recalibrate() -> None:
    current_state: dict[str, str] | None = _get_object()
    if current_state == None:
        log("Could not recalibrate; '_get_object()' returned 'None'")
        return
    
    for key in _KEYS:
        _set_light(key[0], key[1], current_state[key])


def _is_connected_to_internet(host="8.8.8.8", port=53, timeout=3) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False
    

def _check_database() -> None:
    if _COLLECTION.estimated_document_count() == 1:
        entry: dict[str, str] | None = _get_object()
        if entry is not None:
            if sorted(entry.keys()) == sorted(_KEYS + ['_id', 'accessID']):
                log("Database is properly initialized.")
                return
    log("WARNING: Database needs to be re-setup.")
    _COLLECTION.delete_many({})
    reset()


    
def _on_database_change(change_object: dict[str, str]) -> None:
    if SerialHandler.is_connected():
        return 
    
    for row_col in change_object:
        row: str = row_col[0]
        col: str = row_col[1]
        new_value: list[int, int, int] = change_object[row_col]
        _set_light(row, col, new_value)


def _set_light(row: str, col: str, state: list[int, int, int]) -> None:
    _local_state[row + col] = state
    # _display_to_console()
    if __name__ != "__main__":
        LEDHandler.set_light(row + col, state)
    


def _get_object() -> dict[str, str] | None:
    return _COLLECTION.find_one(_ACCESS_QUERY)


def _display_to_console() -> None:
    s: str = ''
    for i in range(len(_KEYS)):
        if i % 4 == 0:
            s += "\n"
        try:
            t: list[int, int, int] = _local_state[_KEYS[i]]
            s += str(ColorHandler.rgb_to_hex(t)) + " "
        except KeyError:
            s += '#ZZZZZZ '
    log(s)
    






if __name__ == "__main__":
    try:
        init_db()
        db_listen()
    except KeyboardInterrupt:
        close()
        