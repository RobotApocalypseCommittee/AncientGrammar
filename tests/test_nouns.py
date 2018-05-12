from ancientgrammar.noun import get_noun
from ancientgrammar.qualifiers import Case
from pytest import param
import pytest

NOUN_TESTS = {
    "basic1f": [
        param(Case.NOMINATIVE, 0, "τιμη", id="basic1fnominative")
    ],
    "basic1m": [
        param(Case.ACCUSATIVE, 0, "ναυτην", id="basic1macc")
    ]
}

@pytest.mark.parametrize("case,plural,expected", NOUN_TESTS["basic1f"])
def test_1declf(case, plural, expected):
    noun = get_noun("τιμη", "τιμης")
    assert noun.decline(case, plural) == expected

@pytest.mark.parametrize("case,plural,expected", NOUN_TESTS["basic1m"])
def test_1declm(case, plural, expected):
    noun = get_noun("ναυτης", "ναυτου")
    assert noun.decline(case, plural) == expected