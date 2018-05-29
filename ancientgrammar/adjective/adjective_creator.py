from ancientgrammar.data import NENDINGS
from ancientgrammar.utils import is_vowel, is_equal
from ancientgrammar.adjective.adjective import Adjective
from ancientgrammar.adjective.adjective33 import Adjective33
from ancientgrammar.adjective.adjectivalerrors import *

def determine_type(parts: list):
    """Determines type of adjective to best of abilities."""
    if len(parts) == 3:
        # 212 or 313
        if parts[0].endswith("ος") and parts[2].endswith("ον"):
            # 212
            return "212"
        else:
            return "313"
    elif len(parts) == 2:
        if parts[0].endswith("ος") and parts[1].endswith("ον"):
            # 22
            return "22"
        else:
            return "33"
    else:
        raise UnknownAdjectiveTypeError(', '.join(parts))

def get_raw_adjective(parts: list, adjtype: str = None, **options):
    """Get an adjective-like object, without all the trimmings."""
    if adjtype is None:
        adjtype = determine_type(parts)
    if adjtype == "212":
        # 212 Adjective
        stem = parts[0][:-2]
        ending = NENDINGS["STANDARD_212"]
        if is_vowel(stem[-1]):
            ending = NENDINGS["ALPHA_212"]
        if options.get("has_adverb", False):
            options["adverb"] = stem + "ως"
        return Adjective(stem, ending, **options)
    elif adjtype == "33":
        # 3-3 Adjective
        stem = parts[0][:-2]
        if is_equal(parts[0][-2:], "ης"):
            endings = NENDINGS["ADJECTIVE_33ETA"]
            if options.get("has_adverb", False):
                options["adverb"] = stem + "ως"
            return Adjective33(stem, endings, **options)
        elif is_equal(parts[0][-2:], "ων"):
            endings = NENDINGS["COMPARATIVE_33WN"]
            return Adjective33(stem, endings, **options)
        else:
            raise UnknownAdjectiveTypeError("3-3 Adjective in unknown form.")
    elif adjtype == "22":
        stem = parts[0][:-2]
        endings = NENDINGS["STANDARD_212"]
        if options.get("has_adverb", False):
            options["adverb"] = stem + "ως"
        return Adjective33(stem, endings, **options)
    elif adjtype == "313":
        # 3-1-3 adjective
        if is_equal(parts[0][-2:], "ων"):
            stem = parts[0][:-2]
            endings = NENDINGS["PARTICIPLE_313"]
            return Adjective(stem, endings)  # no comparative or superlative
        elif is_equal(parts[0][-2:], "ας"):
            stem = parts[0][:-2]
            endings = NENDINGS["WEAK_PARTICIPLE_313"]
            return Adjective(stem, endings)
        elif is_equal(parts[0][-3:], "εις"):
            stem = parts[0][:-3]
            endings = NENDINGS["PASS_PARTICIPLE_313"]
            return Adjective(stem, endings)
        elif is_equal(parts[0][-2:], "υς"):
            stem = parts[0][:-2]
            endings = NENDINGS["ADJECTIVE_U313"]
            if options.get("has_adverb", False):
                options["adverb"] = stem + "εως"
            return Adjective(stem, endings, **options)
    else:
        raise UnknownAdjectiveTypeError('"{}"'.format(adjtype))