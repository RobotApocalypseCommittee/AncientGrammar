from ancientgrammar.noun.noun import Noun
from ancientgrammar.qualifiers import Gender, Case

class Noun3(Noun):
    def __init__(self, nominative: str, genitive: str, gender: Gender, **kwargs):
        super().__init__(nominative, genitive, gender, **kwargs)
        self.nom_stem = nominative[:-2]
        self.gen_stem = genitive[:-2]

    def decline(self, case: Case, is_plural: bool):
        if is_plural and case is Case.NOMINATIVE or case is Case.VOCATIVE or \
           (case is Case.ACCUSATIVE and Gender is Gender.NEUTER):
            stem = self.nom_stem
        else:
            stem = self.gen_stem