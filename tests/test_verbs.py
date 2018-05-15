import json

import pytest

from ancientgrammar.qualifiers import Case, Gender
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

GENDER_REFERENCE = {
    "MASCULINE":Gender.MASCULINE,
    "FEMININE":Gender.FEMININE,
    "NEUTER":Gender.NEUTER
}

CASE_REFERENCE = {
    "NOMINATIVE":Case.NOMINATIVE,
    "VOCATIVE":Case.VOCATIVE,
    "ACCUSATIVE":Case.ACCUSATIVE,
    "GENETIVE":Case.GENITIVE,
    "DATIVE":Case.DATIVE
}

TESTS = json.load(open(path_to_test("verb_tests.json"), encoding="utf-8"))

REGULAR_FINITE_TESTS = []
REGULAR_PARTICIPLE_TESTS = []

for full_verb in TESTS:
    verb_object = RegularVerb(full_verb["present"], full_verb["future"], full_verb["aorist"],
                              full_verb["aorist_passive"], full_verb["preposition"], full_verb["uncommon_epsilon"])

    if full_verb["tests"].get("REGULAR_FINITE") is not None:
        for test in full_verb["tests"]["REGULAR_FINITE"]:
            test_info_list = [verb_object]

            test_info_list.append(TENSE_REFERENCE[test["tense"]])
            test_info_list.append(MOOD_REFERENCE[test["mood"]])
            test_info_list.append(VOICE_REFERENCE[test["voice"]])
            test_info_list.append(test["person"])
            test_info_list.append(test["plural"] == "True")
            test_info_list.append(test["expected"])

            REGULAR_FINITE_TESTS.append(test_info_list)
    
    if full_verb["tests"].get("REGULAR_PARTICIPLE") is not None:
        for test in full_verb["tests"]["REGULAR_PARTICIPLE"]:
            test_info_list = [verb_object]

            test_info_list.append(TENSE_REFERENCE[test["tense"]])
            test_info_list.append(VOICE_REFERENCE[test["voice"]])
            test_info_list.append(GENDER_REFERENCE[test["gender"]])
            test_info_list.append(test["plural"] == "True")
            test_info_list.append(CASE_REFERENCE[test["case"]])
            test_info_list.append(test["expected"])

            REGULAR_PARTICIPLE_TESTS.append(test_info_list)

@pytest.mark.parametrize('test_verb, tense, mood, voice, person, is_plural, expected', REGULAR_FINITE_TESTS)
def test_regular_verb_finite(test_verb: RegularVerb, tense: verb.Tense, mood: verb.Mood,
                             voice: verb.Voice, person: int, is_plural: bool, expected: str):

    assert test_verb.get_finite_form(tense, mood, voice, person, is_plural) == expected

@pytest.mark.parametrize('test_verb, tense, voice, gender, is_plural, case, expected', REGULAR_PARTICIPLE_TESTS)
def test_regular_participle(test_verb: RegularVerb, tense: verb.Tense, voice: verb.Voice,
                            gender: Gender, is_plural: bool, case:Case, expected: str):
    
    assert test_verb.get_participle(tense, voice).decline(gender, is_plural, case) == expected
