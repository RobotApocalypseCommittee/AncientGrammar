from ancientgrammar.data import NENDINGS
from ancientgrammar.noun.noun import Noun
from ancientgrammar.qualifiers import Gender, Case

class Noun3(Noun):
    def __init__(self, nominative: str, vocative: str, genitive: str, dative_plural: str, gender: Gender, **kwargs):
        super().__init__(nominative, genitive, gender, **kwargs)
        self.vocative = vocative
        self.gen_stem = genitive[:-2]
        self.dative_plural = dative_plural

    def decline(self, case: Case, is_plural: bool):
        gender = self.gender if self.gender is not Gender.FEMININE else Gender.MASCULINE
        ending = NENDINGS["NOUN_3"][gender.name][int(is_plural)][int(case)]

        if ending == "nom":
            return self.nominative
        elif ending == "voc":
            return self.vocative
        elif ending == "dat":
            return self.dative_plural
        else:
            return self.gen_stem + ending
