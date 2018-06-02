from ancientgrammar.noun.noun import Noun
from ancientgrammar.noun.noun1 import Noun1
from ancientgrammar.noun.noun2 import Noun2
from ancientgrammar.noun.noun3 import Noun3
from ancientgrammar.qualifiers import Gender
from ancientgrammar.utils import is_equal


def determine_gender(nominative, genitive):
    last_letter = nominative[-1]
    if is_equal(last_letter, "η") or is_equal(last_letter, "α"):
        return Gender.FEMININE
    elif is_equal(nominative[-2:], "ον"):
        return Gender.NEUTER
    else:
        return Gender.MASCULINE


def get_noun(nominative, genitive, gender: Gender=None, **kwargs):
    if gender is None:
        gender = determine_gender(nominative, genitive)
    if nominative.endswith("η") and gender == Gender.FEMININE:
        return Noun1(nominative, Gender.FEMININE, **kwargs)
    elif nominative.endswith("α") and gender == Gender.FEMININE:
        if genitive.endswith("ης"):
            return Noun1(nominative, Gender.FEMININE, halfalphapure=True, **kwargs)
        else:
            return Noun1(nominative, Gender.FEMININE, **kwargs)

    elif kwargs.get("third", False):
        # If this is set, vocative and dative_plural must be set
        return Noun3(nominative, kwargs.pop("vocative", None), genitive, kwargs.pop("dative_plural", None), gender, **kwargs)
    elif (is_equal(nominative[-2:], "ης") or is_equal(nominative[-2:], "ας")) and gender == Gender.MASCULINE:
        return Noun1(nominative, Gender.MASCULINE, **kwargs)
    elif nominative.endswith("ος") or nominative.endswith("ον"):
        return Noun2(nominative, gender, **kwargs)
    elif kwargs.get("irregular_forms", None) is not None:
        return Noun(nominative, genitive, gender, **kwargs)
    else:
        raise NotImplementedError("This is an unrecognised noun type as of now.")
