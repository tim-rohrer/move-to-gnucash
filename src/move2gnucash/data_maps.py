"""
Contains the classes and functions to map account and
transaction data from the csv in Pandas DataFrame for
processing, and ultimately to the lists for writing to
a GnuCash file.
"""
from dataclasses import dataclass
from datetime import datetime

from piecash.core.account import Account
from piecash.core.commodity import Commodity


@dataclass
class Account2Move:
    """Class to keep track of accounts and categories being moved to GnuCash."""

    name: str
    type: str
    parent: str | Account
    commodity: str | Commodity
    placeholder: bool
    description: str


@dataclass
class Split2Move:
    """Class to keep track of splits to be moved."""

    account: str
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


# def accounts_and_balances(data: pd.DataFrame):
#     data.assign(account_names=lambda data: data["Accounts"].map(lambda Accounts: Accounts))
#     # data["account_name"] = data["Accounts"].map({})
#     return data
#     # return pd.DataFrame({"accounts": ["Assets"],
#     #                      "balances": ["placeholder"]})
