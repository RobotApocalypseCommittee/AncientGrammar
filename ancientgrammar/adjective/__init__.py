from ancientgrammar.adjective.fleshed_adjective import FleshedAdjective
from ancientgrammar.data import NENDINGS
from ancientgrammar.utils import is_vowel

def get_adjective(parts, adjtype:str, **options):
    if len(parts) == 3:
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
            return FleshedAdjective(stem, ending, **options)