from .adjective import Adjective
from .endings import STANDARD_212, ALPHA_212
from ..qualifiers import *
from ..utils import is_vowel
class Adjective212(Adjective):
    def __init__(self, parts:list, **options:dict):
        super().__init__(parts)
        self.stem = parts[0][:-2] # Witness the smile?
        if is_vowel(self.stem[-1]):
            self.endings = STANDARD_212
        else:
            self.endings = ALPHA_212

        if options.get("comparative", self.stem+""):
            pass


    def decline(self, gender:Gender, number:bool, case:Case, degree:Degree = Degree.POSITIVE):
        index = case if not number else case + 5
        ending = self.endings[gender][index]
        return self.stem + ending
