from ancientgrammar.data import NENDINGS
from ancientgrammar.noun.noun import Noun
from ancientgrammar.qualifiers import Gender, Case, ContractType
from ancientgrammar.utils import calculate_contraction, is_equal


class Noun3(Noun):
    def __init__(self, nominative: str, vocative: str, genitive: str, dative_plural: str, gender: Gender, **kwargs):
        super().__init__(nominative, genitive, gender, **kwargs)
        self.contract = ContractType.EPSILON if is_equal(self.genitive[-3:],
                                                         "εος") and gender is Gender.NEUTER else None
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
            return calculate_contraction(self.gen_stem, ending, self.contract)
