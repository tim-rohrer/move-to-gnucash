"""test_file_operations.py"""
from unittest.mock import patch, Mock

from piecash import Account, create_book

from move2gnucash.file_operations import (
    fetch_csv_data,
    create_gnucash_book,
    create_accounts,
    add_transactions,
)


@patch("pandas.read_csv")
def test_fetch_csv_data_works(mock_read: Mock):
    """
    GIVEN fetch_csv_data with an existing properly formatted csv file
    WHEN executed
    THEN a Pandas DataFrame is returned with the data
    """
    fetch_csv_data("file")

    mock_read.assert_called_once_with("file")


@patch("move2gnucash.file_operations.create_book")
def test_create_gnucash_book(mock_create_book: Mock):
    """
    GIVEN the proper parameters, minimally a filename
    WHEN passed to create_gnucash_book and executed
    THEN piecash.create_book will be called with all of the parameters.
    """
    create_gnucash_book("testfile", "USD")

    mock_create_book.assert_called_once()


def test_add_accounts_success(simple_fixture_accounts_out):
    """
    GIVEN a list of five accounts and sub accounts, and a viable book instance
    WHEN executed with add_accounts
    THEN five new accounts will be added, if unique.
    """
    book = create_book(currency="USD")

    create_accounts(book, simple_fixture_accounts_out)

    assert len(book.accounts) == 5


def test_add_accounts_success_correct_tree(simple_fixture_accounts_out):
    """
    GIVEN an array of accounts and sub accounts, and a viable book instance
    WHEN executed with add_accounts,
    THEN the list of accounts will have the correct parent/child structure
    """
    book = create_book(currency="USD")

    create_accounts(book, simple_fixture_accounts_out)

    added_accounts = list(map(lambda acct: acct.fullname, book.accounts))
    assert "Assets:Current Assets" in added_accounts
    assert book.accounts(fullname="Assets:Current Assets").parent.name == "Assets"
    assert "Assets:Current Assets:Checking" in added_accounts


def test_add_transactions_success(fixture_opening_balances_simple):
    """
    GIVEN a book with a chart of accounts, and a list of transactions
    WHEN executed with create_transactions
    THEN the book will contain accounts and transactions with the correct balances.
    """
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
    ]
    book.save()
    add_transactions(book, fixture_opening_balances_simple)

    account_to_check = book.accounts(fullname="Assets:Current Assets:Checking")
    assert account_to_check.get_balance() == fixture_opening_balances_simple[0].splits[0].value
    assert (
        book.accounts(fullname="Equity:Opening Balances").get_balance(natural_sign=False)
        == fixture_opening_balances_simple[0].splits[1].value
    )
