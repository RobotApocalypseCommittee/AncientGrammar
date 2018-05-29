from ancientgrammar.adjective.fleshed_adjective import FleshedAdjective
from ancientgrammar.adjective.adjective import Adjective
from ancientgrammar.adjective.adjective33 import Adjective33
from ancientgrammar.utils import is_equal
from ancientgrammar.adjective.adjective_creator import get_raw_adjective, determine_type
from ancientgrammar.adjective.adjectivalerrors import AdjectivalError, UnknownAdjectiveTypeError

def get_adjective(parts: list, adjtype: str = None, **options):
    """Get a fully-featured adjective, with a comparative and superlative."""
    if adjtype is None:
        adjtype = determine_type(parts)

    if "has_adverb" not in options:
        options["has_adverb"] = True
    if adjtype == "212":
        # 212 Adjective
        stem = parts[0][:-2]
        if "last_syll_long" in options and options["last_syll_long"]:
            options["comparative"] = stem + "οτερος"
            options["superlative"] = stem + "οτατος"
    elif adjtype == "33" and is_equal(parts[0][-2:], "ης"):
        # 3-3 Adjective
        stem = parts[0][:-2]
        if "comparative" not in options:
            options["comparative"] = stem + "εστερος"
            options["superlative"] = stem + "εστατος"
    elif adjtype == "22":
        stem = parts[0][:-2]
    elif adjtype == "313" and is_equal(parts[0][-2:], "υς"):
        # 3-1-3 adjective
        stem = parts[0][:-2]
        if "comparative" not in options:
            options["comparative"] = stem + "υτερος"
            options["superlative"] = stem + "υτατος"
    else:
        # If not an adjective which has comparative etc.
        return get_raw_adjective(parts, adjtype, **options)
    # Return it fleshed out with comparative etc.
    return FleshedAdjective(get_raw_adjective(parts, adjtype, **options))



get_participle = get_raw_adjective
