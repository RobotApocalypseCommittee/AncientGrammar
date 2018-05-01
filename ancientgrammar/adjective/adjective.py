from ..qualifiers import Gender, Case

class Adjective:
    def __init__(self, parts:list, **options):
        self.parts  = parts

    def decline(self, gender:Gender, number:bool, case:Case):
        pass
    
