from ancientgrammar.noun import get_noun, determine_gender
from ancientgrammar.qualifiers import Case, Gender
from pytest import param

import pytest

NOUN_TESTS = {
    "basicmasc": [
        param("ναυτης", "ναυτου", Case.ACCUSATIVE, 0, "ναυτην", id="basic1masc_acc"),
        param("νεανιας", "νεανιου", Case.ACCUSATIVE, 0, "νεανιαν", id="basic1masc_acc_alpha"),
        param("λογος", "λογου", Case.NOMINATIVE, 0, "λογος", id="basic2masc_nom")
    ],
    "basicfem": [
        param("τιμη", "τιμης", Case.NOMINATIVE, 0, "τιμη", id="basic1fem_nom"),
        param("χωρα", "χωπας", Case.NOMINATIVE, 0, "χωρα", id="basic1fem_nom_alpha")
    ],
    "basicneut": [
        param("δωρον", "δωρου", Case.NOMINATIVE, 1, "δωρα", id="basic2neut_nom")
    ],
    "genderdetermination": [
        param("λογος", "λογου", Gender.MASCULINE, id="gender_masc2"),
        param("τιμη", "τιμης", Gender.FEMININE, id="gender_fem1"),
        param("κριτης", "κριτης", Gender.MASCULINE, id="gender_masc1"),
        param("θαλλασσα", "θαλλασσης", Gender.FEMININE, id="gender_fem1ha"),
    ]
}

@pytest.mark.parametrize("nominative,genitive,case,plural,expected", NOUN_TESTS["basicmasc"])
def test_masc(nominative, genitive, case, plural, expected):
    noun = get_noun(nominative, genitive, gender=Gender.MASCULINE)
    assert noun.decline(case, plural) == expected

@pytest.mark.parametrize("nominative,genitive,case,plural,expected", NOUN_TESTS["basicfem"])
def test_fem(nominative, genitive, case, plural, expected):
    noun = get_noun(nominative, genitive, gender=Gender.FEMININE)
    assert noun.decline(case, plural) == expected

@pytest.mark.parametrize("nominative,genitive,case,plural,expected", NOUN_TESTS["basicneut"])
def test_neut(nominative, genitive, case, plural, expected):
    noun = get_noun(nominative, genitive, gender=Gender.NEUTER)
    assert noun.decline(case, plural) == expected

@pytest.mark.parametrize("nominative,genitive,expected", NOUN_TESTS["genderdetermination"])
def test_gender_determination(nominative, genitive, expected):
    assert determine_gender(nominative, genitive) == expected