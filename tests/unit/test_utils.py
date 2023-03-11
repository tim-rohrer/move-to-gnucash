"""test_utils.py"""
from datetime import datetime
from decimal import Decimal
import pandas as pd
import pytest

from move2gnucash.utils import (
    combined_strings_by,
    custom_join,
    decimal_to,
    hierarchy_from,
    string_trimmed_after,
    string_trimmed_before,
)


def test_decimal_to():
    """
    GIVEN a number (float) and a specified number of digits
        for the fraction
    WHEN executed with `decimal_to`
    THEN a Decimal object is returned showing the correct number
        of digits.
    """
    assert Decimal(10.03) != Decimal("10.03")
    assert decimal_to(10.03) == Decimal("10.03")
    assert decimal_to(10.03, 4) == Decimal("10.0300")
    assert decimal_to(-10.03, 2) == Decimal("-10.03")


def test_combined_strings_with_separator():
    """
    GIVEN up to two defined string, and a separator
    WHEN passed to combined_strings_by
    THEN a clean combined string is returned
    """
    assert (combined_strings_by("hello", "world", ";")) == "hello; world"
    assert (combined_strings_by("", "world", ";")) == "world"
    assert (combined_strings_by("hello", "", ";")) == "hello"


def test_custom_join():
    """
    GIVEN a Pandas Series produced by the DataFrame,
    WHEN executed with custom_join,
    THEN a literal string is returned preceded by, and joined with, colons
    """
    assert custom_join(pd.Series(["Foo", "Bar", ""])) == ":Foo:Bar"
    assert custom_join(pd.Series(["Foo", "Bar"])) == ":Foo:Bar"
    assert custom_join(pd.Series(["Foo", "", ""])) == ":Foo"
    assert custom_join(pd.Series([""])) == ""


def test_string_trimmed_after():
    """
    GIVEN a string of words separated by a specified delimiter and a specified number of occurrences,
    WHEN executed by string_trimmed_after,
    THEN a literal string is returned comprised of the left hand part of the original string
        before the nth occurrence of the delimiter.
    """
    test_string = "foo:bar:doo:day"
    assert string_trimmed_after(test_string, ":") == "foo:bar:doo"
    assert string_trimmed_after(test_string, ":", 1) == "foo"


def test_string_trimmed_before():
    """
    GIVEN a string of words separated by a specified delimiter and a specified number of occurrences,
    WHEN executed by string_trimmed_before,
    THEN a literal string is returned comprised of the right hand part of the original string
        after the nth occurrence of the delimiter.
    """
    test_string = "foo:bar:doo:day"
    assert string_trimmed_before(test_string, ":") == "day"
    assert string_trimmed_before(test_string, ":", 1) == "bar:doo:day"
    assert string_trimmed_before("foo", ":") == "foo"


def test_hierarchy_from():
    """
    GIVEN a string of words delimited by colons
    WHEN passed to hierarch_from
    THEN a single list of tuples will be return reflecting
    all of the hierarchies and the positions up from the lowest level.
    """

    assert hierarchy_from("Foo:Bar:Boo") == [("Foo", 2), ("Foo:Bar", 1), ("Foo:Bar:Boo", 0)]
