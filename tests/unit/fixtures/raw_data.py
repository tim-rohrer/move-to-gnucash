"""Fixture file to support testing data_preparation functions.

"""

import pandas as pd
import pytest


@pytest.fixture()
def all_transactions():
    """
    Fixture READ FROM FILE to provide DataFrame reflecting
    preprocessed csv transactions (tran).
    """

    return pd.read_csv("tests/unit/fixtures/inc_exp_trans.fixture.csv", thousands=",")


@pytest.fixture()
def balances():
    """
    Fixture READ FROM FILE containing net worth file.

    Used by test_prepared_balances in
        test_data_preparation.py
    """
    return pd.read_csv(
        "tests/unit/fixtures/2016_12_31_net_worth.fixture.csv",
        header=None,
        names=["root", "account", "balance"],
        thousands=",",
    )


@pytest.fixture()
def categories() -> pd.DataFrame:
    """
    Fixture containing raw data from an export of a Quicken Categories report.

    Used by test_prepared_category_accounts in test_data_preparation.py
    """
    return pd.read_csv(
        "tests/unit/fixtures/categories.fixture.csv",
        header=None,
        names=["root", "account", "balance"],
    )
