"""conftest.py"""
import pytest


@pytest.fixture(scope="session")
def fixture_accounts():
    """A fixture to add accounts"""
    return [
        {
            "name": "Assets",
            "account_type": "ASSET",
            "parent": "root",
            "commodity": "USD",
            "placeholder": True,
        },
        {
            "name": "Current Assets",
            "account_type": "ASSET",
            "parent": "Assets",
            "commodity": "USD",
            "placeholder": True,
        },
        {
            "name": "Checking",
            "account_type": "BANK",
            "parent": "Assets:Current Assets",
            "commodity": "USD",
            "placeholder": False,
        },
        {
            "name": "Equity",
            "account_type": "EQUITY",
            "parent": "root",
            "commodity": "USD",
            "placeholder": True,
            # "children": [],
        },
        {
            "name": "Opening Balances",
            "account_type": "EQUITY",
            "parent": "Equity",
            "commodity": "USD",
            "placeholder": False,
        },
    ]
