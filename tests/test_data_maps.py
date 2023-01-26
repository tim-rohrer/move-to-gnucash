import pandas as pd
import pytest

from move2gnucash.data_maps import accounts_and_balances

@pytest.fixture(scope = "module")
def complex_data_frame():
    yield pd.DataFrame({"Accounts": [
        "Assets",
        "Cash",
        "- Cash",
        "- Checking One",
        "- Checking Two",
        "- Total Cash",
        "Savings",
        "- Spouse Savings",
        "- Family Savings",
        "- Total Savings",
        "Property",
        "- 2012 Silverado",
        "- 2012 Camper",
        "- Total Property",
        "Total Assets",
        "Liabilities",
        "Credit Card",
        "- Apple Card",
        "- Credit Card",
        "- Total Credit Card",
        "Loan",
        "- Student Loan",
        "- Total Loan",
        "Total Liabilities",
        ],
        "12/31/2016": [
        "NaN",
        "NaN",
        77.12,
        440.84,
        235.38,
        753.34,
        "NaN",
        987.12,
        3250,
        4237.12,
        "NaN",
        30975,
        0,
        39975,
        44965.46,
        "NaN",
        "NaN",
        0,
        -973.4,
        -973.4,
        "NaN",
        -10500,
        -10650,
        -11623
        ]})

@pytest.fixture(scope = "module")
def empty_data_frame():
    """Provide empty account list, which should error"""
    yield pd.DataFrame({"Accounts": [], "12/31/2016": []})

@pytest.fixture(scope = "module")
def simple_data_frame():
    yield pd.DataFrame({"Accounts": ["Assets","Current Assets","- Checking","Total Current Assets","Total Assets"],
                        "12/31/2016": ["NaN","NaN",1000.00,1000.00,1000.00]})

def test_simple(simple_data_frame):
    """
    GIVEN A DataFrame fetched from the opening_balances CSV
    WHEN processed by accounts_and_opening_balances
    THEN a Pandas DataFrame exists with final account names and opening balances.
    """

    pd.testing.assert_frame_equal(
        accounts_and_balances(simple_data_frame),
        pd.DataFrame({"accounts": ["Assets", "Assets:Current Assets","Assets:Current Assets:Checking"],
                        "balances": ["ph","ph",1000.00]
                    })
    )