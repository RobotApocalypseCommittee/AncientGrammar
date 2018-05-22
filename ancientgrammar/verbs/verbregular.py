import json

from ancientgrammar.adjective import get_adjective
from ancientgrammar.data import path_to_file
from ancientgrammar.qualifiers import ContractType
from ancientgrammar.utils import calculate_contraction, is_vowel, is_equal
from ancientgrammar.verbs.verb import (Mood, Tense, Verb, VerbComputeError,
                                       VerbParseError, Voice, AoristType)


class RegularVerb(Verb):
    """
    The first four arguments are to be given the first person singular indicative
    (and if not otherwise stated, active) form of that tense for the verb you want
    in ALL cases.

    So here's the setup of the VERB_TABLE:

    VERB_TABLE[TENSE][MOOD][VOICE][PERSON][PLURAL]

    For present active singular optatives, the setup is slightly different:

    VERB_TABLE["PRESENT"]["OPTATIVE"]["ACTIVE"][PERSON]["False"][CONTRACT]

    The preposition argument is to give the preposition which precedes the
    verb in a compound verb (such as απο or περι)

    Uncommon epsilon augment refers to the few (but not unique) verbs which,
    starting with ε, instead of the temporal augment lengthening it to η, it instead
    becomes ει (like εχω)

    Allowed forms is a dict of lists (dict[TENSE][0]) where the key is the tense,
    and the value is a list of voices which are allowed. This _can_ be overridden by
    the code which checks which forms are logically possible, but only by _removal_ of
    voices/tenses, no tense/voice will ever be possible to use that you have not specified.
    An empty value (None) signifies that ALL tenses and voices (except for the ones that the
    code determines to be impossible) can be used.
    """
    VERB_TABLE = json.load(open(path_to_file("regular_endings.json"), encoding="utf-8"))

    def __init__(self, present=None, future=None, aorist=None, aorist_passive=None, preposition=None,
                 uncommon_epsilon_augment=False, allowed_forms=None):
        """Initialises, taking forms and converting to stems"""

        if allowed_forms is None:
            super().__init__()
        else:
            self.allowed_forms = allowed_forms

        self.preposition = preposition
        self.uncommon_epsilon_augment = uncommon_epsilon_augment

        if present is None:
            self.allowed_forms[Tense.PRESENT] = []
            self.allowed_forms[Tense.IMPERFECT] = []
        elif not is_equal(present[-1:], "ω"):
            raise VerbParseError("Present not recognised!")
        else:
            self.present = present[:-1]

            if is_equal(present[-2:], "αω"):
                self.contract = ContractType.ALPHA
            elif is_equal(present[-2:], "εω"):
                self.contract = ContractType.EPSILON
            else:
                self.contract = None

        if future is None:
            self.allowed_forms[Tense.FUTURE] = []
        elif not is_equal(future[-1:], "ω"):
            raise VerbParseError("Future not recognised!")
        else:
            self.future = future[:-1]

        if aorist is None:
            if Voice.ACTIVE in self.allowed_forms[Tense.AORIST]:
                self.allowed_forms[Tense.AORIST].remove(Voice.ACTIVE)
            if Voice.MIDDLE in self.allowed_forms[Tense.AORIST]:
                self.allowed_forms[Tense.AORIST].remove(Voice.MIDDLE)
        elif is_equal(aorist[-1:], "α"):
            self.aorist_type = AoristType.WEAK
            self.aorist = aorist[:-1]
        elif is_equal(aorist[-2:], "ον"):
            self.aorist_type = AoristType.STRONG
            self.aorist = aorist[:-2]
        else:
            raise VerbParseError("Aorist not recognised as a specified type!")

        if aorist_passive is None:
            if Voice.PASSIVE in self.allowed_forms[Tense.AORIST]:
                self.allowed_forms[Tense.AORIST].remove(Voice.PASSIVE)
        elif not is_equal(aorist_passive[-2:], "ην"):
            raise VerbParseError("Aorist passive not recognised!")
        else:
            self.aorist_passive = aorist_passive[:-2]

    def get_stem(self, tense: Tense, mood: Mood, voice: Voice):
        if tense is Tense.PRESENT:
            return self.present

        elif tense is Tense.FUTURE:
            if voice is Voice.PASSIVE:
                return self.aorist_passive + "ησ"
            else:
                return self.future

        elif tense is Tense.IMPERFECT:
            stem = self.present
            if mood is Mood.INDICATIVE:
                stem = self.calculate_augment(stem, self.uncommon_epsilon_augment, self.preposition)

            return stem

        else:  # aorist
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive
            else:
                stem = self.aorist

            if mood is Mood.INDICATIVE and stem:
                stem = self.calculate_augment(stem, self.uncommon_epsilon_augment, self.preposition)

            return stem

    def get_finite_form(self, tense: Tense, mood: Mood, voice: Voice, person: int, is_plural: bool, autocontract=True):
        if not mood.is_finite():
            raise VerbComputeError("The passed mood is not finite!")

        if not self.can_get_form(tense, voice):
            raise VerbComputeError("That form of the verb either does not exist, or was not supplied!")

        stem = self.get_stem(tense, mood, voice)

        # handles as a present(same endings) but adds ησ if it's aor pass stem
        tense = Tense.PRESENT if tense is Tense.FUTURE else tense

        aorist_type = AoristType.WEAK if voice is Voice.PASSIVE else self.aorist_type

        if tense is Tense.AORIST:
            ending = self.VERB_TABLE["AORIST"][mood.name][voice.name][aorist_type.name][str(person)][str(is_plural)]
        elif tense is Tense.PRESENT and mood is Mood.OPTATIVE and voice is Voice.ACTIVE and not is_plural:
            # handle dodge optative
            ending = self.VERB_TABLE["PRESENT"]["OPTATIVE"]["ACTIVE"][str(person)]["False"][
                str(self.contract is not None)]
        else:
            ending = self.VERB_TABLE[tense.name][mood.name][voice.name][str(person)][str(is_plural)]

        if autocontract and is_vowel(stem[-1]):
            return calculate_contraction(stem, ending, self.contract)
        else:
            return stem + ending

    def get_imperative(self, aspect: Tense, voice: Voice, is_plural: bool, autocontract=True):
        if not aspect.is_aspect():
            raise VerbComputeError("The passed tense does not have an imperative!")

        if not self.can_get_form(aspect, voice):
            raise VerbComputeError("That form of the verb either does not exist, or was not supplied!")

        aorist_type = AoristType.WEAK if voice is Voice.PASSIVE else self.aorist_type

        stem = self.get_stem(aspect, Mood.IMPERATIVE, voice)

        if aspect is Tense.PRESENT:
            ending = self.VERB_TABLE[aspect.name]["IMPERATIVE"][voice.name]["2"][str(is_plural)]
        else:  # aorist
            ending = self.VERB_TABLE[aspect.name]["IMPERATIVE"][voice.name][aorist_type.name]["2"][str(is_plural)]

        if autocontract:
            return calculate_contraction(stem, ending, self.contract)
        else:
            return stem + ending

    def get_infinitive(self, tense: Tense, voice: Voice, autocontract=True):
        if tense is Tense.IMPERFECT:
            raise VerbComputeError("There is no such thing as an imperfect infinitive!")

        if not self.can_get_form(tense, voice):
            raise VerbComputeError("That form of the verb either does not exist, or was not supplied!")

        spurious_ei = tense is Tense.PRESENT and voice is Voice.ACTIVE

        aorist_type = AoristType.WEAK if voice is Voice.PASSIVE else self.aorist_type

        stem = self.get_stem(tense, Mood.INFINITIVE, voice)

        # This is done after so only the endings get affected
        tense = Tense.PRESENT if tense is Tense.FUTURE else tense

        if tense is Tense.AORIST:
            ending = self.VERB_TABLE[tense.name]["INFINITIVE"][voice.name][aorist_type.name]
        else:
            ending = self.VERB_TABLE[tense.name]["INFINITIVE"][voice.name]

        if autocontract:
            return calculate_contraction(stem, ending, self.contract, spurious_ei=spurious_ei)
        else:
            return stem + ending

    def get_participle(self, tense: Tense, voice: Voice):
        if tense is Tense.IMPERFECT:
            raise VerbComputeError("There is no imperfect participle!")

        if not self.can_get_form(tense, voice):
            raise VerbComputeError("That form of the verb either does not exist, or was not supplied!")

        if tense is Tense.PRESENT:
            stem = self.present
            if voice is Voice.ACTIVE:
                return get_adjective([stem + "ων", stem + "ουσα", stem + "ον"], "313")
            else:
                stem += "ομεν"
                return get_adjective([stem + "ος", stem + "η", stem + "ον"], "212")

        elif tense is Tense.FUTURE:
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive + "ησομεν"
                return get_adjective([stem + "ος", stem + "η", stem + "ον"], "212")

            stem = self.future

            if voice is Voice.ACTIVE:
                return get_adjective([stem + "ων", stem + "ουσα", stem + "ον"], "313")
            else:
                stem += "ομεν"
                return get_adjective([stem + "ος", stem + "η", stem + "ον"], "212")

        elif tense is Tense.AORIST:
            if voice is Voice.PASSIVE:
                stem = self.aorist_passive
                return get_adjective([stem + "εις", stem + "εισα", stem + "εν"], "313")

            stem = self.aorist

            if voice is Voice.ACTIVE:
                if self.aorist_type is AoristType.WEAK:
                    return get_adjective([stem + "ας", stem + "ασα", stem + "αν"], "313")
                else:
                    return get_adjective([stem + "ων", stem + "ουσα", stem + "ον"], "313")
            else:
                if self.aorist_type is AoristType.WEAK:
                    stem += "αμεν"
                else:
                    stem += "ομεν"
                return get_adjective([stem + "ος", stem + "η", stem + "ον"], "212")
