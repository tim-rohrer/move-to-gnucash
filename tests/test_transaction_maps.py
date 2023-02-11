"""test_transaction_maps.py"""
from decimal import Decimal

from numpy import result_type
from move2gnucash.transaction_maps import mapped_transactions


def test_map_multi_split_transactions(fixture_transactions_in):
    """
    GIVEN a Pandas DataFrame fetched from a transactions csv
        and filtered for 'S' splits
    WHEN executed by mapped_transactions
    THEN a list of Transaction2Move objects is returned of
        the correct length and splits with the correct
        Decimal of amounts, and memos
    """

    result = mapped_transactions(
        fixture_transactions_in.loc[fixture_transactions_in["tran_split"] == "S"]
    )

    assert len(result) == 2  # Two transactions
    assert len(result[0].splits) == 6  # the first with three Quicken splits double entry'd
    assert len(result[1].splits) == 4  # and the second with two Quicken splits doubled.
    assert (result[0].splits[0].value) == Decimal(-8.14)


def test_map_single_split_transactions(fixture_transactions_in):
    """
    GIVEN a Pandas DataFrame fetched from a transactions csv
        and filtered for single splits
    WHEN executed by mapped_transactions
    THEN a list of Transaction2Move objects is returned of
        the correct length and splits with the correct
        Decimal of amounts, and memos
    """
    data_frame = fixture_transactions_in.loc[fixture_transactions_in["tran_split"] != "S"]

    result = mapped_transactions(data_frame)

    assert len(result) == 4
    assert result[0].num == "201612300900000000002"
    assert result[0].splits[0].value == Decimal(-200.00)
    assert result[0].splits[1].account == "Education"
    assert result[0].splits[1].value == Decimal(200.00)
    assert (
        result[0].splits[0].memo
        == "Transfer to Checking; college, john, food allowance, room & board, university"
    )


def test_map_bulk_transactions(fixture_transactions_in):
    """
    GIVEN a Pandas DataFrame fetched from a transactions csv
    WHEN executed by mapped_transactions
    THEN a list of Transaction2Move object is returned
    """
    assert len(mapped_transactions(fixture_transactions_in)) == 6
