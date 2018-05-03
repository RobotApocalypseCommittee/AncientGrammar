import os.path

def path_to_test(fname:str):
    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, fname)
    return path