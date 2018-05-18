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
