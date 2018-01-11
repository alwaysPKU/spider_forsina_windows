import os

def mkdir(path):
    if not os.path.exists(path):
        return os.makedirs(path)
    else:
        return path