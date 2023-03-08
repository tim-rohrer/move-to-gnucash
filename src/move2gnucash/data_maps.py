"""
Contains the classes and functions to map prepared data
(from the csv) in Pandas DataFrame to object classes for 
writing to a GnuCash file.
"""
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from piecash.core.account import Account
from piecash.core.commodity import Commodity

from move2gnucash.utils import decimal_to, get_now


@dataclass
class Account2Move:
    """Class to keep track of accounts and categories being moved to GnuCash."""

    name: str  # Short name of account
    type: str  # GnuCash type. See GnuCash app/docs for details
    parent: str | Account  # Generated from CSV column capturing full path to account or category
    commodity: str | Commodity
    placeholder: bool  # Move2GnuCash treats all parent accounts as placeholders
    description: str


@dataclass
class Split2Move:
    """Class to keep track of splits to be moved."""

    account: str  # This should be full path and name
    value: str
    memo: str


@dataclass
class Transaction2Move:
    """Class to keep track of transactions to be moved."""

    post_date: datetime
    enter_date: datetime
    currency: str
    description: str
    notes: str
    num: str  # Use for FITID
    splits: list[Split2Move]


def _split2move_list(split):
    return [
        Split2Move(
            split["tran_acct_from"],  # Set to path_and_name for look up
            decimal_to(-split["tran_amount"]),
            split.tran_memo,
        ),
        Split2Move(
            split["tran_acct_to"],
            decimal_to(split["tran_amount"]),
            split.tran_memo,
        ),
    ]


def _transaction2move(
    posted: datetime, description: str, notes: str, num: str, splits
) -> Transaction2Move:
    return Transaction2Move(
        post_date=posted,
        enter_date=get_now(),
        currency="USD",  # TODO: At some point, this needs to work with other currencies
        description=description,
        notes=notes,
        num=num,
        splits=splits,
    )


def _build_multi_splits_tran(split_group):
    splits = split_group.apply(_split2move_list, axis=1)
    splits_list = [elem for item in splits for elem in item]
    return _transaction2move(
        posted=datetime.strptime(split_group["tran_date"].iat[0], "%m/%d/%Y").date(),
        description=split_group.tran_description.iat[0],
        notes=split_group.tran_memo.iat[0],
        num=split_group.tran_num.iat[0],
        splits=splits_list,
    )


def _build_single_splits_tran(split_data: pd.Series) -> Transaction2Move:
    splits_list = _split2move_list(split_data)
    return _transaction2move(
        posted=datetime.strptime(split_data["tran_date"], "%m/%d/%Y").date(),
        description=split_data["tran_description"],
        notes=split_data["tran_memo"],
        num=split_data["tran_num"],
        splits=splits_list,
    )


def _processed_transactions(transactions: pd.DataFrame):
    """Function to map preprocessed transaction data to
    a list of transactions staged for final processing and
    saving to a GnuCash file.
    """

    splits_mask = transactions["tran_split"] == "S"
    multi_splits_data = transactions[splits_mask]
    single_splits_data = transactions[~splits_mask]

    multi_split_transactions = (
        (
            multi_splits_data.groupby(["tran_date", "tran_description"], sort=False).apply(
                _build_multi_splits_tran
            )
        ).to_list()
        if len(multi_splits_data) > 0
        else []
    )
    single_split_transactions = (
        single_splits_data.apply(_build_single_splits_tran, axis=1).to_list()
        if len(single_splits_data) > 0
        else []
    )
    return multi_split_transactions + single_split_transactions


def mapped_transactions(prepared_transactions: pd.DataFrame) -> list:
    """
    Provides a list of Transaction2Move objects from prepared transactions.
    """

    return _processed_transactions(prepared_transactions)


def _account2move(acct: pd.Series) -> Account2Move:
    return Account2Move(
        name=acct["name"],
        type=acct["selected_type"],
        parent=acct["parent"],
        commodity=acct["commodity"],
        placeholder=acct["placeholder"],
        description=acct["description"],
    )


def _prepared_balances_transactions(data: pd.DataFrame, opening_balances_acct: str) -> pd.DataFrame:
    default_memo = "Migrated by Move2GnuCash"
    data["tran_split"] = ""
    data[
        "tran_acct_to"
    ] = opening_balances_acct  # Must be full_path_name of account to support look up.
    data["tran_description"] = "Opening Balance"
    data[["tran_memo", "tran_tags", "tran_fitid"]] = [default_memo, "", ""]
    data = data.rename(
        columns={
            "path_and_name": "tran_acct_from",
            "acct_balance": "tran_amount",
            "acct_balance_date": "tran_date",
        }
    )
    return data


def mapped_accounts(prepared_data: pd.DataFrame, new_book=False):
    """Provides a list of Account2Move objects from prepared accounts."""

    new_accounts_from_data = prepared_data.apply(_account2move, axis=1).to_list()

    equity_accts = []
    if new_book:
        opening_balances_acct = "Equity:Opening Balances"
        equity_accts = [
            Account2Move(
                name="Equity",
                type="EQUITY",
                parent="root",
                commodity="USD",
                placeholder=True,
                description="",
            ),
            Account2Move(
                name=opening_balances_acct.rsplit(":", 1)[-1],
                type="EQUITY",
                parent="Equity",
                commodity="USD",
                placeholder=False,
                description="",
            ),
        ]
    return new_accounts_from_data + equity_accts
