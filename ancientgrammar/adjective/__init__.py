from ancientgrammar.adjective.fleshed_adjective import FleshedAdjective
from ancientgrammar.adjective.adjective import Adjective
from ancientgrammar.adjective.adjective33 import Adjective33
from ancientgrammar.data import NENDINGS
from ancientgrammar.utils import is_vowel

class AdjectivalError(Exception):
    pass

def get_adjective(parts:list, adjtype:str, **options):
    if adjtype == "212":
        # 212 Adjective
        stem = parts[0][:-2]
        ending = NENDINGS["STANDARD_212"]
        if is_vowel(stem[-1]):
            if "halfeta" in options and options["halfeta"]:
                ending = NENDINGS["HALPHA_212"]
            else:
                ending = NENDINGS["ALPHA_212"]
        if "last_syll_long" in options and options["last_syll_long"]:
            options["comparative"] = stem + "οτερος"
            options["superlative"] = stem + "οτατος"
        if options.get("has_feminine", True):
            return FleshedAdjective(Adjective(stem, ending, **options))
        else:
            return FleshedAdjective(Adjective33(stem, ending, **options))
    elif adjtype == "33":
        # 3-3 Adjective
        stem = parts[0][:-2]
        if parts[0].endswith("ης"):
            endings = NENDINGS["ADJECTIVE_33ETA"]
            if "comparative" not in options:
                options["comparative"] = stem + "εστερος"
                options["superlative"] = stem + "εστατος"
                return FleshedAdjective(Adjective33(stem, endings, **options))
        elif parts[0].endswith("ων"):
            endings = NENDINGS["COMPARATIVE_33WN"]
            return Adjective33(stem, endings, **options)
        elif parts[0].endswith("ος"):
            return get_adjective(parts, "212", has_feminine=False)
        else:
            raise AdjectivalError("3-3 Adjective in unknown form.")
            