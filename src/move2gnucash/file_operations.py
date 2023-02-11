"""
Contains the functions that operate on csv and GnuCash files.
"""
import logging

import pandas as pd
from piecash import Account, Book, create_book, Transaction, Split

from move2gnucash.transaction_maps import Split2Move

logging.basicConfig(level=logging.DEBUG)


def fetch_csv_data(file_to_open):
    """Read all csv contents of file and return DataFrame"""
    return pd.read_csv(file_to_open)


def create_gnucash_book(filename: str, currency_str: str = "USD", overwrite=False):
    """Wrapper to create_book with select defaults."""
    return create_book(filename, currency=currency_str, overwrite=overwrite)


def create_accounts(book: Book, accounts_list):
    """Add accounts and save book.
    Sets chart of accounts hierarchy.
    """
    for acct in accounts_list:
        acct.parent = (
            book.accounts(fullname=acct.parent) if acct.parent != "root" else book.root_account
        )
        acct.commodity = book.commodities(mnemonic=acct.commodity)
        Account(**acct.__dict__)
        book.flush()
    book.save()


def add_transactions(book: Book, transactions_list):
    """Add transactions and save book.

    Chart of accounts must be in place.
    """

    def build_split(split_params: Split2Move):
        """Builds Split entries for transaction being added to book."""
        split_params.account = book.accounts(fullname=split_params.account)
        return Split(**split_params.__dict__)

    for trans in transactions_list:
        trans.splits = [build_split(split) for split in trans.splits]
        trans.currency = book.commodities(mnemonic=trans.currency)
        Transaction(**trans.__dict__)
        book.flush()
    book.save()
