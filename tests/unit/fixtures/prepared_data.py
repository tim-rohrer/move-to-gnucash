"""prepared_data fixture"""
from numpy import NaN
import pandas as pd
import pytest


@pytest.fixture(scope="session")
def prepared_account_data():
    """
    Fixture with only a couple of representative accounts.
    Should result in list of dataclass objects shown in
    new_accounts_list below.

    Used by test_simple_account_maps_accounts in test_data_maps.py
    """
    return pd.DataFrame(
        {
            "path_and_name": [
                "Assets",
                "Assets:Current Assets",
                "Assets:Current Assets:Checking",
            ],
            "name": ["Assets", "Current Assets", "Checking"],
            "parent": ["root", "Assets", "Assets:Current Assets"],
            "placeholder": [True, True, False],
            "description": ["My Assets", "My Current Assets", "My Checking Account"],
            "commodity": ["USD", "USD", "USD"],
            "selected_type": ["ASSET", "ASSET", "BANK"],
            "balance": [NaN, NaN, 1000.00],
            "acct_balance_date": ["12/31/2016", "12/31/2016", "12/31/2016"],
        }
    )


@pytest.fixture(scope="module")
def prepared_transactions():
    """Fixture reflecting prepared transactions used in mapping."""
    return pd.DataFrame(
        {
            "tran_split": ["", "", "", "S", "S", "S", "S", "S", ""],
            "tran_date": [
                "12/30/2016",
                "1/3/2017",
                "1/3/2017",
                "1/3/2017",
                "1/3/2017",
                "1/3/2017",
                "1/3/2017",
                "1/3/2017",
                "1/3/2017",
            ],
            "tran_currency": [
                "USD",
                "USD",
                "USD",
                "USD",
                "USD",
                "USD",
                "USD",
                "USD",
                "USD",
            ],
            "tran_description": [
                "John",
                "Sam Properties",
                "Paypal",
                "Target",
                "Target",
                "Target",
                "Smiths",
                "Smiths",
                "Wal-mart",
            ],
            "tran_amount": [-200.00, -550.00, -24.95, -8.14, -2.99, -96.94, -0.19, -30.97, -11.22],
            "tran_acct_to": [
                "Expenses:Education",
                "Expenses:Education",
                "Expenses:Other Expense:Membership & Dues",
                "Expenses:Taxes:Sales tax paid (personal)",
                "Expenses:Technology:Hardware & Electronics",
                "Expenses:Housing:Furniture & Furnishings",
                "Expenses:Taxes:Sales tax paid (personal)",
                "Expenses:Food:Groceries",
                "Expenses:Transfer:[Cash]",
            ],
            "tran_acct_from": [
                "Checking",
                "Checking",
                "Checking",
                "Checking",
                "Checking",
                "Checking",
                "Checking",
                "Checking",
                "Checking",
            ],
            "tran_memo": [
                "Transfer to Checking; college, john, food allowance, room & board, university",
                "college, john, rent, room & board, university",
                "",
                "",
                "computers & electronics",
                "",
                "",
                "groceries",
                "",
            ],
            "tran_num": [
                "201612300900000000002",
                "201701030625000000000",
                "201701030625000000001",
                "201701030107000000002",
                "201701030107000000002",
                "201701030107000000002",
                "201701030107000000003",
                "201701030107000000003",
                "201701030107000000004",
            ],
        }
    )
