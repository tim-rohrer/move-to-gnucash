"""conftest.py"""
from datetime import datetime
from decimal import Decimal
from numpy import NaN
import pytest

import pandas as pd

from move2gnucash.data_maps import Account2Move, Transaction2Move, Split2Move


@pytest.fixture(scope="module")
def complex_data_frame():
    """Fixture with complete example of accounts."""
    yield pd.DataFrame(
        {
            "Accounts": [
                "Assets",
                "Cash",
                "- Cash",
                "- Checking One",
                "- Checking Two",
                "- Total Cash",
                "Savings",
                "- Spouse Savings",
                "- Family Savings",
                "- Total Savings",
                "Property",
                "- 2012 Silverado",
                "- 2012 Camper",
                "- Total Property",
                "Total Assets",
                "Liabilities",
                "Credit Card",
                "- Apple Card",
                "- Credit Card",
                "- Total Credit Card",
                "Loan",
                "- Student Loan",
                "- Total Loan",
                "Total Liabilities",
            ],
            "12/31/2016": [
                "NaN",
                "NaN",
                77.12,
                440.84,
                235.38,
                753.34,
                "NaN",
                987.12,
                3250,
                4237.12,
                "NaN",
                30975,
                0,
                39975,
                44965.46,
                "NaN",
                "NaN",
                0,
                -973.4,
                -973.4,
                "NaN",
                -10500,
                -10650,
                -11623,
            ],
        }
    )


@pytest.fixture(scope="module")
def empty_data_frame():
    """Provide empty account list, which should error"""
    yield pd.DataFrame({"Accounts": [], "12/31/2016": []})


@pytest.fixture(scope="session")
def simple_data_frame_in():
    """
    Fixture with only a couple of representative accounts.
    Should result in list of dataclass objects shown in
    simple_fixture_accounts_out below.
    """
    return pd.DataFrame(
        {
            "account": [
                "Assets",
                "Assets:Current Assets",
                "Assets:Current Assets:Checking",
            ],
            "description": ["My Assets", "My Current Assets", "My Checking Account"],
            "type": ["ASSET", "ASSET", "BANK"],
            "balance": [NaN, NaN, 1000.00],
            "date": ["12/31/2016", "12/31/2016", "12/31/2016"],
        }
    )


@pytest.fixture()
def simple_fixture_accounts_out():
    """A fixture to add accounts."""
    return [
        Account2Move("Assets", "ASSET", "root", "USD", True, "My Assets"),
        Account2Move("Current Assets", "ASSET", "Assets", "USD", True, "My Current Assets"),
        Account2Move(
            "Checking",
            "BANK",
            "Assets:Current Assets",
            "USD",
            False,
            "My Checking Account",
        ),
        Account2Move("Equity", "EQUITY", "root", "USD", True, "Migration from Quicken"),
        Account2Move(
            "Opening Balances", "EQUITY", "Equity", "USD", False, "Migration from Quicken"
        ),
    ]


@pytest.fixture()
def fixture_opening_balances_simple():
    """Fixture providing example transactions for opening balances"""
    return [
        Transaction2Move(
            datetime.strptime("12/31/2016", "%m/%d/%Y").date(),
            datetime.strptime("12/31/2016", "%m/%d/%Y"),
            "USD",
            "Opening Balance",
            "",
            "",
            [
                Split2Move("Assets:Current Assets:Checking", Decimal("1000"), ""),
                Split2Move("Equity:Opening Balances", Decimal("-1000"), ""),
            ],
        )
    ]
