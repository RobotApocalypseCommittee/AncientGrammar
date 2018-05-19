import json

from tests.data import path_to_test

TESTS = json.load(open(path_to_test("verb_tests.json"), "r", encoding="utf-8"))

ERROR_TESTS = json.load(open(path_to_test("verb_error_tests.json"), "r", encoding="utf-8"))
