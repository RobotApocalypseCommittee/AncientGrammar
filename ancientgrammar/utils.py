import unicodedata
def is_vowel(char):
    return basic_char(char) in "αειορυω"

def is_equal(string1:str, string2:str):
    return remove_accents(string1) == remove_accents(string2)

def basic_char(string:str):
    return ''.join(c for c in unicodedata.normalize('NFD', string) 
            if unicodedata.category(c) != 'Mn')

def remove_accents(string:str):
    '''Keeps IOTA SUBSCRIPT'''
    return unicodedata.normalize("NFC", ''.join(c for c in unicodedata.normalize('NFD', string) 
            if unicodedata.category(c) != 'Mn' or c == "\u0345"))