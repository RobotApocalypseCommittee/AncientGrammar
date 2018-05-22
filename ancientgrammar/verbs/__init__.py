from ancientgrammar.utils import is_equal
from ancientgrammar.verbs.verb import VerbType
from ancientgrammar.verbs.verbdeponent import DeponentVerb
from ancientgrammar.verbs.verbirregular import IrregularVerb
from ancientgrammar.verbs.verbregular import RegularVerb


def get_verb(present=None, future=None, aorist=None, aorist_passive=None, preposition=None,
             uncommon_epsilon_augment=False, allowed_forms=None, irregular_forms=None, irregular_participles=None):
    verb_type = get_type(present, future, aorist, irregular_participles, irregular_forms)
    if verb_type is VerbType.DEPONENT:
        return DeponentVerb(present, future, aorist, aorist_passive, preposition, uncommon_epsilon_augment,
                            allowed_forms)
    elif verb_type is VerbType.IRREGULAR:
        print(allowed_forms)
        return IrregularVerb(present, future, aorist, aorist_passive, preposition, uncommon_epsilon_augment,
                             allowed_forms, irregular_forms, irregular_participles)
    else:  # Regular (so far)
        return RegularVerb(present, future, aorist, aorist_passive, preposition, uncommon_epsilon_augment,
                           allowed_forms)


def get_type(present=None, future=None, aorist=None, irregular_participles=None, irregular_forms=None):
    if (irregular_participles is not None or irregular_forms is not None) or (
            irregular_participles == {} or irregular_forms == {}):
        return VerbType.IRREGULAR
    elif (present is not None and is_equal(present[-4:], "ομαι")) or (
            future is not None and is_equal(future[-4:], "ομαι")) or (
            aorist is not None and (is_equal(aorist[-4:], "ομην") or
                                    is_equal(aorist[-4:], "αμην") or is_equal(aorist[-2:], "ην"))):
        return VerbType.DEPONENT
    else:  # Regular (so far)
        return VerbType.REGULAR
