from ancientgrammar.qualifiers import Case, Gender

class Noun:
    def __init__(self, nominative:str, genitive:str, gender:Gender, **kwargs):
        self.nominative = nominative
        self.genitive = genitive
        self.gender = gender
    def decline(self, case:Case, plural:bool):
        pass  # pragma: no cover
