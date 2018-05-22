import inspect
from copy import deepcopy
from types import FunctionType

# noinspection PyPackageRequirements
import pytest

from ancientgrammar.verbs.verb import VerbComputeError, VerbParseError, VerbType
from ancientgrammar.verbs.verbirregular import IrregularVerb
from tests.verbs import ERROR_TESTS
from tests.verbs.utils import convert_args, convert_kwargs, convert_forms

PARSE_ERROR_TESTS = []
COMPUTE_ERROR_TESTS = []

for full_verb in deepcopy(ERROR_TESTS):
    if full_verb.pop("should_fail_creation") == "True":
        full_verb.pop("deponent")
        PARSE_ERROR_TESTS.append([value for value in full_verb.values()])
        continue
    else:
        verb_object = IrregularVerb(full_verb["present"], full_verb["future"], full_verb["aorist"],
                                    full_verb["aorist_passive"], full_verb["preposition"],
                                    full_verb["uncommon_epsilon"] == "True", convert_forms(full_verb["allowed_forms"]))

        verb_functions = {val[0]: val[1] for val in inspect.getmembers(verb_object, predicate=inspect.ismethod)}
        verb_functions.update({val[0]: val[1] for val in inspect.getmembers(verb_object, predicate=inspect.isfunction)})

        for test in full_verb["tests"]:
            test_info_list = [verb_functions[test["function"]], test["args"],
                              test["kwargs"], test["message"]]

            COMPUTE_ERROR_TESTS.append(test_info_list)


@pytest.mark.parametrize('present, future, aorist, aorist_passive, preposition, uncommon_epsilon, forms, message',
                         PARSE_ERROR_TESTS)
def test_verb_creation_error(present: str, future: str, aorist: str, aorist_passive: str,
                             preposition: str, uncommon_epsilon: bool, forms: dict, message: str):
    with pytest.raises(VerbParseError) as parse_error:
        IrregularVerb(present, future, aorist, aorist_passive, preposition, uncommon_epsilon, convert_forms(forms))
    assert message == str(parse_error.value)


@pytest.mark.parametrize('func, args, kwargs, message', COMPUTE_ERROR_TESTS)
def test_verb_computation_error(func: FunctionType, args: list, kwargs: dict, message: str):
    args = convert_args(args)
    kwargs = convert_kwargs(kwargs)

    with pytest.raises(VerbComputeError) as compute_error:
        func(*args, **kwargs)
    assert message == str(compute_error.value)
