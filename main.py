import pymongo

URI = "mongodb+srv://admin:j2MzVYcewmPjnzrG@linkedpad.qrzkm98.mongodb.net/?retryWrites=true&w=majority&appName=linkedpad";
ACCESS_QUERY = { 'accessID': ':3' }

def get_keys():
    rows = ["A", "B", "C", "D"]
    columns = ["0", "1", "2", "3"]
    
    out = []
    
    for row in rows:
        for col in columns:
            out.append(row + col)
    return out
KEYS = get_keys()


def get_default_obj(): 
    o = {}
    for key in KEYS:
        o[key] = 0
    key = list(ACCESS_QUERY.keys())[0]
    o[key] = ACCESS_QUERY[key]
    return o
DEFAULT_DB_OBJ = get_default_obj()
        
local_state = {}




client = pymongo.MongoClient(URI)
database = client.get_database('pad_data')
collection = database.get_collection('data')



def init():
    print("Initializing...")
    check_database()
    collection.find_one({})
    recalibrate()
    listen()
    
    
    
    
def check_database():
    if (collection.estimated_document_count() == 1):
        entry = get_object()
        
        if entry != None:
            if sorted(entry.keys()) == sorted(KEYS + ['_id', 'accessID']):
                print("Database is properly initialized.")
                return
    print("WARNING: Database needs to be re-setup.")
    collection.delete_many({})
    reset()
    
def listen():
    try:    
        with collection.watch() as stream:
            for change in stream:
                on_database_change(change['updateDescription']['updatedFields'])
                
    except pymongo.errors.PyMongoError as e:
        client.close()
        
def on_database_change(change_object):
    for row_col in change_object:
        row = row_col[0]
        col = row_col[1]
        new_value = change_object[row_col]
        set_light(row, col, new_value)
            

def reset():
    result = collection.find_one_and_update(
        ACCESS_QUERY,
        { '$set': DEFAULT_DB_OBJ },
        return_document='after', upsert=True,
    )
    
    for key in result:
        set_light(key[0], key[1], 0)
    
def recalibrate():
    current_state = get_object()
    for key in KEYS:
        set_light(key[0], key[1], current_state[key])

def set_light(row, col, isOn):
    local_state[row + col] = isOn
    displayStateToConsole()



        
def get_object():
    return collection.find_one(ACCESS_QUERY)


def displayStateToConsole():
    s = ''

    for i in range(len(KEYS)):
        if (i % 4 == 0):
            s += "\n"
        
        try:
            t = local_state[KEYS[i]]
            s += '1 ' if  t > 0 else '0 '
        except KeyError:
            s += '0 '

    
    print(s)


init()