from enum import Enum, IntEnum, auto

class Gender(Enum):
    MASCULINE = auto()
    FEMININE = auto()
    NEUTER = auto()

class Case(IntEnum):
    NOMINATIVE = 0
    VOCATIVE = 1
    ACCUSATIVE = 2
    GENITIVE = 3
    DATIVE = 4

class Degree(IntEnum):
    POSITIVE = 0
    COMPARATIVE = 1
    SUPERLATIVE = 2

class ContractType(Enum):
    ALPHA = auto()
    EPSILON = auto()