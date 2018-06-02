from ancientgrammar.qualifiers import Case, Gender

class Noun:
    def __init__(self, nominative:str, genitive:str, gender:Gender, **kwargs):
        self.nominative = nominative
        self.genitive = genitive
        self.gender = gender
        self.irregular_forms = kwargs.get("irregular_forms", [])
    def decline(self, case:Case, plural:bool):
        try:
            form = self.irregular_forms[int(plural)][int(case)]
        except IndexError:
            form = None
        if form is not None:
            return form
        else:
            return self.decline_regular(case, plural)

    def decline_regular(self, case, plural):
        raise NotImplementedError("This noun does not have this form registered.")

