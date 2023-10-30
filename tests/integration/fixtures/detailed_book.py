"""Fixtures supporting integration tests with GnuCash books"""
from datetime import datetime
import pytest

from piecash import Account, create_book, Transaction, Split


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
                    name="Cash",
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
                ),
                Account(
                    name="Investments",
                    type="ASSET",
                    commodity=usd,
                    placeholder=True,
                    children=[Account(name="IRA", type="STOCK", commodity=usd, placeholder=False)],
                ),
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
            name="Income",
            type="INCOME",
            commodity=usd,
            placeholder=True,
            children=[
                Account(name="Salary", type="INCOME", commodity=usd, placeholder=False),
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
                Account(
                    name="Uncategorized",
                    type="EXPENSE",
                    commodity=usd,
                    placeholder=False,
                ),
            ],
        ),
    ]
    book.flush()
    checking = book.accounts(fullname="Assets:Cash:Checking")
    opening_balances = book.accounts(fullname="Equity:Opening Balances")
    Transaction(
        currency=usd,
        description="Opening Balances",
        post_date=datetime(2016, 12, 31).date(),
        splits=[Split(account=checking, value=-100), Split(account=opening_balances, value=100)],
    )
    book.save()
    yield book
