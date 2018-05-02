from ancientgrammar.data import path_to_file
import json

with open(path_to_file("nendings.json"), encoding="utf-8") as f:
    obj = json.load(f)
    alpha = obj["STANDARD_212"]
    alpha["FEMININE"][0] = obj["ALHPA_212"][0]
    obj["ALPHA_212"] = alpha
    halpha = obj["STANDARD_212"]
    halpha["FEMININE"][0] = obj["HALHPA_212"][0]
    obj["HALPHA_212"] = halpha
    
NENDINGS = obj