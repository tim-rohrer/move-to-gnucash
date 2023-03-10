"""
test_file_operations.py

Includes tests to read and write data. Read includes input files of Quicken exported
accounts (net worth), categories and transactions. Write includes objects
for the GnuCash data file being created. 
"""
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch, Mock

from piecash import Account, create_book

from move2gnucash.file_operations import (
    fetch_categories,
    create_gnucash_book,
    create_accounts,
    add_transactions,
    fetch_accounts,
)


def setup_basic_book():
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
    return book


#############################
# Tests supporting get data
#############################
@patch("pandas.read_csv")
def test_fetch_accounts(mock_read: Mock):
    """
    GIVEN the file name of an existing properly formatted accounts csv file,
    WHEN executed with fetch_accounts,
    THEN Pandas.read_csv is called with header=None, column headers will be added;
        and an object will be returned with the as_of_date from the file name and a data
        key reflecting the accounts and their balances data.
    """
    res = fetch_accounts("2016_12_31_file.csv")

    mock_read.assert_called_once_with(
        "2016_12_31_file.csv", header=None, names=["root", "account", "balance"], thousands=","
    )
    assert isinstance(res, dict)
    assert res["as_of_date"] == datetime.strptime("2016_12_31", "%Y_%m_%d").date()


@patch("pandas.read_csv")
def test_fetch_categories(mock_read: Mock):
    """
    GIVEN the file name of an existing properly formatted categories csv file,
    WHEN executed with fetch_categories
    THEN Pandas.read_csv is called with header=None and column headers set;
        and an object will be returned with the raw category data.
    """
    fetch_categories("categories.csv")

    mock_read.assert_called_once_with(
        "categories.csv", header=None, names=["root", "account", "balance"]
    )


#############################
# Tests supporting the
# writing of data to GnuCash
#############################


# Book creation
@patch("move2gnucash.file_operations.create_book")
def test_create_gnucash_book(mock_create_book: Mock):
    """
    GIVEN the proper parameters, minimally a filename,
    WHEN passed to create_gnucash_book and executed
    THEN piecash.create_book will be called with all of the parameters.
    """
    create_gnucash_book("testfile", "USD")

    mock_create_book.assert_called_once()


# Accounts
def test_add_accounts(new_accounts_list):
    """
    GIVEN a list of three accounts and sub accounts, and a viable book instance
    WHEN executed with add_accounts
    THEN three new accounts will be added, if unique.
    """
    book = create_book(currency="USD")

    create_accounts(book, new_accounts_list)

    assert len(book.accounts) == 3


def test_add_accounts_correct_tree(new_accounts_list):
    """
    GIVEN an array of accounts and sub accounts, and a viable book instance
    WHEN executed with add_accounts,
    THEN the list of accounts will have the correct parent/child structure
    """
    book = create_book(currency="USD")

    create_accounts(book, new_accounts_list)

    added_accounts = list(map(lambda acct: acct.fullname, book.accounts))
    assert "Assets:Current Assets" in added_accounts
    assert book.accounts(fullname="Assets:Current Assets").parent.name == "Assets"
    assert "Assets:Current Assets:Checking" in added_accounts


# Transactions and Splits
def test_add_transactions(transaction_simple):
    """
    GIVEN a book with a chart of accounts, and a list of mapped transaction objects
    WHEN executed with create_transactions
    THEN the book will double entries with the correct balances.
    """
    book = setup_basic_book()

    add_transactions(book, transaction_simple)

    assert (
        book.accounts(fullname="Assets:Current Assets:Checking").get_balance()
        == transaction_simple[0].splits[0].value
    )
    assert (
        book.accounts(fullname="Equity:Opening Balances").get_balance(natural_sign=False)
        == transaction_simple[0].splits[1].value
    )


def test_add_transaction_shorter_name_only(transaction_using_short_acct_name):
    """
    GIVEN the user imports transaction data with shorter names for accounts
    WHEN add_transaction tries to create the account reference
    THEN the account will be found and referenced by short name.
    """
    book = setup_basic_book()

    add_transactions(book, transaction_using_short_acct_name)

    assert book.accounts(name="Checking").get_balance() == Decimal(1000)
