import inspect


def log(*message) -> None:
    
    filename = inspect.stack()[1].filename.replace("\\", '/').split("/")[-1].split('.')[0]
    
    out: str = ''
    
    for s in message:
        out += ' ' + str(s)
    
    print(filename + ": " + out[1:], flush=True)
    