import json

import pytest

from ancientgrammar.verbs import verb
from ancientgrammar.verbs.verbregular import RegularVerb
from tests.data import path_to_test

TENSE_REFERENCE = {
    "FUTURE":verb.Tense.FUTURE,
    "PRESENT":verb.Tense.PRESENT,
    "IMPERFECT":verb.Tense.IMPERFECT,
    "AORIST":verb.Tense.AORIST
}

MOOD_REFERENCE = {
    "INDICATIVE":verb.Mood.INDICATIVE,
    "SUBJUNCTIVE":verb.Mood.SUBJUNCTIVE,
    "OPTATIVE":verb.Mood.OPTATIVE,
    "IMPERATIVE":verb.Mood.IMPERATIVE,
    "INFINITIVE":verb.Mood.INFINITIVE
}

VOICE_REFERENCE = {
    "ACTIVE":verb.Voice.ACTIVE,
    "MIDDLE":verb.Voice.MIDDLE,
    "PASSIVE":verb.Voice.PASSIVE
}

TESTS = json.load(open(path_to_test("verb_tests.json"), encoding="utf-8"))

REGULAR_FINITE_TESTS = []

for full_verb in TESTS["REGULAR"]:
    verb_object = RegularVerb(full_verb["present"], full_verb["future"], full_verb["aorist"],
                              full_verb["aorist_passive"], full_verb["preposition"], full_verb["uncommon_epsilon"])

    for test in full_verb["tests"]:
        test_info_list = [verb_object]

        test_info_list.append(TENSE_REFERENCE[test["tense"]])
        test_info_list.append(MOOD_REFERENCE[test["mood"]])
        test_info_list.append(VOICE_REFERENCE[test["voice"]])
        test_info_list.append(test["person"])
        test_info_list.append(test["plural"] == "True")
        test_info_list.append(test["expected"])

        REGULAR_FINITE_TESTS.append(test_info_list)

@pytest.mark.parametrize('test_verb, tense, mood, voice, person, is_plural, expected', REGULAR_FINITE_TESTS)
def test_regular_verb_finite(test_verb: RegularVerb, tense: verb.Tense, mood: verb.Mood,
                             voice: verb.Voice, person: int, is_plural: bool, expected: str):

    assert test_verb.get_finite_form(tense, mood, voice, person, is_plural) == expected
