import pymongo
import LEDHandler

_URI: str = "mongodb+srv://admin:j2MzVYcewmPjnzrG@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad"
_CLIENT = pymongo.MongoClient(_URI)
_DATABASE = _CLIENT.get_database('pad_data')
_COLLECTION = _DATABASE.get_collection('data')

_ACCESS_QUERY: dict[str, str] = {'accessID': ':3'}

_KEYS: list[str] = [row + col for row in ["A", "B", "C", "D"] for col in ["0", "1", "2", "3"]]


def _get_default_obj() -> dict:
    o = {}
    for key in _KEYS:
        o[key] = 0
    key = list(_ACCESS_QUERY.keys())[0]
    o[key] = _ACCESS_QUERY[key]
    return o


_DEFAULT_DB_OBJ: dict = _get_default_obj()

_local_state: dict[str, str] = {}


def test():
    print(_CLIENT)
    print("\n")
    print(_DATABASE)
    print("\n")
    print(_COLLECTION)


def init_db() -> None:
    print("Initializing database handler...")
    
    _check_database()
    _COLLECTION.find_one({})
    recalibrate()

    print("Database initialization finished.")


def db_listen() -> None:
    print("Database listener started.")
    try:
        with _COLLECTION.watch() as stream:
            for change in stream:
                _on_database_change(change['updateDescription']['updatedFields'])
    except Exception as e:
        print("Database closing...")
        print(e)
        _CLIENT.close()


def on_key_press(row: str, col: str) -> None:
    _COLLECTION.find_one_and_update(_ACCESS_QUERY, {"$bit": {row + col: {'xor': 1}}})


def close() -> None:
    _CLIENT.close()
    

def reset() -> None:
    _COLLECTION.find_one_and_update(
        _ACCESS_QUERY,
        {'$set': _DEFAULT_DB_OBJ},
        return_document='after', upsert=True,
    )
    
    recalibrate()


def recalibrate() -> None:
    current_state: dict[str, str] | None = _get_object()
    if current_state == None:
        print("Could not recalibrate; '_get_object()' returned 'None'")
        return
    
    for key in _KEYS:
        _set_light(key[0], key[1], current_state[key])


def _check_database() -> None:
    if _COLLECTION.estimated_document_count() == 1:
        entry: dict[str, str] | None = _get_object()
        if entry is not None:
            if sorted(entry.keys()) == sorted(_KEYS + ['_id', 'accessID']):
                print("Database is properly initialized.")
                return
    print("WARNING: Database needs to be re-setup.")
    _COLLECTION.delete_many({})
    reset()


def _on_database_change(change_object: dict[str, str]) -> None:
    for row_col in change_object:
        row: str = row_col[0]
        col: str = row_col[1]
        new_value: str = change_object[row_col]
        _set_light(row, col, new_value)


def _set_light(row: str, col: str, state) -> None:
    print(state)
    print(type(state))
    _local_state[row + col] = state
    
    if (row + col == "A0"):
        if state == '1':
            LEDHandler.set_light(0, (255,255,255))
        else:
            LEDHandler.set_light(0, (0, 0, 0))
        
    
    _displayStateToConsole()


def _get_object() -> dict[str, str] | None:
    return _COLLECTION.find_one(_ACCESS_QUERY)


def _displayStateToConsole() -> None:
    s: str = ''
    for i in range(len(_KEYS)):
        if i % 4 == 0:
            s += "\n"
        try:
            t: str = _local_state[_KEYS[i]]
            s += '1 ' if t == '1' else '0 '
        except KeyError:
            s += '0 '
    print(s)
