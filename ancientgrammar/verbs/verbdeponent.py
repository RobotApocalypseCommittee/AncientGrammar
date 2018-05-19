from copy import deepcopy

from ancientgrammar.verbs.verb import VerbParseError, VerbComputeError, Tense, Mood, Voice, Verb
from ancientgrammar.verbs.verbregular import AoristType, RegularVerb
from ancientgrammar.qualifiers import ContractType
from ancientgrammar.utils import is_equal


class DeponentVerb(RegularVerb):
    # noinspection PyMissingConstructor
    def __init__(self, present=None, future=None, aorist=None, aorist_passive=None, preposition=None,
                 uncommon_epsilon_augment=False):
        """Initialises, taking forms and converting to stems"""

        self.allowed_forms = deepcopy(Verb.ALL_FORMS_ALLOWED)

        self.deponent_parts = {
            "PRESENT": False,
            "FUTURE": False,
            "AORIST_(MIDDLE)": False,
            "AORIST_(PASSIVE)": False
        }

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
            self.deponent_parts["PRESENT"] = True
            self.present = present[:-4]

            self.allowed_forms[Tense.PRESENT].remove(Voice.ACTIVE)
            self.allowed_forms[Tense.IMPERFECT].remove(Voice.ACTIVE)

            if is_equal(present[-5:], "αομαι"):
                self.contract = ContractType.ALPHA
            elif is_equal(present[-5:], "εομαι"):
                self.contract = ContractType.EPSILON
            else:
                self.contract = None
        else:
            raise VerbParseError("Present not regular!")

        if future is None:
            self.allowed_forms[Tense.FUTURE] = []
        elif is_equal(future[-1:], "ω"):
            self.future = future[:-1]
        elif is_equal(future[-4:], "ομαι"):
            self.deponent_parts["FUTURE"] = True
            self.future = future[:-4]

            self.allowed_forms[Tense.FUTURE].remove(Voice.ACTIVE)
        else:
            raise VerbParseError("Future not regular!")

        # Variable to store whether the aorist passive has been accounted for by the aorist (passive form aorists)
        aorist_passive_covered = False
        if aorist is None:
            self.allowed_forms[Tense.AORIST] = [Voice.PASSIVE]
        elif is_equal(aorist[-1:], "α"):
            self.aorist_type = AoristType.WEAK
            self.aorist = aorist[:-1]
        elif is_equal(aorist[-2:], "ον"):
            self.aorist_type = AoristType.STRONG
            self.aorist = aorist[:-2]
        elif is_equal(aorist[-4:], "αμην"):
            self.deponent_parts["AORIST_(MIDDLE)"] = True
            self.aorist_type = AoristType.WEAK
            self.aorist = aorist[:-4]

            self.allowed_forms[Tense.AORIST].remove(Voice.ACTIVE)
        elif is_equal(aorist[-4:], "ομην"):
            self.deponent_parts["AORIST_(MIDDLE)"] = True
            self.aorist_type = AoristType.STRONG
            self.aorist = aorist[:-4]

            self.allowed_forms[Tense.AORIST].remove(Voice.ACTIVE)
        elif is_equal(aorist[-2:], "ην"):
            self.deponent_parts["AORIST_(PASSIVE)"] = True
            self.aorist_type = AoristType.WEAK
            self.aorist_passive = aorist[:-2]

            self.allowed_forms[Tense.AORIST] = [Voice.PASSIVE]
            aorist_passive_covered = True
        else:
            raise VerbParseError("Aorist not recognised as a specified type!")

        # This means that there is not just aorist passive left - i.e. it is not a passive form aorist
        # In that case, the passive aorist would have been covered by the aorist section
        if not aorist_passive_covered:
            if aorist_passive is None:
                self.allowed_forms[Tense.AORIST].remove(Voice.PASSIVE)
            elif not is_equal(aorist_passive[-2:], "ην"):
                raise VerbParseError("Aorist passive not regular!")
            else:
                self.aorist_passive = aorist_passive[:-2]
