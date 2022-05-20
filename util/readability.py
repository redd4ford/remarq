from enum import Enum, auto


class Readability(Enum):
    """
    Sentence readability types.
    """
    # less than 14 words
    NORMAL = auto()
    # reading level between 10 and 14
    HARD = auto()
    # reading level more than 14
    VERY_HARD = auto()
