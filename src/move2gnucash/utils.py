"""
Utility functions used in Move2GnuCash.

Also being used to support mocking.
"""
from decimal import Decimal
from datetime import datetime
from typing import Literal, LiteralString

from numpy import NaN
from pandas import Series


def decimal_to(val: float, places: int = 2) -> Decimal:
    """Function to fix the number of places in a Decimal
    after the period.
    """
    return Decimal(val).quantize(Decimal(10) ** -places)


def combined_strings_by(string1: str, string2: str, separator: str) -> str:
    """Function to cleanly combine two strings. If both defined, they will
    be separated by the passed separator.
    """
    if not string1:
        return string2
    if not string2:
        return string1
    return string1 + separator + " " + string2


def custom_join(strings: Series) -> LiteralString | Literal[""]:
    """Function to join string data contained in non-empty elements of a Pandas Series,
    returning a string with each "word" delimited by a colon."""
    strings[strings == ""] = NaN
    strings.dropna(inplace=True)
    res: LiteralString | Literal[""] = ":" + ":".join(strings.tolist()) if len(strings) > 0 else ""
    return res


def string_trimmed_after(string: str, delimiter: str, occurrences=0) -> str:
    """Function to trim a string after the nth occurrence of the specified delimiter.

    If occurrences == 0, only the last word/segment is trimmed.
    """
    groups: list[str] = string.split(delimiter)
    n_th: int = occurrences if occurrences >> 0 else len(groups) - 1
    return delimiter.join((string.split(delimiter))[:n_th])


def string_trimmed_before(string: str, delimiter, occurrences=0) -> str:
    """Function to trim a string before the nth occurrence of the specified delimiter.

    If occurrences = 0, only the last word/segment is returned."""
    groups: list[str] = string.split(delimiter)
    n_th: int = occurrences if occurrences >> 0 else len(groups) - 1
    return delimiter.join((groups)[n_th:])


def hierarchy_from(delimited_words: str) -> list[str]:
    """
    Function to make list of all parents from a string delimited by a colon.

    For example, "strong:java:bean" becomes "["strong", "strong:java", "strong:java:bean"].

    CURRENTLY UNUSED, but being retained as it wasn't yet committed.
    This was originally written to help create accounts automatically based on categories,
    a desired future feature.
    """
    root = delimited_words.split(":", 1)[0]  # The root tells us when to stop recursing
    tracker: list[tuple[str, Literal[0]]] = [(delimited_words, 0)]

    def recurse(word: str, level=1) -> str:
        if word != root:
            word = string_trimmed_after(word, ":")
            tracker.append((word, level))
            return recurse(word, level + 1)
        return tracker

    res = recurse(delimited_words)
    res.reverse()
    return res


def get_now():
    """Wrapper to provide now(), mainly in support of code testing"""
    return datetime.now()
