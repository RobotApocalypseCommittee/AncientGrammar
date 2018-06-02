from ancientgrammar.noun.noun import Noun
from ancientgrammar.qualifiers import Gender, Case
from ancientgrammar.utils import is_vowel, alpha_purify
from ancientgrammar.data import NENDINGS


class Noun1(Noun):
    endings = NENDINGS["1declnoun"]

    def __init__(self, nominative, gender, **kwargs):
        super().__init__(nominative, None, gender)
        if gender == Gender.MASCULINE:
            self.stem = self.nominative[:-2]
        else:
            self.stem = self.nominative[:-1]

        if kwargs.get("halfalphapure", False):
            self.alpha = False
            self.halpha = True
        else:
            self.halpha = False
            self.alpha = Noun1.is_alpha_pure(nominative, gender)

    def decline_regular(self, case: Case, plural: bool):
        ending = self.endings[self.gender.name][int(plural)][int(case)]
        if not plural:
            if (
                    (self.halpha and (case == Case.NOMINATIVE or case == Case.ACCUSATIVE))
                    or self.alpha
            ):
                ending = alpha_purify(ending)

        return self.stem + ending

    @staticmethod
    def is_alpha_pure(nominative, gender):
        if gender == Gender.MASCULINE:
            stem = nominative[:-2]
        else:
            stem = nominative[:-1]

        return is_vowel(stem[-1])
