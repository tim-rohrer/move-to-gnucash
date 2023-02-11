"""
Contains the classes and functions to map account data 
from the csv in Pandas DataFrame for processing, and 
ultimately to the lists for writing to a GnuCash file.
"""
from dataclasses import dataclass

import pandas as pd
from piecash.core.account import Account
from piecash.core.commodity import Commodity

from move2gnucash.transaction_maps import mapped_transactions


@dataclass
class Account2Move:
    """Class to keep track of accounts and categories being moved to GnuCash."""

    name: str  # Short name of account
    type: str
    parent: str | Account
    commodity: str | Commodity
    placeholder: bool
    description: str


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


def __account2move(acct):
    return Account2Move(
        name=acct["acct_name"],
        type=acct["acct_type"],
        parent=acct["acct_parent"],
        commodity=acct["acct_commodity"],
        placeholder=acct["acct_placeholder"],
        description=acct["acct_description"],
    )


def __prepared_balances_transactions(
    data: pd.DataFrame, opening_balances_acct: str
) -> pd.DataFrame:
    default_memo = "Migrated by Move2GnuCash"
    data["tran_split"] = ""
    data[
        "tran_acct_to"
    ] = opening_balances_acct  # Must be full_path_name of account to support look up.
    data["tran_description"] = "Opening Balance"
    data[["tran_memo", "tran_tags", "tran_fitid"]] = [default_memo, "", ""]
    data = data.rename(
        columns={
            "acct_path_and_name": "tran_acct_from",
            "acct_balance": "tran_amount",
            "acct_balance_date": "tran_date",
        }
    )
    return data


def accounts_and_balances(accounts_data: pd.DataFrame):
    """Function to provide the list of mapped accounts, the special
    Equity:Opening Balances account, and associated balances."""
    opening_balances_acct = "Equity:Opening Balances"
    accounts_data["acct_placeholder"] = accounts_data["acct_balance"].isna()
    accounts_data["acct_commodity"] = "USD"
    accounts_data["acct_parent"] = parent_of(accounts_data["acct_path_and_name"])
    accounts_data["acct_name"] = name_of(accounts_data["acct_path_and_name"])
    accounts = accounts_data.apply(__account2move, axis=1).to_list() + [
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

    transactions = mapped_transactions(
        __prepared_balances_transactions(
            accounts_data.loc[~accounts_data["acct_balance"].isna()].copy(),
            opening_balances_acct,
        ),
    )

    return {
        "accounts": accounts,
        "transactions": transactions,
    }
