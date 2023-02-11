"""
Utility functions to help prepare mapped data.

Also being used to support mocking.
"""

from datetime import datetime


def combined_strings_by(string1: str, string2: str, separator: str) -> str:
    """Function to cleanly combine two strings. If both defined, they will
    be separated by the passed separator.
    """
    if not string1:
        return string2
    if not string2:
        return string1
    return string1 + separator + " " + string2


def get_now():
    """Wrapper to provide now(), mainly in support of code testing"""
    return datetime.now()
