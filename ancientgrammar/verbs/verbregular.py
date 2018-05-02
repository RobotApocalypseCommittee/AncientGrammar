import json
import re
from enum import Enum, auto

from .verb import Mood, Tense, Verb, VerbComputeError, VerbParseError, Voice


class AoristTypes(Enum):
    WEAK = auto()
    STRONG = auto()
    ROOT = auto()

class ContractTypes(Enum):
    ALPHA = auto()
    EPSILON = auto()

class RegularVerb(Verb):
    '''
    So here's the setup of the VERB_TABLE:

    VERB_TABLE[TENSE][MOOD][VOICE][PERSON][PLURAL]

    For present active singular optatives, the setup is slightly different:

    VERB_TABLE["PRESENT"]["OPTATIVE"]["ACTIVE"][PERSON]["False"][CONTRACT]
    '''
    VERB_TABLE = json.load(open("ancientgrammar/verbs/regular_endings.json", encoding="utf-8"))

    def __init__(self, present=None, future=None, aorist=None, aorist_passive=None):
        '''Initialises, taking forms and converting to stems'''

        if re.search(r"αω$", present) is not None:
            self.contract = ContractTypes.ALPHA
        elif re.search(r"εω$", present) is not None:
            self.contract = ContractTypes.EPSILON
        else:
            self.contract = None

        if present is None:
            self.present = False
        elif re.search(r"ω$", present) is None:
            raise VerbParseError("Present not regular!")
        else:
            self.present = present[:-1]

        if future is None:
            self.future = False
        elif re.search(r"ω$", future) is None:
            raise VerbParseError("Future not regular!")
        else:
            self.future = future[:-1]
        
        if aorist is None:
            self.aorist = False
        elif re.search(r"α$", aorist) is not None:
            self.aorist_type = AoristTypes.WEAK
            self.aorist = aorist[:-1]
        elif re.search(r"ον$", aorist) is not None:
            self.aorist_type = AoristTypes.STRONG
            self.aorist = aorist[:-2]
        elif re.search(r"ν$", aorist) is not None:
            self.aorist_type = AoristTypes.ROOT
            self.aorist = aorist[:-1]
        else:
            raise VerbParseError("Aorist not recognised as a specified type!")
        
        if aorist_passive is None:
            self.aorist_passive = False
        elif re.search(r"ην$", aorist_passive) is None:
            raise VerbParseError("Aorist passive not regular!")
        else:
            self.aorist_passive = aorist_passive[:-2]
    
    def get_finite_form(self, tense: Tense, mood: Mood, voice: Voice, person: int, is_plural: bool):
        if not mood.is_finite():
            raise VerbComputeError("The passed mood is not finite!")
        
        if tense is Tense.PRESENT:
            stem = self.present

        elif tense is Tense.FUTURE:
            # handles as a present (same endings) but adds ησ if it's aor pass
            tense = Tense.PRESENT
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive + "ησ"
            else:
                stem = self.future

        elif tense is Tense.IMPERFECT:
            stem = self.present
            if mood is Mood.INDICATIVE:
                stem = self.calculate_augment(stem)

        else: # aorist
            if voice is Voice.PASSIVE:
                aorist_type = AoristTypes.WEAK
                stem = self.aorist_passive
            else:
                aorist_type = self.aorist_type
                stem = self.aorist

            if mood is Mood.INDICATIVE:
                stem = self.calculate_augment(stem)
        
        if stem is None:
            raise VerbComputeError("That form of the verb either does not exist, or was not supplied!")
        
        if tense is tense.AORIST:
            ending = 
        elif tense is Tense.PRESENT and mood is Mood.OPTATIVE and voice is Voice.ACTIVE and not is_plural:
            # handle dodge optative
            ending = self.VERB_TABLE["PRESENT"]["OPTATIVE"]["ACTIVE"][str(person)]["False"][str(self.contract is not None)]
        else:
            ending = self.VERB_TABLE[tense.name][mood.name][voice.name][str(person)][str(is_plural)]

        return stem + ending
    
    def get_imperative(self, aspect: Tense, voice: Voice, is_plural: bool):
        if not aspect.is_aspect():
            raise VerbComputeError("The passed tense does not have an imperative!")

        if aspect is Tense.PRESENT:
            stem = self.present
        else: # aorist
            stem = self.aorist
        
        ending = self.VERB_TABLE[aspect.name]["IMPERATIVE"][voice.name][str(is_plural)]

        return stem + ending
    
    def get_infinitive(self, tense: Tense, voice: Voice):
        if tense is Tense.PRESENT:
            stem = self.present

        elif tense is Tense.FUTURE:
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive
            else:
                stem = self.future

        elif tense is Tense.IMPERFECT:
            stem = self.present

        else: # aorist
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive
            else:
                stem = self.aorist
        
        ending = self.VERB_TABLE[tense.name]["INFINITIVE"][voice.name]

        return stem + ending
