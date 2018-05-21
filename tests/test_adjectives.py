from ancientgrammar.adjective import get_adjective, determine_type, AdjectivalError
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
    "alpha212": [
        param(Gender.FEMININE, 0, Case.ACCUSATIVE, Degree.POSITIVE, "μικραν", id="halpha212"),
        param(Gender.FEMININE, 0, Case.GENITIVE, Degree.POSITIVE, "μικρας", id="halpha212gen"),
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
    ],
    "a313": [
        param(Gender.FEMININE, 0, Case.ACCUSATIVE, Degree.POSITIVE, "βραδειαν", id="basic313"),
    ],
    "a22": {
        param(Gender.FEMININE, 0, Case.ACCUSATIVE, Degree.POSITIVE, "αδικον", id="basic22"),
    },
    # TODO: This is Tuesday
    "type_determine": [
        param(["σοφος", "σοφη", "σοφον"], "212", id="typedetermine212"),
        param(["δυστυχης", "δυστυχες"], "33", id="typedetermine33"),
        param(["αδικος", "αδικον"], "22", id="typedetermine22"),
        param(["βραδυς", "βραδεια", "βραδυ"], "313", id="typedetermine313"),

    ]
}


@pytest.mark.parametrize("g,n,c,d,expected", ADJECTIVE_TESTS["a212"])
def test_basic_adjective(g,n,c,d,expected):
    adj = get_adjective(["σοφος", "σοφη", "σοφον"])
    assert adj.decline(g, n, c, d) == expected

@pytest.mark.parametrize("g,n,c,d,expected", ADJECTIVE_TESTS["l212"])
def test_adjective_long_last_vowel(g, n, c, d, expected):
    adj = get_adjective(["δεινος", "δεινη", "δεινον"], "212", last_syll_long=True)
    assert adj.decline(g, n, c, d) == expected

@pytest.mark.parametrize("g,n,c,d,expected", ADJECTIVE_TESTS["alpha212"])
def test_adjective_long_last_vowel(g, n, c, d, expected):
    adj = get_adjective(["μικρος", "μικρα", "μικρον"], "212", last_syll_long=True)
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

@pytest.mark.parametrize("g,n,c,d,expected", ADJECTIVE_TESTS["a313"])
def test_313_adjective(g, n, c, d, expected):
    adj = get_adjective(["βραδυς", "βραδεια", "βραδυ"], "313")
    assert adj.decline(g, n, c, d) == expected

@pytest.mark.parametrize("g,n,c,d,expected", ADJECTIVE_TESTS["a22"])
def test_22_adjective(g, n, c, d, expected):
    adj = get_adjective(["αδικος", "αδικον"], "22")
    assert adj.decline(g, n, c, d) == expected

def test_irregular_comparative():
    comparative = get_adjective(["μειζων"], "33")
    adj = get_adjective(["αγαθος", "αγαθη", "αγαθον"], "212", comparative=comparative)
    assert adj.decline(Gender.MASCULINE, 0, Case.GENITIVE, Degree.COMPARATIVE) == "μειζονος"

def test_irregular_superlative():
    superlative = get_adjective(["αριστος", "αριστη", "αριστον"], "212")
    adj = get_adjective(["αγαθος", "αγαθη", "αγαθον"], "212", superlative=superlative)
    assert adj.decline(Gender.MASCULINE, 0, Case.GENITIVE, Degree.SUPERLATIVE) == "αριστου"

@pytest.mark.parametrize("parts,expected", ADJECTIVE_TESTS["type_determine"])
def test_type_determination(parts, expected):
    assert determine_type(parts) == expected

def test_errors():
    with pytest.raises(NotImplementedError):
        adj = get_adjective(["noot"])
    with pytest.raises(AdjectivalError):
        adj = get_adjective(["noot"], "33")
    with pytest.raises(NotImplementedError):
        adj = get_adjective([], "230498")

