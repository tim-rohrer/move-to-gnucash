"""test_data_preparation.py"""
from datetime import datetime
from unittest.mock import patch

import pandas as pd
from piecash import Split, Transaction

from move2gnucash.data_preparation import (
    prepared_balances,
    prepared_category_accounts,
    prepared_transactions,
)


def test_prepared_balances(balances: pd.DataFrame):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken accounts and balances,
        and an opening balances date,
    WHEN executed by prepared_balances,
    THEN a new DateFrame with a fully prepared set of data ready
        to be processed by the mapping stage (creation of new account/transaction
        objects suitable for GnuCash) will be returned.
    """
    test_date = datetime.strptime("2017_12_31", "%Y_%m_%d").date()

    test_data = {"as_of_date": test_date, "data": balances}
    res = prepared_balances(test_data)

    assert len(res) == 21
    assert all(
        w in res.columns
        for w in [
            "balance",
            "placeholder",
            "commodity",
            "name",
            "parent",
            "tran_split",
            "tran_amount",
            "tran_acct_from",
            "tran_acct_to",
            "tran_memo",
            "tran_date",
            "tran_num",
        ]
    )

    assert res.loc[5].at["tran_acct_to"] == "Assets:Savings:Savings Account"

    assert isinstance(res.loc[20].at["tran_amount"], float)
    assert res.tran_date[0] == datetime(2017, 12, 31).date()

    assert all(
        res.selected_type
        == pd.Series(
            [
                "ASSET",
                "ASSET",
                "CASH",
                "BANK",
                "ASSET",
                "BANK",
                "ASSET",
                "ASSET",
                "STOCK",
                "STOCK",
                "ASSET",
                "ASSET",
                "ASSET",
                "ASSET",
                "ASSET",
                "LIABILITY",
                "LIABILITY",
                "CREDIT",
                "CREDIT",
                "LIABILITY",
                "LIABILITY",
            ]
        )
    )


def test_prepared_balances_correct_balances(balances: pd.DataFrame):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken accounts and balances,
        and an opening balances date,
    WHEN executed by prepared_balances,
    THEN a new DateFrame with correct balances for accounts and zero balances
        for investment accounts will be returned.
    """
    test_date = datetime.strptime("2017_12_31", "%Y_%m_%d").date()

    test_data = {"as_of_date": test_date, "data": balances}
    res = prepared_balances(test_data)

    assert res.loc[20].at["tran_amount"] == -10600.00
    assert all(acct.tran_amount == 0 for acct in res.itertuples() if acct.selected_type == "STOCK")


def test_prepared_category_accounts(categories):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken categories,
    WHEN executed by prepared_category_accounts,
    THEN a new DateFrame with fully prepared set of data ready to be processed
        by the mapping stage will be returned.
    """
    res: pd.DataFrame = prepared_category_accounts(categories)

    assert len(res) == 24
    assert all(w in res.columns for w in ["placeholder", "commodity", "name", "parent"])
    assert all(w in ["INCOME", "EXPENSE"] for w in res.selected_type.to_list())


def test_prepared_transactions_input_check(all_transactions, detailed_book):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken transactions,
    WHEN executed by prepared_transactions also passed a book,
    THEN a new DataFrame with the columns necessary for subsequent  processing
        is returned and the date is of the correct form.
    """
    res: pd.DataFrame = prepared_transactions(detailed_book, all_transactions)["non_invest"]

    assert all(
        w in res.columns
        for w in [
            "tran_date",
            "tran_description",
            "tran_memo",
            "tran_num",
            "tran_split",
            "tran_acct_from",
            "tran_acct_to",
        ]
    )


def test_prepared_transactions_investment(all_transactions, detailed_book):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken transactions,
    WHEN executed by prepared_transactions also passed a book,
    THEN a new DataFrame with the columns necessary for subsequent processing
        is returned and the date is of the correct form.
    """
    res: pd.DataFrame = prepared_transactions(detailed_book, all_transactions)["invest"]

    assert len(res) == 1
    print(res.invest_acct, res.account)


def test_prepared_transactions_filtered(all_transactions, detailed_book):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken transactions,
    WHEN executed by prepared_transactions also passed a book with an opening balance,
    THEN a new DataFrame without transactions prior to the opening balance is returned.
    """
    res: pd.DataFrame = prepared_transactions(detailed_book, all_transactions)["non_invest"]

    assert res.tran_date[0] == datetime(2017, 1, 1).date()


def test_prepared_transactions_memo(all_transactions, detailed_book):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken transactions,
    WHEN executed by prepared_transactions also passed a book,
    THEN a new DataFrame with properly formed memo is formed
    """
    res: pd.DataFrame = prepared_transactions(detailed_book, all_transactions)["non_invest"]

    assert res.tran_memo[1] == "college, john, rent, room & board, university"


@patch("move2gnucash.data_preparation._manual_choice")
def test_prepared_transactions_identify_transfer(mock_input, all_transactions, detailed_book):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken transactions,
    WHEN executed by prepared_transactions also passed a book,
    THEN a new DataFrame with row 8 acct_to set to transfer account cash.
    """
    mock_input.return_value = "Shouldn't be called!"
    res: pd.DataFrame = prepared_transactions(detailed_book, all_transactions)["non_invest"]

    mock_input.assert_not_called()
    assert res.tran_acct_to[8] == "Assets:Cash:Cash"


def test_prepared_transactions_full_acct_names(all_transactions, detailed_book):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken transactions,
    WHEN executed by prepared_transactions also passed a book,
    THEN a new DataFrame fully developed with referenced accounts
        is returned.
    """
    res: pd.DataFrame = prepared_transactions(detailed_book, all_transactions)["non_invest"]

    assert res.tran_acct_to[0] == "Expenses:Education"
    assert res.tran_acct_from[0] == "Assets:Cash:Checking"
    assert res.tran_acct_to[9] == "Income:Salary"


def test_prepared_transactions_amounts(all_transactions, detailed_book):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken transactions,
    WHEN executed by prepared_transactions also passed a book,
    THEN a new DataFrame fully developed with correctly signed amounts is returned.
    """
    res: pd.DataFrame = prepared_transactions(detailed_book, all_transactions)["non_invest"]

    assert res.tran_amount[0] > 0
    assert res.tran_amount[9] < 0
