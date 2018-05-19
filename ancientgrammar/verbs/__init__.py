from ancientgrammar.utils import is_equal
from ancientgrammar.verbs.verb import VerbType
from ancientgrammar.verbs.verbdeponent import DeponentVerb
from ancientgrammar.verbs.verbregular import RegularVerb


def get_verb(present=None, future=None, aorist=None, aorist_passive=None, preposition=None,
             uncommon_epsilon_augment=False):
    if get_type(present, future, aorist) is VerbType.DEPONENT:
        return DeponentVerb(present, future, aorist, aorist_passive, preposition, uncommon_epsilon_augment)
    else:  # Regular (so far)
        return RegularVerb(present, future, aorist, aorist_passive, preposition, uncommon_epsilon_augment)


def get_type(present=None, future=None, aorist=None):
    if (present is not None and is_equal(present[-4:], "ομαι")) or (
            future is not None and is_equal(future[-4:], "ομαι")) or (
            aorist is not None and (is_equal(aorist[-4:], "ομην") or
                                    is_equal(aorist[-4:], "αμην") or is_equal(aorist[-2:], "ην"))):
        return VerbType.DEPONENT
    else:  # Regular (so far)
        return VerbType.REGULAR
