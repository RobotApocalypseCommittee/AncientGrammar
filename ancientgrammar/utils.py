import unicodedata
from ancientgrammar.qualifiers import ContractType

from ancientgrammar.data import CONTRACTS


def is_vowel(char):
    return basic_char(char) in "αειορυωη"


def is_equal(string1: str, string2: str):
    return remove_accents(string1) == remove_accents(string2)


def basic_char(string: str):
    return ''.join(c for c in unicodedata.normalize('NFD', string)
                   if unicodedata.category(c) != 'Mn')


def remove_accents(string: str):
    """Keeps IOTA SUBSCRIPT"""
    return unicodedata.normalize("NFC", ''.join(c for c in unicodedata.normalize('NFD', string)
                                                if unicodedata.category(c) != 'Mn' or c == "\u0345"))


def alpha_purify(ending: str):
    new_str = []
    for char in ending:
        if is_equal(char, "η"):
            new_str.append("α")
        elif is_equal(char, "ῃ"):
            new_str.append("ᾳ")
        else:
            new_str.append(char)

    return ''.join(new_str)


def calculate_contraction(stem: str, ending: str, cont_type: ContractType, **kwargs):
    """
        Kwargs can be:
        "spurious_ei" (as true) to signify that the ει in the ending is 'spurious'
        "d_or_p_noun" (as true) to signify that this is a noun, and is either dual or plural
    """

    if cont_type is ContractType.ALPHA:
        for start_of_ending in CONTRACTS["ALPHA"]:
            if is_equal(start_of_ending, ending[:len(start_of_ending)]):
                return stem[:-1] + CONTRACTS["ALPHA"][start_of_ending] + ending[len(start_of_ending):]

        if is_equal("ει", ending[:2]):
            if "spurious_ei" in kwargs.keys() and kwargs["spurious_ei"]:
                return stem + ending[2:]
            else:
                return stem[:-1] + "ᾳ" + ending[2:]
    elif cont_type is ContractType.EPSILON:
        for start_of_ending in CONTRACTS["EPSILON"]:
            if is_equal(start_of_ending, ending[:len(start_of_ending)]):
                return stem[:-1] + CONTRACTS["EPSILON"][start_of_ending] + ending[len(start_of_ending):]

        if is_equal("α", ending[0]):
            if "d_or_p_noun" in kwargs.keys() and kwargs["d_or_p_noun"]:
                return stem + "α" + ending[1:]
            else:
                return stem + "η" + ending[1:]
        elif is_equal("αι", ending[:2]):
            if "d_or_p_noun" in kwargs.keys() and kwargs["d_or_p_noun"]:
                return stem + "α" + ending[1:]
            else:
                return stem + "ῃ" + ending[1:]

    return stem + ending
