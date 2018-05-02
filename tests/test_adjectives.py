from ancientgrammar.adjective import get_adjective
from ancientgrammar.qualifiers import Gender, Case, Degree

def get_basic_adjective():
    return get_adjective(["σοφος", "σοφη", "σοφον"], "212")

def test_basic_adjective():
    adj = get_basic_adjective()
    x = adj.decline(Gender.FEMININE, 0, Case.ACCUSATIVE, Degree.POSITIVE)
    assert x == "σοφην"

def test_basic_adjective_comparative():
    adj = get_basic_adjective()
    x = adj.decline(Gender.MASCULINE, 1, Case.DATIVE, Degree.COMPARATIVE)
    assert x == "σοφωτεροις"

def test_basic_adjective_superlative():
    adj = get_basic_adjective()
    x = adj.decline(Gender.NEUTER, 1, Case.VOCATIVE, Degree.SUPERLATIVE)
    assert x == "σοφωτατα"

