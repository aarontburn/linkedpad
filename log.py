import inspect
import os


def log(*message) -> None:
    
    filename = os.path.normpath(inspect.stack()[1].filename).split("\\")[-1].split('.')[0]
    
    out: str = ''
    
    for s in message:
        out += ' ' + str(s)
    
    print(filename + ": " + out[1:])
    