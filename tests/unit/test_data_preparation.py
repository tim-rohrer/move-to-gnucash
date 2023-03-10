"""test_data_preparation.py"""
import pandas as pd

from move2gnucash.data_preparation import (
    prepared_balances,
    prepared_category_accounts,
    prepared_transactions,
)


def test_prepared_balances(balances: pd.DataFrame):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken accounts and balances,
    WHEN executed by prepared_balances,
    THEN a new DateFrame with a fully prepared set of data ready
        to be processed by the mapping stage (creation of new account/transaction
        objects suitable for GnuCash) will be returned.
    """

    res = prepared_balances(balances)

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
    assert res.loc[20].at["tran_amount"] == -10600.00
    assert isinstance(res.loc[20].at["tran_amount"], float)
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


def test_prepared_transactions(expenses):
    """
    GIVEN a Pandas DataFrame from a csv import of Quicken transactions,
    WHEN executed by prepared_transactions also passed a root account designator,
    THEN a new DataFrame with a fully prepared set of data ready to be
        processed by the mapping stated will be returned.
    """
    res: pd.DataFrame = prepared_transactions("Expenses", expenses)

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
    # assert all(list(map(lambda x: x.startswith("Expenses"), res.tran_acct_to)))
    assert res.tran_acct_to[0] == "Expenses:Education"
    assert res.tran_memo[1] == "college, john, rent, room & board, university"
    assert res.tran_acct_to[8] == "Cash"
