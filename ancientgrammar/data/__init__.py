import os.path
import ancientgrammar.data.nendings

def path_to_file(fname:str):
    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, fname)
    return path

NENDINGS = ancientgrammar.data.nendings.NENDINGS