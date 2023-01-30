"""
Contains the functions that operate on csv and GnuCash files.
"""
import pandas as pd

from piecash import Account, Book, create_book
from piecash.core.factories import create_currency_from_ISO


def fetch_csv_data(file_to_open):
    """Read all csv contents of file and return DataFrame"""
    return pd.read_csv(file_to_open)


def create_gnucash_book(filename: str, currency_str: str = "USD", overwrite=False):
    """Wrapper to create_book with select defaults."""
    create_book(filename, currency=create_currency_from_ISO(currency_str), overwrite=overwrite)


def create_accounts(book: Book, accounts_to_add):
    """Add accounts and save book.
    Sets chart of accounts hierarchy.
    """
    for account in accounts_to_add:
        name, account_type, parent, commodity, placeholder = account.values()
        parent_acct = book.accounts(fullname=parent) if parent != "root" else book.root_account
        Account(
            parent=parent_acct,
            name=name,
            type=account_type,
            commodity=book.commodities(mnemonic=commodity),
            placeholder=placeholder,
        )
        book.flush()

    book.save()
