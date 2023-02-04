"""test_data_maps.py"""
from move2gnucash.data_maps import accounts_and_balances


def test_simple_account_map_accounts(simple_data_frame_in, simple_fixture_accounts_out):
    """
    GIVEN a DF fetched from the opening_balances CSV
    WHEN executed by build_accounts_balances
    THEN a list of accounts  is returned
    """
    assert accounts_and_balances(simple_data_frame_in)["accounts"] == simple_fixture_accounts_out


def test_simple_account_map_balances_transactions(
    simple_data_frame_in, fixture_opening_balances_simple
):
    """
    GIVEN a Pandas DataFrame fetched from the opening_balances CSV
    WHEN executed by build_accounts_balances
    THEN a list opening balance transactions is returned
    """

    assert (
        accounts_and_balances(simple_data_frame_in)["transactions"]
        == fixture_opening_balances_simple
    )
