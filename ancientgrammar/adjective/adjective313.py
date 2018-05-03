from ancientgrammar.adjective.adjective import Adjective
from ancientgrammar.qualifiers import Case, Gender, Degree
from ancientgrammar.data import NENDINGS

class Adjective313(Adjective):
    def __init__(self, nom:str, stem:str, endings:list, **options):
        super().__init__(stem, endings, **options)
        self.nom = nom
        self.fem = fem

    def decline(self, gender:Gender, number:bool, case:Case):
        