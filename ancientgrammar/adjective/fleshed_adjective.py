from ancientgrammar.adjective.adjective_creator import get_raw_adjective
from ancientgrammar.adjective.adjective import Adjective
from ancientgrammar.qualifiers import Case, Gender, Degree

class FleshedAdjective(Adjective):
    is_fleshed = True
    def __init__(self, adjective:Adjective):
        options = adjective.options
        super().__init__(adjective.stem, adjective.endings, **options)
        self.positive = adjective

        if "comparative" not in options:
            self.comparative = get_raw_adjective([self.stem+"ωτερος"], "212", has_adverb=True)
        else:
            if type(options["comparative"]) == str:
                self.comparative = get_raw_adjective([options["comparative"]], "212", has_adverb=True)
            else:
                self.comparative = options["comparative"]
        self.comparative.adverb = self.comparative.decline(Gender.NEUTER, 0, Case.NOMINATIVE)

        if "superlative" not in options:
            self.superlative = get_raw_adjective([self.stem+"ωτατος"], "212", has_adverb=True)
        else:
            if type(options["superlative"]) == str:
                self.superlative = get_raw_adjective([options["superlative"]], "212", has_adverb=True)
            else:
                self.superlative = options["superlative"]
        self.superlative.adverb = self.superlative.decline(Gender.NEUTER, 1, Case.NOMINATIVE)

    def decline(self, gender:Gender, number:bool, case:Case, degree:Degree = Degree.POSITIVE):
        if degree == Degree.POSITIVE:
            return self.positive.decline(gender, number, case)
        elif degree == Degree.COMPARATIVE:
            return self.comparative.decline(gender, number, case)
        elif degree == Degree.SUPERLATIVE:
            return self.superlative.decline(gender, number, case)
