from ancientgrammar.qualifiers import Case, Gender, Degree
from ancientgrammar.utils import is_vowel
from ancientgrammar.data import path_to_file, NENDINGS

class Adjective:
    def __init__(self, stem:str, endings:list, **options):
        self.stem = stem
        self.endings = endings
        self.options = options
        if "adverb" in options:
            self.adverb = options["adverb"]
        else:
            self.adverb = None


    def decline(self, gender:Gender, number:bool, case:Case):
        ending = self.endings[gender.name][int(number)][int(case)]
        return self.stem + ending



