import json
import re
from enum import Enum, auto

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
    def calculate_augment(stem):
        # actually do something TODO
        return stem
