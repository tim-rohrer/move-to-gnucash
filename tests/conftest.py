"""conftest.py"""
from datetime import datetime
import pytest

from move2gnucash.data_maps import Account2Move, Transaction2Move, Split2Move


@pytest.fixture()
def fixture_accounts():
    """A fixture to add accounts"""
    return [
        Account2Move("Assets", "ASSET", "root", "USD", True, "My Assets"),
        Account2Move("Current Assets", "ASSET", "Assets", "USD", True, "My Current Assets"),
        Account2Move("Checking", "BANK", "Assets:Current Assets", "USD", False, "My Checking Acct"),
        Account2Move("Equity", "EQUITY", "root", "USD", True, "My Equity"),
        Account2Move("Opening Balances", "EQUITY", "Equity", "USD", False, "My Opening Balances"),
    ]


@pytest.fixture()
def fixture_opening_balances_simple():
    """Fixture providing example transactions for opening balances"""
    return [
        Transaction2Move(
            datetime.strptime("12/31/2016", "%m/%d/%Y").date(),
            datetime.strptime("12/31/2016", "%m/%d/%Y"),
            "USD",
            "Test Transaction",
            "Migrated from Quicken",
            "FITID NUMBER",
            [
                Split2Move("Checking", "2350.47", "Split Memo!"),
                Split2Move("Equity:Opening Balances", "-2350.47", "Another Split Memo!"),
            ],
        )
    ]
