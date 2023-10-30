"""
Contains the functions that operate on csv and GnuCash files.
"""
from datetime import datetime
import typing
import logging

import pandas as pd
from piecash import Account, Book, create_book, Transaction, Split

from move2gnucash.data_maps import Split2Move
from move2gnucash.utils import string_trimmed_after, string_trimmed_before

logging.basicConfig(level=logging.DEBUG)


def fetch_csv_data(file_to_open, _header=0):
    """Read all csv contents of file and return DataFrame"""
    return pd.read_csv(file_to_open, header=_header, thousands=",")


def fetch_accounts(file_name) -> typing.Dict:
    """Function to read and set up raw net worth data for preparation,
    mapping and saving to GnuCash.
    """
    date_string = string_trimmed_after(file_name, "_", 3)
    return {
        "as_of_date": datetime.strptime(date_string, "%Y_%m_%d").date(),
        "data": pd.read_csv(
            file_name, header=None, names=["root", "account", "balance"], thousands=","
        ),
    }


def fetch_categories(file_name: str) -> pd.DataFrame:
    """Function to read and set up raw accounts (from categories) data for preparation,
    mapping and saving to GnuCash.
    """
    # GnuCash refers to category-like information as just another account.
    return pd.read_csv(file_name, header=None, names=["root", "account", "balance"])


def create_gnucash_book(filename: str, currency_str: str = "USD", overwrite=False):
    """Wrapper to create_book with select defaults."""
    return create_book(filename, currency=currency_str, overwrite=overwrite)


def create_accounts(book: Book, accounts_list: pd.DataFrame) -> None:
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


def add_transactions(book: Book, transactions_list: pd.DataFrame) -> None:
    """Add balance transactions and save book.

    Chart of accounts must be in place.
    """

    def get_acct_reference_name(name: str):
        try:
            ref = book.accounts(name=name)
        except KeyError:
            print(f"\nNeed to create a new account: {name}!")
        return ref

    def get_acct_reference_fullname(fullname: str):
        try:
            return book.accounts(fullname=fullname)
        except KeyError:
            name = string_trimmed_before(fullname, ":")  # Remove any hierarchy.
            return get_acct_reference_name(name)

    def build_split(split_params: Split2Move):
        """Builds Split entries for transaction being added to book."""
        split_params.account = get_acct_reference_fullname(split_params.account)

        return Split(**split_params.__dict__)

    for trans in transactions_list:
        trans.splits = [build_split(split) for split in trans.splits]
        trans.currency = book.commodities(mnemonic=trans.currency)

        Transaction(**trans.__dict__)

        book.flush()

    book.save()
