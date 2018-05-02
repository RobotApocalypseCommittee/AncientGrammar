import unicodedata

def is_vowel(char):
    return remove_accents(char) in "αειορυω"

def remove_accents(string:str):
    return ''.join(char for char in unicodedata.normalize('NFD', string) 
            if unicodedata.category(char) != 'Mn')