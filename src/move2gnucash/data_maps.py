"""
Contains the classes and functions to map account and
transaction data from the csv in Pandas DataFrame for
processing, and ultimately to the lists for writing to
a GnuCash file.
"""
from dataclasses import dataclass
from datetime import datetime
import decimal
import pandas as pd

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


def parent_of(col: pd.Series) -> pd.Series:
    """Function to extract the parent account and determine roots"""
    result = col.str.rsplit(":", n=1, expand=True)
    result.loc[result[1].isna(), 0] = "root"
    return result[0]


def name_of(accts: pd.Series) -> pd.Series:
    """Function to extract short account name from fullname"""
    result = accts.str.rsplit(":", n=1, expand=True)
    result.loc[result[1].isna(), 1] = result[0]
    return result[1]


def decimal_to(value: float, precision: int) -> decimal.Decimal:
    """Function to create Decimal rounded to 'prec' number of digits"""
    decimal.getcontext().prec = precision
    return decimal.Decimal(value) * 1


def accounts_and_balances(data: pd.DataFrame):
    """Function to provide the list of mapped accounts, the special
    Equity:Opening Balances account, and associated balances."""
    data["placeholder"] = data["balance"].isna()
    data["commodity"] = "USD"
    data["parent"] = parent_of(data["account"])
    data["name"] = name_of(data["account"])
    accts = [
        Account2Move(
            name=acct.name,
            type=acct.type,
            parent=acct.parent,
            commodity=acct.commodity,
            placeholder=acct.placeholder,
            description=acct.description,
        )
        for acct in data.itertuples()
    ]
    balances = data.loc[~data["balance"].isna()]
    trans = [
        Transaction2Move(
            post_date=datetime.strptime(tran.date, "%m/%d/%Y").date(),
            enter_date=datetime.strptime(tran.date, "%m/%d/%Y"),
            currency=tran.commodity,
            description="Opening Balance",
            notes="",
            num="",
            splits=[
                Split2Move(
                    tran.account,
                    decimal_to(tran.balance, 2),
                    "",
                ),
                Split2Move(
                    "Equity:Opening Balances",
                    decimal_to(-tran.balance, 2),
                    "",
                ),
            ],
        )
        for tran in balances.itertuples()
    ]
    return {
        "accounts": accts
        + [
            Account2Move(
                name="Equity",
                type="EQUITY",
                parent="root",
                commodity="USD",
                placeholder=True,
                description="Migration from Quicken",
            ),
            Account2Move(
                name="Opening Balances",
                type="EQUITY",
                parent="Equity",
                commodity="USD",
                placeholder=False,
                description="Migration from Quicken",
            ),
        ],
        "transactions": trans,
    }
