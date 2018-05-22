# noinspection PyPackageRequirements
import pytest

from ancientgrammar.qualifiers import Case, Gender
from ancientgrammar.verbs import get_type
from ancientgrammar.verbs.verb import Tense, Mood, Voice, VerbType
from ancientgrammar.verbs.verbdeponent import DeponentVerb
from tests.verbs import TESTS
from tests.verbs.utils import CASE_REFERENCE, GENDER_REFERENCE, MOOD_REFERENCE, TENSE_REFERENCE, VOICE_REFERENCE, \
    convert_forms

DEPONENT_TESTS = {"FINITE": [], "IMPERATIVE": [], "INFINITIVE": [], "PARTICIPLE": []}

for full_verb in TESTS:
    if get_type(full_verb["present"], full_verb["future"], full_verb["aorist"]) is VerbType.DEPONENT:
        continue

    verb_object = DeponentVerb(full_verb["present"], full_verb["future"], full_verb["aorist"],
                               full_verb["aorist_passive"], full_verb["preposition"],
                               full_verb["uncommon_epsilon"] == "True", convert_forms(full_verb["allowed_forms"]))

    if full_verb["tests"].get("REGULAR_FINITE") is not None:
        for test in full_verb["tests"]["REGULAR_FINITE"]:
            test_info_list = [verb_object, TENSE_REFERENCE[test["tense"]], MOOD_REFERENCE[test["mood"]],
                              VOICE_REFERENCE[test["voice"]], test["person"], test["plural"] == "True",
                              test["expected"]]

            DEPONENT_TESTS["FINITE"].append(test_info_list)

    if full_verb["tests"].get("REGULAR_IMPERATIVE") is not None:
        for test in full_verb["tests"]["REGULAR_IMPERATIVE"]:
            test_info_list = [verb_object, TENSE_REFERENCE[test["tense"]], VOICE_REFERENCE[test["voice"]],
                              test["plural"] == "True", test["autocontract"] == "True",
                              test["expected"]]

            DEPONENT_TESTS["IMPERATIVE"].append(test_info_list)

    if full_verb["tests"].get("REGULAR_INFINITIVE") is not None:
        for test in full_verb["tests"]["REGULAR_INFINITIVE"]:
            test_info_list = [verb_object, TENSE_REFERENCE[test["tense"]], VOICE_REFERENCE[test["voice"]],
                              test["autocontract"] == "True", test["expected"]]

            DEPONENT_TESTS["INFINITIVE"].append(test_info_list)

    if full_verb["tests"].get("REGULAR_PARTICIPLE") is not None:
        for test in full_verb["tests"]["REGULAR_PARTICIPLE"]:
            test_info_list = [verb_object, TENSE_REFERENCE[test["tense"]], VOICE_REFERENCE[test["voice"]],
                              GENDER_REFERENCE[test["gender"]], test["plural"] == "True", CASE_REFERENCE[test["case"]],
                              test["expected"]]

            DEPONENT_TESTS["PARTICIPLE"].append(test_info_list)


@pytest.mark.parametrize('test_verb, tense, mood, voice, person, is_plural, expected', DEPONENT_TESTS["FINITE"])
def test_regular_verb_finite(test_verb: DeponentVerb, tense: Tense, mood: Mood,
                             voice: Voice, person: int, is_plural: bool, expected: str):
    assert expected == test_verb.get_finite_form(tense, mood, voice, person, is_plural)


@pytest.mark.parametrize('test_verb, tense, voice, is_plural, autocontract, expected', DEPONENT_TESTS["IMPERATIVE"])
def test_regular_verb_imperative(test_verb: DeponentVerb, tense: Tense, voice: Voice,
                                 is_plural: bool, autocontract: bool, expected: str):
    assert expected == test_verb.get_imperative(tense, voice, is_plural, autocontract=autocontract)


@pytest.mark.parametrize('test_verb, tense, voice, autocontract, expected', DEPONENT_TESTS["INFINITIVE"])
def test_regular_verb_infinitive(test_verb: DeponentVerb, tense: Tense, voice: Voice,
                                 autocontract: bool, expected: str):
    assert expected == test_verb.get_infinitive(tense, voice, autocontract=autocontract)


@pytest.mark.parametrize('test_verb, tense, voice, gender, is_plural, case, expected', DEPONENT_TESTS["PARTICIPLE"])
def test_regular_verb_participle(test_verb: DeponentVerb, tense: Tense, voice: Voice,
                                 gender: Gender, is_plural: bool, case: Case, expected: str):
    assert expected == test_verb.get_participle(tense, voice).decline(gender, is_plural, case)
