from ancientgrammar.adjective import get_adjective
from ancientgrammar.qualifiers import Gender, Case, Degree

def test_basic_adjective():
    adj = get_adjective(["σοφος", "σοφη", "σοφον"], "212")
    x = adj.decline(Gender.FEMININE, 0, Case.ACCUSATIVE, Degree.POSITIVE)
    assert x == "σοφην"