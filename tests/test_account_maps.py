"""test_account_maps.py"""
from datetime import datetime
from unittest import mock
from move2gnucash.account_maps import accounts_and_balances


def test_simple_account_map_accounts(simple_data_frame_in, simple_fixture_accounts_out):
    """
    GIVEN a DF preprocessed to internal colum names
        after import of opening account balanced CSV
    WHEN executed by build_accounts_balances
    THEN a list of accounts is returned
    """
    result = (accounts_and_balances(simple_data_frame_in))["accounts"]

    assert len(result) == 5
    assert result == simple_fixture_accounts_out


def test_simple_account_map_balances_transactions(
    simple_data_frame_in,
    fixture_opening_balances_simple,
):
    """
    GIVEN a Pandas DataFrame preprocess to internal column names
        after being fetched from the opening_balances CSV
    WHEN executed by build_accounts_balances
    THEN a list opening balance transactions is returned
    """
    with mock.patch(
        "move2gnucash.transaction_maps.get_now", return_value=datetime(2023, 2, 1, 0, 0, 0, 0)
    ):
        result = (accounts_and_balances(simple_data_frame_in))["transactions"]

        assert len(result) == 1
        assert result == fixture_opening_balances_simple
