from ancientgrammar.noun.noun1 import Noun1
from ancientgrammar.qualifiers import Gender
def get_noun(nominative, genitive, gender:Gender=None, **kwargs):
    if nominative.endswith("η"):
        return Noun1(nominative, Gender.FEMININE)
    elif nominative.endswith("α"):
        if genitive.endswith("ης"):
            return Noun1(nominative, Gender.FEMININE, halfalphapure=True)
        else:
            return Noun1(nominative, Gender.FEMININE)
    elif nominative.endswith("ης") or nominative.endswith("ας"):
        return Noun1(nominative, Gender.MASCULINE)
    else:
        raise NotImplementedError("This is an unrecognised noun type as of now.")
    