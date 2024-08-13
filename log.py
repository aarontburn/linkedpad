import inspect


def log(message) -> None:
    filename = inspect.stack()[1].filename.split("\\")[-1].split('.')[0]
    
    print(filename + ": " + str(message))
    