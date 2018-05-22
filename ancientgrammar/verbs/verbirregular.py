from copy import deepcopy

from ancientgrammar.adjective import get_adjective
from ancientgrammar.qualifiers import ContractType
from ancientgrammar.utils import is_equal
from ancientgrammar.verbs.verb import Tense, VerbParseError, AoristType, Verb, Voice, Mood
from ancientgrammar.verbs.verbdeponent import DeponentVerb


# Note how this _only_ subclasses DeponentVerb to show that it is a superset, not that there would
# be any logical difference were it to subclass RegularVerb
class IrregularVerb(DeponentVerb):
    # noinspection PyMissingConstructor
    def __init__(self, present=None, future=None, aorist=None, aorist_passive=None, preposition=None,
                 uncommon_epsilon_augment=False, allowed_forms=None, irregular_forms=None, irregular_participles=None):
        """
        Initialises, taking forms and converting to stems

        The form of irregular_forms is EXACTLY the same as VERB_TABLE.
        Also, in this dictionary, there can be a separate future for things like "εσομεν"

        Also, the forms should NOT be endings, but rather the entire form (with all contractions and augments already
        applied)

        The form of irregular_participles is:
        dict["TENSE_NAME"]["VOICE_NAME"] = [["ὠν", "οὐσα", "ὀν"], "313"]

        The principle parts _should_ be kept as "None" if they are completely irregular, but should be supplied if there
        are any regular parts (for example, if a verb has an irregular aorist active, but its aorist middle is
        completely normal, input "-ομην" for the aorist, and for irregular forms, put the irregular active as
        you would normally).

        Importantly, irregular forms are evaluated before checking whether that tense is "allowed", and therefore
        before any regular forms are evaluated!
        """

        if irregular_forms is None:
            irregular_forms = {}

        if irregular_participles is None:
            irregular_participles = {}

        self.irregular_forms = irregular_forms
        self.irregular_participles = irregular_participles

        super().__init__(present, future, aorist, aorist_passive, preposition, uncommon_epsilon_augment, allowed_forms)

    def get_finite_form(self, tense: Tense, mood: Mood, voice: Voice, person: int, is_plural: bool, autocontract=True):
        try:
            return self.irregular_forms[tense.name][mood.name][voice.name][str(person)][str(is_plural)]
        except KeyError:
            pass
        return super().get_finite_form(tense, mood, voice, person, is_plural, autocontract)

    def get_imperative(self, aspect: Tense, voice: Voice, is_plural: bool, autocontract=True):
        try:
            return self.irregular_forms[aspect.name]["IMPERATIVE"][voice.name]["2"][str(is_plural)]
        except KeyError:
            pass
        return super().get_imperative(aspect, voice, is_plural, autocontract)

    def get_infinitive(self, tense: Tense, voice: Voice, autocontract=True):
        try:
            return self.irregular_forms[tense.name]["INFINITIVE"][voice.name]
        except KeyError:
            pass
        return super().get_infinitive(tense, voice, autocontract)

    def get_participle(self, tense: Tense, voice: Voice):
        try:
            return get_adjective(*self.irregular_participles[tense.name][voice.name])
        except KeyError:
            pass
        return super().get_participle(tense, voice)
