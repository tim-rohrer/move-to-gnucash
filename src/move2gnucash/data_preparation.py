"""
Contains the functions that work with Pandas DataFrames to to prepare raw data 
into columns ready for mapping and subsequent file operations. 
"""
import configparser
import re

import numpy as np
import pandas as pd

from move2gnucash.utils import combined_strings_by, custom_join


def _parent_of(col: pd.Series) -> pd.Series:
    """Function to extract the parent account and determine roots"""
    result = col.str.rsplit(":", n=1, expand=True)
    result.loc[result[1].isna(), 0] = "root"
    return result[0]


def _name_of(accts: pd.Series) -> pd.Series:
    """Function to extract short account name from fullname"""
    result = accts.str.rsplit(":", n=1, expand=True)
    result.loc[result[1].isna(), 1] = result[0]
    return result[1]


def _mapped_column_names(input_df: pd.DataFrame, map_dict: dict) -> pd.DataFrame:
    """Function to rename user provided columns in csv to internal
    column names for processing.
    """
    mapping_dict = {value: key for key, value in map_dict.items()}
    return input_df.rename(columns=mapping_dict)


def _sub_paths_from_raw_refs(series: pd.Series) -> pd.Series:
    expanded: pd.DataFrame = series.str.split(" - ", expand=True)

    expanded.fillna(value="Skip", inplace=True)  # Elements of None (missing) marked with "Skip",
    expanded[expanded == ""] = np.NaN  # and true empty elements marked NaN,
    expanded.fillna(
        method="ffill", inplace=True
    )  # so they can be filled with real value from an earlier row
    expanded.replace("Skip", "", inplace=True)  # and "Skip" label is removed.

    expanded["completed"] = expanded.apply(custom_join, axis=1)

    return expanded["completed"]


def _total_lines_removed(raw_data: pd.DataFrame, col: str) -> pd.DataFrame:
    mask = raw_data[col].str.contains(":Total")
    return raw_data[~mask]


def _prepared_account_names(root_account_names: pd.DataFrame) -> pd.DataFrame:
    """
    Function to transform a raw list of accounts or categories from Quicken's exported
    report into a fully developed list of accounts for mapping opening balances to GnuCash.
    """
    root_account_names["root"].fillna(method="ffill", inplace=True)

    root_account_names["path_and_name"] = root_account_names["root"] + _sub_paths_from_raw_refs(
        root_account_names["account"]
    )

    prepared_names: pd.DataFrame = _total_lines_removed(root_account_names, "path_and_name")

    return prepared_names


def _add_account_types_of(accounts: pd.DataFrame) -> None:
    """Uses full account name and placeholder status to guess GnuCash account_type.
    As of 2/2023, reference links were valid:
    https://code.gnucash.org/docs/MAINT/group__Account.html#ga398c5d6f7a5127db7b81789e05262908
    https://piecash.readthedocs.io/en/master/_modules/piecash/core/account.html?highlight=types
    """

    def chosen_type(acct: pd.Series) -> str:
        candidate_types, placeholder = acct
        num_candidates = len(candidate_types)
        acct_choice_index = num_candidates - 1 if num_candidates > 0 else 0
        placeholder_choice_index = num_candidates - 2 if num_candidates > 1 else 0

        choice = (
            candidate_types[0]
            if candidate_types[0] in ["INCOME", "EXPENSE"]
            else (
                candidate_types[placeholder_choice_index]
                if placeholder is True
                else candidate_types[acct_choice_index]
            )
        )
        return choice

    account_types = {
        "ASSET": {"ASSET", "ASSETS"},
        "LIABILITY": {"LIABILITY", "LIABILITIES"},
        "EQUITY": {"EQUITY", "EQUITIES"},
        "INCOME": {"INCOME", "INCOMES"},
        "EXPENSE": {"EXPENSE", "EXPENSES"},
        "CASH": {"CASH"},
        "BANK": {"CHECKING", "ACCOUNT"},
        "CREDIT": {"CREDIT CARD", "CREDIT CARDS"},
        "PAYABLE": {"ACCOUNTS PAYABLE", "PAYABLE"},
        "RECEIVABLE": {"ACCOUNTS RECEIVABLE", "RECEIVABLES"},
        "STOCK": {"BROKERAGE"},
        "MUTUAL": {"MUTUAL FUND", "MONEY MARKET FUND", "FUND"},
    }
    reversed_dict = {i: k for k, v in account_types.items() for i in v}

    accounts["upper_path_name"] = accounts.path_and_name.str.upper()
    accounts["candidate_types"] = [
        [reversed_dict[y] for y in x]
        for x in accounts.upper_path_name.str.findall(
            "|".join(reversed_dict.keys()), flags=re.IGNORECASE
        )
    ]
    accounts["selected_type"] = accounts[["candidate_types", "placeholder"]].apply(
        chosen_type, axis=1
    )


def prepared_balances(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Provides a Pandas DataFrame of account data and balances prepared from a raw list
    of account data/balances imported from Quicken's exported balances report.

    The returned DataFrame contains the information sufficient to map both the accounts
    and the transactions necessary to create balances in GnuCash, specifically opening
    balances.
    """
    named_accounts = _prepared_account_names(raw_data)

    prepared_data = named_accounts[["path_and_name", "balance"]].reset_index(drop=True)
    prepared_data["placeholder"] = prepared_data["balance"].isna()

    _add_account_types_of(prepared_data)

    prepared_data["commodity"] = "USD"
    prepared_data["description"] = "Migrated by Move2GnuCash"
    prepared_data["tran_description"] = prepared_data.description

    prepared_data["parent"] = _parent_of(prepared_data["path_and_name"])
    prepared_data["name"] = _name_of(prepared_data["path_and_name"])
    prepared_data.rename(columns={"path_and_name": "tran_acct_to"}, inplace=True)

    prepared_data["tran_split"] = ""
    prepared_data["tran_acct_from"] = "Opening Balances"
    prepared_data["tran_amount"] = prepared_data["balance"].astype(float)
    prepared_data["tran_memo"] = prepared_data.description
    prepared_data["tran_date"] = "12/31/2016"
    prepared_data["tran_num"] = 1

    return prepared_data


def prepared_category_accounts(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Provides a Pandas DataFrame of account data prepared from a raw list of categories imported
    from Quicken's exported category report.
    """
    named_accounts: pd.Series = _prepared_account_names(raw_data)

    prepared_data = named_accounts[["path_and_name", "balance"]].reset_index(drop=True)
    prepared_data["placeholder"] = prepared_data["balance"].isna()

    _add_account_types_of(prepared_data)

    prepared_data["commodity"] = "USD"
    prepared_data["description"] = "Migrated by Move2GnuCash"

    prepared_data["parent"] = _parent_of(prepared_data["path_and_name"])
    prepared_data["name"] = _name_of(prepared_data["path_and_name"])

    return prepared_data


def _combined_memo_tags(_: pd.DataFrame) -> str:
    memo_notes, tags = _
    return combined_strings_by(memo_notes, tags, ";")


def prepared_transactions(root: str, raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Provides a Pandas DataFrame of transaction data prepared from a raw list of income or expense
    transactions imported from Quicken's transaction export -> csv feature.

    A string reflecting the root account, (typically "Income" or "Expenses"), must be provided due
    to limitations with Quicken's export file.
    """

    config = configparser.ConfigParser()
    config.read("src/move2gnucash/field_mappings.ini")
    prepared_data = _mapped_column_names(raw_data, config["transactions"])

    prepared_data.fillna("", inplace=True)
    prepared_data["tran_num"] = prepared_data.fitid
    prepared_data["tran_memo"] = prepared_data[["memo_notes", "tags"]].agg(
        _combined_memo_tags, axis=1
    )

    prepared_data["root"] = root
    _prepared_account_names(prepared_data)

    # Next line should handle internal transfers contained in Quicken data by
    # assigning the Transfer name to tran_acct_to when the former is defined.
    prepared_data["tran_acct_to"] = np.where(
        prepared_data.transfer == "", prepared_data.path_and_name, prepared_data.transfer
    )

    prepared_data["tran_date"] = prepared_data["date"]

    return prepared_data
