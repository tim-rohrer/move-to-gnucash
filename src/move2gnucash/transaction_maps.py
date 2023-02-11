"""
Contains the classes and functions to map transaction data
from the csv in Pandas DataFrame for processing, and
ultimately to the lists for writing to a GnuCash file.
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

import pandas as pd

from move2gnucash.utils import combined_strings_by, get_now


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


def __combined_memo_tags(memo: str, tags: str) -> str:
    return combined_strings_by(memo, tags, ";")


def __split2move_list(split):
    return [
        Split2Move(
            split["tran_acct_from"],  # Set to acct_path_and_name for look up
            Decimal(split["tran_amount"]),
            __combined_memo_tags(split["tran_memo"], split["tran_tags"]),
        ),
        Split2Move(
            split["tran_acct_to"],
            Decimal(-split["tran_amount"]),
            __combined_memo_tags(split["tran_memo"], split["tran_tags"]),
        ),
    ]


def __transaction2move(
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


def __build_multi_splits_tran(split_group):
    splits = split_group.apply(__split2move_list, axis=1)
    splits_list = [elem for item in splits for elem in item]
    return __transaction2move(
        posted=datetime.strptime(split_group["tran_date"].iat[0], "%m/%d/%Y").date(),
        description=split_group.tran_description.iat[0],
        notes=split_group.tran_memo.iat[0],
        num=split_group.tran_fitid.iat[0],
        splits=splits_list,
    )


def __build_single_splits_tran(split_data: pd.Series) -> Transaction2Move:
    splits_list = __split2move_list(split_data)
    return __transaction2move(
        posted=datetime.strptime(split_data["tran_date"], "%m/%d/%Y").date(),
        description=split_data["tran_description"],
        notes=split_data["tran_memo"],
        num=split_data["tran_fitid"],
        splits=splits_list,
    )


def __processed_transactions(transactions: pd.DataFrame):
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
                __build_multi_splits_tran
            )
        ).to_list()
        if len(multi_splits_data) > 0
        else []
    )
    single_split_transactions = (
        single_splits_data.apply(__build_single_splits_tran, axis=1).to_list()
        if len(single_splits_data) > 0
        else []
    )
    return multi_split_transactions + single_split_transactions


def mapped_transactions(raw_transactions: pd.DataFrame):
    """Function to map csv imported transaction data to a
    list of transactions ready for saving to a GnuCash file.

    TODO: raw_transactions is a bad name since these may come from
        accounts_map module.
    """
    return __processed_transactions(raw_transactions)
