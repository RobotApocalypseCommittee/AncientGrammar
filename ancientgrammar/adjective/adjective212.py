from .adjective import Adjective
from .endings import STANDARD_121
from ..qualifiers import *
class Adjective212(Adjective):
    def __init__(self, parts:list):
        super().__init__(parts)
        self.stem = parts[0][:-2] # Witness the smile?

    def decline(self, gender:Gender, number:bool, case:Case):
        index = case if not number else case + 5
        ending = STANDARD_121[gender][index]
        return self.stem + ending
