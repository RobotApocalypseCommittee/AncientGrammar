import json
import re
from enum import Enum, auto
import unicodedata

from ..utils import is_vowel, is_equal, remove_accents

class VerbParseError(Exception):
    pass

class VerbComputeError(Exception):
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

class Verb():
    AUGMENTS = {
        "ᾳ":u"η\u0345",
        "αι":u"η\u0345",
        "ει":u"η\u0345",
        "αυ":"ηυ",
        "ευ":"ηυ",
        "α":"η",
        "ι":"ι",
        "ο":"ω",
        "οι":u"ω\u0345",
        "υ":"υ"
    }

    def get_finite_form(self, tense: Tense, mood: Mood, voice: Voice, person: int, is_plural: bool):
        pass
    
    def get_imperative(self, aspect: Tense, voice: Voice, is_plural: bool):
        pass
    
    def get_infinitive(self, tense: Tense, voice: Voice):
        pass
    
    def get_participle(self):
        # Will return participle object associated with this verb TODO
        pass

    @staticmethod
    def calculate_augment(stem, uncommon_epsilon=False):
        if stem is None:
            return

        if not is_vowel(stem[0]):
            return unicodedata.normalize("NFC", u"ε\u0313") + stem
        
        for start in Verb.AUGMENTS:
            if remove_accents(stem).startswith(start):
                
                length = len(unicodedata.normalize("NFD", unicodedata.normalize("NFC", stem)[:len(start)]))

                return Verb.calculate_breathing(stem, Verb.AUGMENTS[start], length)

        if remove_accents(stem).startswith("ε"):
            if uncommon_epsilon:
                return Verb.calculate_breathing(stem, "ει", 1)
            else:
                return Verb.calculate_breathing(stem, "η", 1)
    
    @staticmethod
    def calculate_breathing(stem, augment, length):
        # smooth breathing
        if u"\u0313" in unicodedata.normalize("NFD", stem):
            return unicodedata.normalize("NFC", augment + u"\u0313") + stem[length:]
        elif u"\u0314" in unicodedata.normalize("NFD", stem):
            return unicodedata.normalize("NFC", augment + u"\u0314") + stem[length:]
        else:
            raise VerbComputeError("Could not ascertain breathing!")