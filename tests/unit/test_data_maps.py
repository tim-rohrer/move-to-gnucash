"""test_data_maps.py"""

from decimal import Decimal

from move2gnucash.data_maps import mapped_accounts, mapped_transactions


def test_mapped_accounts(prepared_account_data, new_accounts_list):
    """
    GIVEN a Pandas DataFrame produced by the data_preparation module,
    WHEN executed by mapped_accounts,
    THEN a list of Account2Move objects is returned
    """
    result = mapped_accounts(prepared_account_data)

    assert len(result) == 3
    assert result == new_accounts_list


def test_mapped_accounts_new_book(prepared_account_data, new_accounts_list_new_book):
    """
    GIVEN a Pandas DataFrame produced by the data_preparation module,
    WHEN executed by mapped_accounts with new_book=True,
    THEN a list of Account2Move objects including initial Equity
        accounts is returned.
    """
    result = mapped_accounts(prepared_account_data, new_book=True)

    assert len(result) == 5
    assert result == new_accounts_list_new_book


def test_map_multi_split_transactions(prepared_transactions):
    """
    GIVEN a Pandas DataFrame fetched from a transactions csv
        and filtered for 'S' splits
    WHEN executed by transactions
    THEN a list of Transaction2Move objects is returned of
        the correct length and splits with the correct
        Decimal of amounts, and memos
    """

    result = mapped_transactions(
        prepared_transactions.loc[prepared_transactions["tran_split"] == "S"]
    )

    assert len(result) == 2  # Two transactions
    assert len(result[0].splits) == 6  # the first with three Quicken splits double entry'd
    assert len(result[1].splits) == 4  # and the second with two Quicken splits doubled.
    assert (result[0].splits[0].value) == Decimal("8.14")


def test_map_single_split_transactions(prepared_transactions):
    """
    GIVEN a Pandas DataFrame fetched from a transactions csv
        and filtered for single splits
    WHEN executed by mapped_transactions
    THEN a list of Transaction2Move objects is returned of
        the correct length and splits with the correct
        Decimal of amounts, and memos
    """
    data_frame = prepared_transactions.loc[prepared_transactions["tran_split"] != "S"]

    result = mapped_transactions(data_frame)

    assert len(result) == 4
    assert result[0].num == "201612300900000000002"
    assert result[0].splits[0].value == Decimal(200.00)
    assert result[0].splits[1].account == "Expenses:Education"
    assert result[0].splits[1].value == Decimal(-200.00)
    assert (
        result[0].splits[0].memo
        == "Transfer to Checking; college, john, food allowance, room & board, university"
    )


def test_map_bulk_transactions(prepared_transactions):
    """
    GIVEN a Pandas DataFrame fetched from a transactions csv
    WHEN executed by mapped_transactions
    THEN a list of Transaction2Move object is returned
    """
    assert len(mapped_transactions(prepared_transactions)) == 6
