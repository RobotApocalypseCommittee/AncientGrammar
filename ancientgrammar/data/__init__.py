import os.path
import json
import copy

def path_to_file(fname:str):
    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, fname)
    return path

with open(path_to_file("nendings.json"), encoding="utf-8") as f:
    obj = json.load(f)

    # Alpha Pure Fleshing
    alpha = copy.deepcopy(obj["STANDARD_212"])
    alpha["FEMININE"][0] = obj["ALPHA_212"]["FEMININE"][0]
    obj["ALPHA_212"] = alpha
    
    # Half Alpha Pure Fleshing
    halpha = copy.deepcopy(obj["STANDARD_212"])
    halpha["FEMININE"][0] = obj["HALPHA_212"]["FEMININE"][0]
    obj["HALPHA_212"] = halpha

NENDINGS = obj