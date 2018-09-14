from copy import deepcopy

from ancientgrammar.verbs.verb import VerbParseError, Tense, Voice, Verb, AoristType
from ancientgrammar.verbs.verbregular import RegularVerb
from ancientgrammar.qualifiers import ContractType
from ancientgrammar.utils import is_equal


class DeponentVerb(RegularVerb):
    # noinspection PyMissingConstructor
    def __init__(self, present=None, future=None, aorist=None, aorist_passive=None, preposition=None,
                 uncommon_epsilon_augment=False, allowed_forms=None):
        """Initialises, taking forms and converting to stems"""

        if allowed_forms is None:
            self.allowed_forms = deepcopy(Verb.ALL_FORMS_ALLOWED)
        else:
            self.allowed_forms = allowed_forms

        self.aorist_type = None

        self.preposition = preposition
        self.uncommon_epsilon_augment = uncommon_epsilon_augment

        if present is None:
            self.allowed_forms[Tense.PRESENT] = []
            self.allowed_forms[Tense.IMPERFECT] = []
        elif is_equal(present[-1:], "ω"):
            self.present = present[:-1]

            if is_equal(present[-2:], "αω"):
                self.contract = ContractType.ALPHA
            elif is_equal(present[-2:], "εω"):
                self.contract = ContractType.EPSILON
            else:
                self.contract = None
        elif is_equal(present[-4:], "ομαι"):
            self.present = present[:-4]

            if Voice.ACTIVE in self.allowed_forms[Tense.PRESENT]:
                self.allowed_forms[Tense.PRESENT].remove(Voice.ACTIVE)
            if Voice.ACTIVE in self.allowed_forms[Tense.IMPERFECT]:
                self.allowed_forms[Tense.IMPERFECT].remove(Voice.ACTIVE)

            if is_equal(present[-5:], "αομαι"):
                self.contract = ContractType.ALPHA
            elif is_equal(present[-5:], "εομαι"):
                self.contract = ContractType.EPSILON
            else:
                self.contract = None
        else:
            raise VerbParseError("Present not recognised!")

        if future is None:
            self.allowed_forms[Tense.FUTURE] = []
        elif is_equal(future[-1:], "ω"):
            self.future = future[:-1]
        elif is_equal(future[-4:], "ομαι"):
            self.future = future[:-4]

            if Voice.ACTIVE in self.allowed_forms[Tense.FUTURE]:
                self.allowed_forms[Tense.FUTURE].remove(Voice.ACTIVE)
        else:
            raise VerbParseError("Future not recognised!")

        # Variable to store whether the aorist passive has been accounted for by the aorist (passive form aorists)
        aorist_passive_covered = False
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
        elif is_equal(aorist[-4:], "αμην"):
            self.aorist_type = AoristType.WEAK
            self.aorist = aorist[:-4]

            if Voice.ACTIVE in self.allowed_forms[Tense.AORIST]:
                self.allowed_forms[Tense.AORIST].remove(Voice.ACTIVE)
        elif is_equal(aorist[-4:], "ομην"):
            self.aorist_type = AoristType.STRONG
            self.aorist = aorist[:-4]

            if Voice.ACTIVE in self.allowed_forms[Tense.AORIST]:
                self.allowed_forms[Tense.AORIST].remove(Voice.ACTIVE)
        elif is_equal(aorist[-2:], "ην"):
            self.aorist_type = AoristType.WEAK
            self.aorist_passive = aorist[:-2]

            if Voice.ACTIVE in self.allowed_forms[Tense.AORIST]:
                self.allowed_forms[Tense.AORIST].remove(Voice.ACTIVE)
            if Voice.MIDDLE in self.allowed_forms[Tense.AORIST]:
                self.allowed_forms[Tense.AORIST].remove(Voice.MIDDLE)
            aorist_passive_covered = True
        else:
            raise VerbParseError("Aorist not recognised as a specified type!")

        # This means that there is not just aorist passive left - i.e. it is not a passive form aorist
        # In that case, the passive aorist would have been covered by the aorist section
        if not aorist_passive_covered:
            if aorist_passive is None:
                if Voice.PASSIVE in self.allowed_forms[Tense.AORIST]:
                    self.allowed_forms[Tense.AORIST].remove(Voice.PASSIVE)
            elif not is_equal(aorist_passive[-2:], "ην"):
                raise VerbParseError("Aorist passive not recognised!")
            else:
                self.aorist_passive = aorist_passive[:-2]
