import json
import re
from enum import Enum, auto

from ancientgrammar.adjective import get_adjective
from ancientgrammar.data import path_to_file
from ancientgrammar.qualifiers import ContractType
from ancientgrammar.utils import calculate_contraction
from ancientgrammar.verbs.verb import (Mood, Tense, Verb, VerbComputeError,
                                       VerbParseError, Voice)


class AoristType(Enum):
    WEAK = auto()
    STRONG = auto()

class RegularVerb(Verb):
    '''
    The first four arguments are to be given the first person singular indicative
    (and if not otherwise stated, active) form of that tense for the verb you want
    in ALL cases.

    So here's the setup of the VERB_TABLE:

    VERB_TABLE[TENSE][MOOD][VOICE][PERSON][PLURAL]

    For present active singular optatives, the setup is slightly different:

    VERB_TABLE["PRESENT"]["OPTATIVE"]["ACTIVE"][PERSON]["False"][CONTRACT]

    The preposition argument is to give the preposition which preceeds the
    verb in a compound verb (such as απο or περι)

    Uncommon epsilon augment refers to the few (but not unique) verbs which,
    starting with ε, instead of the temporal augment lengthening it to η, it instead
    becomes ει (like εχω)
    '''
    VERB_TABLE = json.load(open(path_to_file("regular_endings.json"), encoding="utf-8"))

    def __init__(self, present=None, future=None, aorist=None, aorist_passive=None, preposition=None, uncommon_epsilon_augment=False):
        '''Initialises, taking forms and converting to stems'''

        self.preposition = preposition
        self.uncommon_epsilon_augment = uncommon_epsilon_augment

        if re.search(r"αω$", present) is not None:
            self.contract = ContractType.ALPHA
        elif re.search(r"εω$", present) is not None:
            self.contract = ContractType.EPSILON
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
            self.aorist_type = AoristType.WEAK
            self.aorist = aorist[:-1]
        elif re.search(r"ον$", aorist) is not None:
            self.aorist_type = AoristType.STRONG
            self.aorist = aorist[:-2]
        else:
            raise VerbParseError("Aorist not recognised as a specified type!")
        
        if aorist_passive is None:
            self.aorist_passive = False
        elif re.search(r"ην$", aorist_passive) is None:
            raise VerbParseError("Aorist passive not regular!")
        else:
            self.aorist_passive = aorist_passive[:-2]
    
    def get_finite_form(self, tense: Tense, mood: Mood, voice: Voice, person: int, is_plural: bool, autocontract=True):
        if not mood.is_finite():
            raise VerbComputeError("The passed mood is not finite!")
        
        stem = None

        if tense is Tense.PRESENT:
            stem = self.present

        elif tense is Tense.FUTURE:
            # handles as a present (same endings) but adds ησ if it's aor pass stem
            tense = Tense.PRESENT
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive + "ησ"
            else:
                stem = self.future

        elif tense is Tense.IMPERFECT:
            stem = self.present
            if mood is Mood.INDICATIVE:
                stem = self.calculate_augment(stem, self.uncommon_epsilon_augment, self.preposition)

        else: # aorist
            if voice is Voice.PASSIVE:
                # all passive aorists are the same
                aorist_type = AoristType.WEAK
                stem = self.aorist_passive
            else:
                aorist_type = self.aorist_type
                stem = self.aorist

            if mood is Mood.INDICATIVE:
                stem = self.calculate_augment(stem, self.uncommon_epsilon_augment, self.preposition)
        
        if stem is None:
            raise VerbComputeError("That form of the verb either does not exist, or was not supplied!")
        
        if tense is Tense.AORIST:
            ending = self.VERB_TABLE["AORIST"][mood.name][voice.name][aorist_type.name][str(person)][str(is_plural)]
        elif tense is Tense.PRESENT and mood is Mood.OPTATIVE and voice is Voice.ACTIVE and not is_plural:
            # handle dodge optative
            ending = self.VERB_TABLE["PRESENT"]["OPTATIVE"]["ACTIVE"][str(person)]["False"][str(self.contract is not None)]
        else:
            ending = self.VERB_TABLE[tense.name][mood.name][voice.name][str(person)][str(is_plural)]

        if autocontract and tense is not Tense.FUTURE and not (tense is Tense.AORIST and self.aorist_type is AoristType.WEAK):
            return calculate_contraction(stem, ending, self.contract)
        else:
            return stem + ending
    
    def get_imperative(self, aspect: Tense, voice: Voice, is_plural: bool, autocontract=True):
        if not aspect.is_aspect():
            raise VerbComputeError("The passed tense does not have an imperative!")

        stem = None

        if aspect is Tense.PRESENT:
            stem = self.present
            ending = self.VERB_TABLE[aspect.name]["IMPERATIVE"][voice.name]["2"][str(is_plural)]
        else: # aorist
            if voice is voice.PASSIVE:
                aorist_type = AoristType.WEAK
                stem = self.aorist_passive
            else:
                aorist_type = self.aorist_type
                stem = self.aorist

            ending = self.VERB_TABLE[aspect.name]["IMPERATIVE"][voice.name][aorist_type.name]["2"][str(is_plural)]
        
        if stem is None:
            raise VerbComputeError("That form of the verb either does not exist, or was not supplied!")

        if autocontract:
            return calculate_contraction(stem, ending, self.contract)
        else:
            return stem + ending
    
    def get_infinitive(self, tense: Tense, voice: Voice, auotocontract=True):
        spurious_ei = False

        if tense is Tense.PRESENT:
            stem = self.present
            if voice is Voice.ACTIVE:
                spurious_ei = True

        elif tense is Tense.FUTURE:
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive
            else:
                stem = self.future

        elif tense is Tense.IMPERFECT:
            stem = self.present

        else: # aorist
            if voice is Voice.PASSIVE:
                aorist_type = AoristType.WEAK
                stem = self.aorist_passive
            else:
                aorist_type = self.aorist_type
                stem = self.aorist
        
        if tense is Tense.AORIST:
            ending = self.VERB_TABLE[tense.name]["INFINITIVE"][voice.name][aorist_type.name]
        else:
            ending = self.VERB_TABLE[tense.name]["INFINITIVE"][voice.name]

        if auotocontract:
            return calculate_contraction(stem, ending, self.contract, spurious_ei=spurious_ei)
        else:
            return stem + ending
    
    def get_participle(self, tense:Tense, voice:Voice):
        if tense is Tense.IMPERFECT:
            raise VerbComputeError("There is no imperfect participle!")

        if tense is Tense.PRESENT:
            stem = self.present
            if Voice is Voice.ACTIVE:
                return get_adjective([stem+"ων", stem+"ουσα", stem+"ον"], "313")
            else:
                stem += "ομεν"
                return get_adjective([stem+"ος", stem+"η", stem+"ον"], "212")

        elif tense is Tense.FUTURE:
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive + "ησομεν"
                return get_adjective([stem+"ος", stem+"η", stem+"ον"], "212")
            
            stem = self.future

            if voice is Voice.ACTIVE:
                return get_adjective([stem+"ων", stem+"ουσα", stem+"ον"], "313")
            else:
                stem += "ομεν"
                return get_adjective([stem+"ος", stem+"η", stem+"ον"], "212")
        
        elif tense is Tense.AORIST: # TODO
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive
                return get_adjective([stem+"εις", stem+"εισα", stem+"εν"], "313")
            
            stem = self.aorist

            if voice is Voice.ACTIVE:
                if self.aorist_type is AoristType.WEAK:
                    return get_adjective([stem+"ας", stem+"ασα", stem+"αν"], "313")
                else:
                    return get_adjective([stem+"ων", stem+"ουσα", stem+"ον"], "313")
            else:
                if self.aorist_type is AoristType.WEAK:
                    stem += "αμεν"
                else:
                    stem += "ομεν"
                return get_adjective([stem+"ος", stem+"η", stem+"ον"], "212")
