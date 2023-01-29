"""test_file_operations.py"""
from unittest.mock import patch, Mock

from piecash import create_book

from move2gnucash.file_operations import fetch_csv_data, create_gnucash_book, create_accounts


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
    create_gnucash_book("testfile")

    mock_create_book.assert_called_once_with("testfile")


def test_add_accounts_success(fixture_accounts):
    """
    GIVEN a list of five accounts and sub accounts, and a viable book instance
    WHEN executed with add_accounts
    THEN five new accounts will be added, if unique.
    """
    book = create_book(currency="USD")

    create_accounts(book, fixture_accounts)

    assert len(book.accounts) == 5


def test_add_accounts_success_correct_tree(fixture_accounts):
    """
    GIVEN an array of accounts and sub accounts, and a viable book instance
    WHEN executed with add_accounts,
    THEN the list of accounts will have the correct parent/child structure
    """
    book = create_book(currency="USD")

    create_accounts(book, fixture_accounts)

    added_accounts = list(map(lambda acct: acct.fullname, book.accounts))
    assert "Assets:Current Assets" in added_accounts
    assert book.accounts(fullname="Assets:Current Assets").parent.name == "Assets"
    assert "Assets:Current Assets:Checking" in added_accounts


# def test_add_transactions_success():
#     """
#     GIVEN a book with a complete chart of accounts, and a list of transactions
#     WHEN executed with create_transactions
#     THEN the book will contain accounts and transactions.
#     """
#     today = datetime.now()
#     book = create_book(currency="USD")
#     book.root_account.children = accounts_fixture(book)
#     book.save()
#     to_account = book.accounts(fullname="Assets:Current Assets:Checking")
#     from_account = book.accounts(fullname="Equity:Opening Balances")
#     amount = Decimal("2350.47")
#     transactions = [
#         Transaction(
#             post_date=today.date(),
#             enter_date=today,
#             currency=book.commodities(mnemonic="USD"),
#             description="Test Transaction",
#             splits=[
#                 Split(account=to_account, value=amount, memo="Split Memo!"),
#                 Split(account=from_account, value=-amount, memo="Other Split Memo!"),
#             ],
#         )
#     ]

#     add_transactions(book, transactions)

#     account_to_check = book.accounts(fullname="Assets:Current Assets:Checking")
#     assert account_to_check.get_balance() == amount
#     assert from_account.get_balance() == amount * -1
