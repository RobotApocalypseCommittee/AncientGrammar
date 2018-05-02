import json

from ancientgrammar.qualifiers import Case, Gender, Degree
from ancientgrammar.utils import is_vowel
from ancientgrammar.data import path_to_file, NENDINGS



def get_adjective(parts, adjtype:str, **options):
    if len(parts) == 3:
        if adjtype == "212":
            # 212 Adjective
            stem = parts[0][:-2]
            ending = NENDINGS["STANDARD_212"]
            if is_vowel(stem[-1]):
                if "halfeta" in options and options["halfeta"]:
                    ending = NENDINGS["HALPHA_212"]
                else:
                    ending = NENDINGS["ALPHA_212"]
            return Adjective(stem, ending, **options)

class Adjective:
    def __init__(self, stem:str, endings:list, **options):
        self.stem = stem
        self.endings = endings


    def decline(self, gender:Gender, number:bool, case:Case):
        ending = self.endings[gender.name][int(number)][int(case)]
        return self.stem + ending

