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
    ],
    "w33": [
        param(Gender.FEMININE, 0, Case.ACCUSATIVE, "μειζονα", id="wnbasic33")
    ],
    "norm313": [
        param(Gender.NEUTER, 0, Case.ACCUSATIVE, "παυον", id="participlepresent313neut"),
        param(Gender.MASCULINE, 0, Case.ACCUSATIVE, "παυοντα", id="participlepresent313masc")
    ],
    "weak313": [
        param(Gender.FEMININE, 0, Case.DATIVE, "παυσασῃ", id="participleaorist313fem"),
        param(Gender.MASCULINE, 0, Case.GENITIVE, "παυσαντος", id="participleaorist313masc")
    ],
    "pass313": [
        param(Gender.FEMININE, 1, Case.GENITIVE, "παυσθεισων", id="participlepass313fem"),
        param(Gender.MASCULINE, 0, Case.GENITIVE, "παυσθεντος", id="participlepass313masc")
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

@pytest.mark.parametrize("g,n,c,expected", ADJECTIVE_TESTS["w33"])
def test_33_comparative(g, n, c, expected):
    adj = get_adjective(["μειζων"], "33")
    assert adj.decline(g, n, c) == expected

@pytest.mark.parametrize("g,n,c,expected", ADJECTIVE_TESTS["norm313"])
def test_313_participle_normal(g, n, c, expected):
    adj = get_adjective(["παυων", "παυουσα", "παυον"], "313")
    assert adj.decline(g, n, c) == expected

@pytest.mark.parametrize("g,n,c,expected", ADJECTIVE_TESTS["weak313"])
def test_313_participle_weak(g, n, c, expected):
    adj = get_adjective(["παυσας", "παυσασα", "παυσαν"], "313")
    assert adj.decline(g, n, c) == expected
