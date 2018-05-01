import unicodedata
def is_vowel(char):
    return remove_accents(char) in "αειορυω"

def remove_accents(string:str):
    return ''.join(c for c in unicodedata.normalize('NFD', s) 
            if unicodedata.category(c) != 'Mn')