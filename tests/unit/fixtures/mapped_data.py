"""
Fixtures of data objects ready to write to the GnuCash file.

Includes:
    - transactions with splits objects
    - account objects
    """

from datetime import datetime
from decimal import Decimal

import pytest

from move2gnucash.data_maps import Account2Move, Transaction2Move, Split2Move


@pytest.fixture()
def transaction_using_short_acct_name():
    """
    Fixture providing example of a short name transaction

    Used by test_add_transaction_shorter_name_only in
        test_file_operations.py
    """
    return [
        Transaction2Move(
            datetime.strptime("12/31/2016", "%m/%d/%Y").date(),
            datetime(2023, 2, 1, 0, 0, 0),
            "USD",
            "Transfer",
            "Test transfer",
            "",
            [
                Split2Move(
                    "Checking",
                    Decimal("1000"),
                    "Migrated by Move2GnuCash",
                ),
                Split2Move(
                    "Equity:Opening Balances",
                    Decimal("-1000"),
                    "Migrated by Move2GnuCash",
                ),
            ],
        )
    ]


@pytest.fixture()
def transaction_simple():
    # TODO Evaluate difference to previous fixture compared to requirement. Specifically, am I using short or full path names????
    """
    Fixture providing example transactions for opening balances

    Used by test_simple_account_map_balances_transactions in
        test_data_maps.py
    Used by test_add_transactions in test_file_operations.py
    """
    return [
        Transaction2Move(
            datetime.strptime("12/31/2016", "%m/%d/%Y").date(),
            datetime(2023, 2, 1, 0, 0, 0),
            "USD",
            "Opening Balance",
            "Migrated by Move2GnuCash",
            "",
            [
                Split2Move(
                    "Assets:Current Assets:Checking",
                    Decimal("1000"),
                    "Migrated by Move2GnuCash",
                ),
                Split2Move(
                    "Equity:Opening Balances",
                    Decimal("-1000"),
                    "Migrated by Move2GnuCash",
                ),
            ],
        )
    ]


@pytest.fixture()
def new_accounts_list():
    """
    A fixture reflecting Account2Move objects ready to write
    in GnuCash.
    """
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
    ]


@pytest.fixture()
def new_accounts_list_new_book():
    """
    A fixture reflecting Account2Move objects ready to write
    in GnuCash.
    """
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
        Account2Move("Equity", "EQUITY", "root", "USD", True, ""),
        Account2Move("Opening Balances", "EQUITY", "Equity", "USD", False, ""),
    ]
