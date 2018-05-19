import inspect
from types import FunctionType

# noinspection PyPackageRequirements
import pytest

from ancientgrammar.verbs import get_type
from ancientgrammar.verbs.verb import VerbComputeError, VerbParseError, VerbType
from ancientgrammar.verbs.verbdeponent import DeponentVerb
from tests.verbs import ERROR_TESTS
from tests.verbs.utils import convert_args, convert_kwargs

PARSE_ERROR_TESTS = []
COMPUTE_ERROR_TESTS = []

for full_verb in ERROR_TESTS:
    if full_verb.pop("should_fail_creation") == "True":
        if full_verb.pop("deponent") == "True":
            continue

        PARSE_ERROR_TESTS.append([value for value in full_verb.values()])
        continue
    else:
        if get_type(full_verb["present"], full_verb["future"], full_verb["aorist"]) is VerbType.DEPONENT:
            continue

        verb_object = DeponentVerb(full_verb["present"], full_verb["future"], full_verb["aorist"],
                                   full_verb["aorist_passive"], full_verb["preposition"],
                                   full_verb["uncommon_epsilon"] == "True")

        verb_functions = {val[0]: val[1] for val in inspect.getmembers(verb_object, predicate=inspect.ismethod)}
        verb_functions.update({val[0]: val[1] for val in inspect.getmembers(verb_object, predicate=inspect.isfunction)})

        for test in full_verb["tests"]:
            test_info_list = [verb_functions[test["function"]], test["args"],
                              test["kwargs"], test["message"]]

            COMPUTE_ERROR_TESTS.append(test_info_list)


@pytest.mark.parametrize('present, future, aorist, aorist_passive, preposition, uncommon_epsilon, message',
                         PARSE_ERROR_TESTS)
def test_verb_creation_error(present: str, future: str, aorist: str, aorist_passive: str,
                             preposition: str, uncommon_epsilon: bool, message: str):
    with pytest.raises(VerbParseError) as parse_error:
        DeponentVerb(present, future, aorist, aorist_passive, preposition, uncommon_epsilon)
    assert message == str(parse_error.value)


@pytest.mark.parametrize('func, args, kwargs, message', COMPUTE_ERROR_TESTS)
def test_verb_computation_error(func: FunctionType, args: list, kwargs: dict, message: str):
    args = convert_args(args)
    kwargs = convert_kwargs(kwargs)

    with pytest.raises(VerbComputeError) as compute_error:
        func(*args, **kwargs)
    assert message == str(compute_error.value)