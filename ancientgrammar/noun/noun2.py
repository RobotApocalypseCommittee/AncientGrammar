from ancientgrammar.noun.noun import Noun
from ancientgrammar.qualifiers import Gender, Case
from ancientgrammar.utils import is_vowel, alpha_purify
from ancientgrammar.data import NENDINGS

class Noun2(Noun):
    def __init__(self, nominative, gender, **kwargs):
        super().__init__(nominative, None, gender)
        # os or on
        self.stem = nominative[:-2]

    def decline_regular(self, case:Case, plural:bool):
        gender = self.gender if self.gender != Gender.FEMININE else Gender.MASCULINE
        ending = NENDINGS["STANDARD_212"][gender.name][int(plural)][int(case)]
        return self.stem + ending
