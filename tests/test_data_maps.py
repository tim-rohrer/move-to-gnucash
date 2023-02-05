"""test_data_maps.py"""
from datetime import datetime
from unittest import mock
from move2gnucash.data_maps import accounts_and_balances


def test_simple_account_map_accounts(simple_data_frame_in, simple_fixture_accounts_out):
    """
    GIVEN a DF fetched from the opening_balances CSV
    WHEN executed by build_accounts_balances
    THEN a list of accounts  is returned
    """
    assert accounts_and_balances(simple_data_frame_in)["accounts"] == simple_fixture_accounts_out


# @patch("move2gnucash.data_maps.get_now")
def test_simple_account_map_balances_transactions(
    simple_data_frame_in,
    fixture_opening_balances_simple,
):
    """
    GIVEN a Pandas DataFrame fetched from the opening_balances CSV
    WHEN executed by build_accounts_balances
    THEN a list opening balance transactions is returned
    """
    with mock.patch(
        "move2gnucash.data_maps.get_now", return_value=datetime(2023, 2, 1, 0, 0, 0, 0)
    ):
        assert (
            accounts_and_balances(simple_data_frame_in)["transactions"]
            == fixture_opening_balances_simple
        )
