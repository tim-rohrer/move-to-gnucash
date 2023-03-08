"""Fixtures supporting integration tests with GnuCash books"""
import pytest

from piecash import Account, create_book


@pytest.fixture
def detailed_book():
    """Creates basic book to support tests below."""
    book = create_book(currency="USD")
    usd = book.commodities(mnemonic="USD")
    book.root_account.children = [
        Account(
            parent=book.root_account,
            name="Assets",
            type="ASSET",
            commodity=usd,
            placeholder=True,
            children=[
                Account(
                    name="Current Assets",
                    type="ASSET",
                    commodity=usd,
                    placeholder=True,
                    children=[
                        Account(
                            name="Checking",
                            type="BANK",
                            commodity=usd,
                            placeholder=False,
                        ),
                        Account(
                            name="Cash",
                            type="CASH",
                            commodity=usd,
                            placeholder=False,
                        ),
                    ],
                )
            ],
        ),
        Account(
            parent=book.root_account,
            name="Equity",
            type="EQUITY",
            commodity=usd,
            placeholder=True,
            children=[
                Account(
                    name="Opening Balances",
                    type="EQUITY",
                    commodity=usd,
                    placeholder=False,
                )
            ],
        ),
        Account(
            parent=book.root_account,
            name="Expenses",
            type="EXPENSE",
            commodity=usd,
            placeholder=True,
            children=[
                Account(
                    name="Education",
                    type="EXPENSE",
                    commodity=usd,
                    placeholder=False,
                ),
                Account(
                    name="Other Expense",
                    type="EXPENSE",
                    commodity=usd,
                    placeholder=True,
                    children=[
                        Account(
                            name="Membership & Dues",
                            type="EXPENSE",
                            commodity=usd,
                            placeholder=False,
                        ),
                    ],
                ),
                Account(
                    name="Taxes",
                    type="EXPENSE",
                    commodity=usd,
                    placeholder=True,
                    children=[
                        Account(
                            name="Sales tax paid (personal)",
                            type="EXPENSE",
                            commodity=usd,
                            placeholder=False,
                        ),
                    ],
                ),
                Account(
                    name="Technology",
                    type="EXPENSE",
                    commodity=usd,
                    placeholder=True,
                    children=[
                        Account(
                            name="Hardware & Electronics",
                            type="EXPENSE",
                            commodity=usd,
                            placeholder=False,
                        ),
                    ],
                ),
                Account(
                    name="Housing",
                    type="EXPENSE",
                    commodity=usd,
                    placeholder=True,
                    children=[
                        Account(
                            name="Furniture & Furnishings",
                            type="EXPENSE",
                            commodity=usd,
                            placeholder=False,
                        ),
                    ],
                ),
                Account(
                    name="Food",
                    type="EXPENSE",
                    commodity=usd,
                    placeholder=True,
                    children=[
                        Account(
                            name="Groceries",
                            type="EXPENSE",
                            commodity=usd,
                            placeholder=False,
                        ),
                    ],
                ),
            ],
        ),
    ]
    book.save()
    yield book
