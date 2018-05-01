from enum import IntEnum, auto

class Gender(IntEnum):
    MASCULINE = 0
    FEMININE = 1
    NEUTER = 2

class Case(Enum):
    NOMINATIVE = 0
    VOCATIVE = 1
    ACCUSATIVE = 2
    GENITIVE = 3
    DATIVE = 4
