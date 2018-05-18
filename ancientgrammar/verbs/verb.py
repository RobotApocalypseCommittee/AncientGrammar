from enum import Enum, auto
import unicodedata

from ancientgrammar.utils import is_vowel, is_equal, remove_accents


class BaseVerbError(Exception):
    pass


class VerbParseError(BaseVerbError):
    pass


class VerbComputeError(BaseVerbError):
    pass


class Tense(Enum):
    FUTURE = auto()
    PRESENT = auto()
    IMPERFECT = auto()
    AORIST = auto()

    def is_aspect(self):
        return self in [Tense.PRESENT, Tense.AORIST]


class Mood(Enum):
    INDICATIVE = auto()
    SUBJUNCTIVE = auto()
    OPTATIVE = auto()
    IMPERATIVE = auto()
    INFINITIVE = auto()

    def is_finite(self):
        return self in [Mood.INDICATIVE, Mood.SUBJUNCTIVE, Mood.OPTATIVE]


class Voice(Enum):
    ACTIVE = auto()
    MIDDLE = auto()
    PASSIVE = auto()


class Verb:
    AUGMENTS = {
        "ᾳ": u"η\u0345",
        "αι": u"η\u0345",
        "ει": u"η\u0345",
        "αυ": "ηυ",
        "ευ": "ηυ",
        "α": "η",
        "ι": "ι",
        "ο": "ω",
        "οι": u"ω\u0345",
        "υ": "υ",
        "η": "η",
        "ω": "ω"
    }

    def get_finite_form(self, tense: Tense, mood: Mood, voice: Voice, person: int, is_plural: bool, autocontract: bool):
        pass  # pragma: no cover

    def get_imperative(self, aspect: Tense, voice: Voice, is_plural: bool, autocontract: bool):
        pass  # pragma: no cover

    def get_infinitive(self, tense: Tense, voice: Voice, autocontract: bool):
        pass  # pragma: no cover

    def get_participle(self, tense: Tense, voice: Voice):
        pass  # pragma: no cover

    @staticmethod
    def calculate_augment(stem: str, uncommon_epsilon=False, preposition=None):

        # Preposition set up
        has_prep = False
        to_add = ""
        if preposition is not None:
            has_prep = True
            if not (is_equal(preposition, "προ") or is_equal(preposition, "περι")) and is_vowel(preposition[-1]):
                to_add = preposition[:-1]
            else:
                to_add = preposition

            stem = stem[len(preposition):]
        # No longer prepositioning

        if not is_vowel(stem[0]):
            if preposition is not None:
                return to_add + "ε" + stem
            else:
                return unicodedata.normalize("NFC", u"ε\u0313") + stem

        to_return = None

        for start in Verb.AUGMENTS:
            if remove_accents(stem).startswith(start):
                length = len(unicodedata.normalize("NFD", unicodedata.normalize("NFC", stem)[:len(start)]))

                to_return = Verb.calculate_breathing(unicodedata.normalize("NFD", stem), Verb.AUGMENTS[start], length,
                                                     has_prep)

        if remove_accents(stem).startswith("ε") and to_return is None:
            if uncommon_epsilon:
                to_return = Verb.calculate_breathing(stem, "ει", 1, has_prep)
            else:
                to_return = Verb.calculate_breathing(stem, "η", 1, has_prep)

        if preposition is not None:
            return to_add + to_return
        else:
            return to_return

    @staticmethod
    def calculate_breathing(stem: str, augment: str, length: int, has_preposition: bool):
        if has_preposition:
            return augment + stem[length:]
        # smooth breathing
        if u"\u0313" in unicodedata.normalize("NFD", stem):
            return unicodedata.normalize("NFC", augment + u"\u0313" + stem[length:])
        # rough breathing
        elif u"\u0314" in unicodedata.normalize("NFD", stem):
            return unicodedata.normalize("NFC", augment + u"\u0314" + stem[length:])
        else:
            raise VerbComputeError("Could not ascertain breathing!")
