"""
Module used by app to handle the various user actions
taken to migrate data to GnuCash book.
"""
from typing import Dict, NewType

import pandas as pd
from piecash import Book

from move2gnucash.data_maps import mapped_accounts, mapped_transactions
from move2gnucash.data_preparation import (
    prepared_balances,
    prepared_category_accounts,
    prepared_transactions,
)
from move2gnucash.file_operations import (
    add_transactions,
    create_accounts,
    fetch_accounts,
    fetch_categories,
    fetch_csv_data,
)

NewBookData = NewType("NewBookData", Dict)


def _new_book_data(book_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    return {
        "accounts": mapped_accounts(book_data, new_book=True),
        "transactions": mapped_transactions(book_data.dropna()),
    }


def opening_balances(data_filename: str, book: Book) -> None:
    """Do something"""
    raw_data = fetch_accounts(data_filename)

    prepared_data = prepared_balances(raw_data["data"])

    res = _new_book_data(prepared_data)

    create_accounts(book, res["accounts"])

    add_transactions(book, res["transactions"])
    book.save()


def category_accounts(data_filename: str, book: Book) -> None:
    """Adds accounts reflecting (income and expense) accounts to the book."""
    raw_data: pd.DataFrame = fetch_categories(data_filename)

    prepared_data: pd.DataFrame = prepared_category_accounts(raw_data)

    mapped_data: list = mapped_accounts(prepared_data)

    create_accounts(book, mapped_data)
    book.save()


def transactions(data_filename: str, book: Book) -> None:
    """Add double entry transactions (usually income or expense) to the book."""
    raw_data: pd.DataFrame = fetch_csv_data(data_filename)

    prepared_data: pd.DataFrame = prepared_transactions("Expenses", raw_data)

    mapped_data: list = mapped_transactions(prepared_data)

    add_transactions(book, mapped_data)
    book.save()
