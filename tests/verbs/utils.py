from ancientgrammar.verbs.verb import Mood, Tense, Voice
from ancientgrammar.qualifiers import Case, Gender

TENSE_REFERENCE = {
    "FUTURE": Tense.FUTURE,
    "PRESENT": Tense.PRESENT,
    "IMPERFECT": Tense.IMPERFECT,
    "AORIST": Tense.AORIST
}

MOOD_REFERENCE = {
    "INDICATIVE": Mood.INDICATIVE,
    "SUBJUNCTIVE": Mood.SUBJUNCTIVE,
    "OPTATIVE": Mood.OPTATIVE,
    "IMPERATIVE": Mood.IMPERATIVE,
    "INFINITIVE": Mood.INFINITIVE
}

VOICE_REFERENCE = {
    "ACTIVE": Voice.ACTIVE,
    "MIDDLE": Voice.MIDDLE,
    "PASSIVE": Voice.PASSIVE
}

GENDER_REFERENCE = {
    "MASCULINE": Gender.MASCULINE,
    "FEMININE": Gender.FEMININE,
    "NEUTER": Gender.NEUTER
}

CASE_REFERENCE = {
    "NOMINATIVE": Case.NOMINATIVE,
    "VOCATIVE": Case.VOCATIVE,
    "ACCUSATIVE": Case.ACCUSATIVE,
    "GENITIVE": Case.GENITIVE,
    "DATIVE": Case.DATIVE
}


def convert_args(args: list):
    return [convert_argument(val[0], val[1]) for val in args]


def convert_kwargs(kwargs: dict):
    return {key: convert_argument(val[0], val[1]) for (key, val) in kwargs.items()}


def convert_argument(proposed_type: str, value):
    if proposed_type == "bool":
        return value == "True"
    elif proposed_type == "Tense":
        return TENSE_REFERENCE[value]
    elif proposed_type == "Mood":
        return MOOD_REFERENCE[value]
    elif proposed_type == "Voice":
        return VOICE_REFERENCE[value]
    else:
        return value
