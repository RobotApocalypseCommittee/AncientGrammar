import json

# noinspection PyPackageRequirements
import pytest

from ancientgrammar.qualifiers import Case, Gender
from ancientgrammar.verbs.verb import Tense, Mood, Voice
from ancientgrammar.verbs.verbregular import RegularVerb
from tests.data import path_to_test
from tests.utils import CASE_REFERENCE, GENDER_REFERENCE, MOOD_REFERENCE, TENSE_REFERENCE, VOICE_REFERENCE

TESTS = json.load(open(path_to_test("verb_tests.json"), "r", encoding="utf-8"))

REGULAR_TESTS = {"FINITE": [], "IMPERATIVE": [], "INFINITIVE": [], "PARTICIPLE": []}

for full_verb in TESTS:
    verb_object = RegularVerb(full_verb["present"], full_verb["future"], full_verb["aorist"],
                              full_verb["aorist_passive"], full_verb["preposition"],
                              full_verb["uncommon_epsilon"] == "True")

    if full_verb["tests"].get("REGULAR_FINITE") is not None:
        for test in full_verb["tests"]["REGULAR_FINITE"]:
            test_info_list = [verb_object, TENSE_REFERENCE[test["tense"]], MOOD_REFERENCE[test["mood"]],
                              VOICE_REFERENCE[test["voice"]], test["person"], test["plural"] == "True",
                              test["expected"]]

            REGULAR_TESTS["FINITE"].append(test_info_list)

    if full_verb["tests"].get("REGULAR_IMPERATIVE") is not None:
        for test in full_verb["tests"]["REGULAR_IMPERATIVE"]:
            test_info_list = [verb_object, TENSE_REFERENCE[test["tense"]], VOICE_REFERENCE[test["voice"]],
                              test["plural"] == "True", test["autocontract"] == "True",
                              test["expected"]]

            REGULAR_TESTS["IMPERATIVE"].append(test_info_list)

    if full_verb["tests"].get("REGULAR_INFINITIVE") is not None:
        for test in full_verb["tests"]["REGULAR_INFINITIVE"]:
            test_info_list = [verb_object, TENSE_REFERENCE[test["tense"]], VOICE_REFERENCE[test["voice"]],
                              test["autocontract"] == "True", test["expected"]]

            REGULAR_TESTS["INFINITIVE"].append(test_info_list)

    if full_verb["tests"].get("REGULAR_PARTICIPLE") is not None:
        for test in full_verb["tests"]["REGULAR_PARTICIPLE"]:
            test_info_list = [verb_object, TENSE_REFERENCE[test["tense"]], VOICE_REFERENCE[test["voice"]],
                              GENDER_REFERENCE[test["gender"]], test["plural"] == "True", CASE_REFERENCE[test["case"]],
                              test["expected"]]

            REGULAR_TESTS["PARTICIPLE"].append(test_info_list)


@pytest.mark.parametrize('test_verb, tense, mood, voice, person, is_plural, expected', REGULAR_TESTS["FINITE"])
def test_regular_verb_finite(test_verb: RegularVerb, tense: Tense, mood: Mood,
                             voice: Voice, person: int, is_plural: bool, expected: str):
    assert expected == test_verb.get_finite_form(tense, mood, voice, person, is_plural)


@pytest.mark.parametrize('test_verb, tense, voice, is_plural, autocontract, expected', REGULAR_TESTS["IMPERATIVE"])
def test_regular_verb_imperative(test_verb: RegularVerb, tense: Tense, voice: Voice,
                                 is_plural: bool, autocontract: bool, expected: str):
    assert expected == test_verb.get_imperative(tense, voice, is_plural, autocontract=autocontract)


@pytest.mark.parametrize('test_verb, tense, voice, autocontract, expected', REGULAR_TESTS["INFINITIVE"])
def test_regular_verb_infinitive(test_verb: RegularVerb, tense: Tense, voice: Voice,
                                 autocontract: bool, expected: str):
    assert expected == test_verb.get_infinitive(tense, voice, autocontract=autocontract)


@pytest.mark.parametrize('test_verb, tense, voice, gender, is_plural, case, expected', REGULAR_TESTS["PARTICIPLE"])
def test_regular_verb_participle(test_verb: RegularVerb, tense: Tense, voice: Voice,
                            gender: Gender, is_plural: bool, case: Case, expected: str):
    assert expected == test_verb.get_participle(tense, voice).decline(gender, is_plural, case)
