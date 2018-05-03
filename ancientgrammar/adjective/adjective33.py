from ancientgrammar.adjective.adjective import Adjective
from ancientgrammar.qualifiers import Case, Gender, Degree
from ancientgrammar.data import NENDINGS

class Adjective33(Adjective):
    def decline(self, gender:Gender, number:bool, case:Case):
        if gender == Gender.FEMININE:
            gender = Gender.MASCULINE
        return super().decline(gender, number, case)