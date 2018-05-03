from ancientgrammar.adjective.adjective import Adjective
from ancientgrammar.qualifiers import Case, Gender, Degree
from ancientgrammar.data import NENDINGS

class FleshedAdjective(Adjective):
    def __init__(self, adjective:Adjective):
        options = adjective.options
        super().__init__(adjective.stem, adjective.endings, **options)
        self.positive = adjective

        if "comparative" not in options:
            self.comparative = Adjective(self.stem+"ωτερ", NENDINGS["ALPHA_212"])
        else:
            if type(options["comparative"]) == str:
                self.comparative = Adjective(
                    options["comparative"][:-2], 
                    NENDINGS["ALPHA_212"])
            else:
                self.comparative = options["comparative"]

        if "superlative" not in options:
            self.superlative = Adjective(self.stem+"ωτατ", NENDINGS["STANDARD_212"])
        else:
            if type(options["superlative"]) == str:
                self.superlative = Adjective(
                    options["superlative"][:-2], 
                    NENDINGS["STANDARD_212"])
            else:
                self.superlative = options["superlative"]

    def decline(self, gender:Gender, number:bool, case:Case, degree:Degree = Degree.POSITIVE):
        if degree == Degree.POSITIVE:
            return self.positive.decline(gender, number, case)
        elif degree == Degree.COMPARATIVE:
            return self.comparative.decline(gender, number, case)
        elif degree == Degree.SUPERLATIVE:
            return self.superlative.decline(gender, number, case)
