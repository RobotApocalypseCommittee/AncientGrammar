from ancientgrammar.adjective import get_adjective
from ancientgrammar.qualifiers import Gender, Case, Degree
from pytest import param
import pytest
ADJECTIVE_TESTS = {
    "a212": [
        param(Gender.FEMININE, 0, Case.ACCUSATIVE, Degree.POSITIVE, "σοφην", id="basic212"),
        param(Gender.MASCULINE, 1, Case.DATIVE, Degree.COMPARATIVE, "σοφωτεροις", id="comparative212"),
        param(Gender.NEUTER, 1, Case.VOCATIVE, Degree.SUPERLATIVE, "σοφωτατα", id="superlative212")
    ],
    "l212": [
        param(Gender.MASCULINE, 0, Case.NOMINATIVE, Degree.COMPARATIVE, "δεινοτερος", id="longsyllcomp212"),
        param(Gender.MASCULINE, 0, Case.NOMINATIVE, Degree.SUPERLATIVE, "δεινοτατος", id="longsyllsup212")
    ],
    "a33": [
        param(Gender.FEMININE, 0, Case.ACCUSATIVE, Degree.POSITIVE, "δυστυχη", id="basic33")
    ]
}


@pytest.mark.parametrize("g,n,c,d,expected", ADJECTIVE_TESTS["a212"])
def test_basic_adjective(g,n,c,d,expected):
    adj = get_adjective(["σοφος", "σοφη", "σοφον"], "212")
    assert adj.decline(g, n, c, d) == expected

@pytest.mark.parametrize("g,n,c,d,expected", ADJECTIVE_TESTS["l212"])
def test_adjective_long_last_vowel(g, n, c, d, expected):
    adj = get_adjective(["δεινος", "δεινη", "δεινον"], "212", last_syll_long=True)
    assert adj.decline(g, n, c, d) == expected

@pytest.mark.parametrize("g,n,c,d,expected", ADJECTIVE_TESTS["a33"])
def test_33_adjective(g, n, c, d, expected):
    adj = get_adjective(["δυστυχης"], "33")
    assert adj.decline(g, n, c, d) == expected




