"""test_utils.py"""
from move2gnucash.utils import combined_strings_by


def test_combined_strings_with_separator():
    """
    GIVEN up to two defined string, and a separator
    WHEN passed to combined_strings_by
    THEN a clean combined string is returned
    """
    assert (combined_strings_by("hello", "world", ";")) == "hello; world"
    assert (combined_strings_by("", "world", ";")) == "world"
    assert (combined_strings_by("hello", "", ";")) == "hello"
