import pytest
from pytest import param

from ancientgrammar.noun import get_noun, determine_gender
from ancientgrammar.qualifiers import Case, Gender

NOUN_TESTS = {
    "basicmasc": [
        param("ναυτης", "ναυτου", Case.ACCUSATIVE, 0, "ναυτην", id="basic1masc_acc"),
        param("νεανιας", "νεανιου", Case.ACCUSATIVE, 0, "νεανιαν", id="basic1masc_acc_alpha"),
        param("λογος", "λογου", Case.NOMINATIVE, 0, "λογος", id="basic2masc_nom")
    ],
    "basicfem": [
        param("τιμη", "τιμης", Case.NOMINATIVE, 0, "τιμη", id="basic1fem_nom"),
        param("χωρα", "χωπας", Case.NOMINATIVE, 0, "χωρα", id="basic1fem_nom_alpha"),
        param("χωρα", "χωπας", Case.DATIVE, 0, "χωρᾳ", id="basic1fem_dat_alpha"),
        param("θαλασσα", "θαλασσης", Case.DATIVE, 0, "θαλασσῃ", id="basic1fem_dat_halpha")
    ],
    "basicneut": [
        param("δωρον", "δωρου", Case.NOMINATIVE, 1, "δωρα", id="basic2neut_nom")
    ],
    "genderdetermination": [
        param("λογος", "λογου", Gender.MASCULINE, id="gender_masc2"),
        param("τιμη", "τιμης", Gender.FEMININE, id="gender_fem1"),
        param("κριτης", "κριτης", Gender.MASCULINE, id="gender_masc1"),
        param("θαλλασσα", "θαλλασσης", Gender.FEMININE, id="gender_fem1ha")
    ],
    "full_gender_determination": [
        param("τεκνον", "τεκνου", Case.ACCUSATIVE, 1, "τεκνα", id="full_gender_neut1")
    ],
    "3rd_dec": [
        param("γερων", "γερον", "γεροντος", "γερουσι", Gender.MASCULINE,
              Case.ACCUSATIVE, False, "γεροντα", id="3rd_masc1"),
        param("γερων", "γερον", "γεροντος", "γερουσι", Gender.MASCULINE,
              Case.VOCATIVE, False, "γερον", id="3rd_masc2"),
        param("γερων", "γερον", "γεροντος", "γερουσι", Gender.MASCULINE,
              Case.NOMINATIVE, False, "γερων", id="3rd_masc3"),
        param("ὀνομα", "ὀνομα", "ὀνοματος", "ὀνομασι", Gender.NEUTER,
              Case.ACCUSATIVE, False, "ὀνομα", id="3rd_neut1"),
        param("ὀνομα", "ὀνομα", "ὀνοματος", "ὀνομασι", Gender.NEUTER,
              Case.DATIVE, True, "ὀνομασι", id="3rd_neut2"),
        param("τειχος", "τειχος", "τειχεος", "τειχεσι", Gender.NEUTER,
              Case.ACCUSATIVE, True, "τειχη", id="3rd_neut_eps1"),
        param("τειχος", "τειχος", "τειχεος", "τειχεσι", Gender.NEUTER,
              Case.GENITIVE, False, "τειχους", id="3rd_neut_eps2"),
    ],
    "not_implemented": [
        param("βασιλευς", "βασιλεια", Gender.MASCULINE, id="not_implemented1")
    ],
    "irregular_noun": [
        # Yes, I know; TODO: MAKE NICER BY 2000%
        param("ναυς", "νεως", Gender.MASCULINE, [
            ["ναυς", None, "ναυν", "νεως", "νηι"],
            ["νηες", None, "ναυς", "νεων", "ναυσι"]
        ], Case.GENITIVE, False, "νεως", id="irregularNAUS")

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


@pytest.mark.parametrize("nominative, genitive, case, is_plural, expected", NOUN_TESTS["full_gender_determination"])
def test_full_gender_determination(nominative, genitive, case, is_plural, expected):
    assert expected == get_noun(nominative, genitive).decline(case, is_plural)


@pytest.mark.parametrize('nominative, vocative, genitive, dative_plural, gender, case, is_plural, expected',
                         NOUN_TESTS["3rd_dec"])
def test_third_declension(nominative, vocative, genitive, dative_plural, gender, case, is_plural, expected):
    noun = get_noun(nominative, genitive, gender, third=True, vocative=vocative, dative_plural=dative_plural)
    assert expected == noun.decline(case, is_plural)


@pytest.mark.parametrize("nominative, genitive, gender", NOUN_TESTS["not_implemented"])
def test_not_implemented(nominative, genitive, gender):
    with pytest.raises(NotImplementedError):
        get_noun(nominative, genitive, gender)


@pytest.mark.parametrize("nominative, genitive, gender, forms, case, is_plural, expected",
                         NOUN_TESTS["irregular_noun"])
def test_irregular(nominative, genitive, gender, forms, case, is_plural, expected):
    noun = get_noun(nominative, genitive, gender, irregular_forms=forms)
    assert expected == noun.decline(case, is_plural)

def test_unimplemented_forms():
    noun = get_noun("ναυς", "νεως", Gender.MASCULINE, irregular_forms=[
            ["ναυς", None, "ναυν", "νεως", "νηι"],
            ["νηες", None, "ναυς", "νεων", "ναυσι"]
        ])
    with pytest.raises(NotImplementedError):
        noun.decline(Case.VOCATIVE, False)
