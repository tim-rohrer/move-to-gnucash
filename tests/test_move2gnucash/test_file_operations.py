from unittest.mock import patch, Mock

import pytest
import pandas as pd

# import move2gnucash.file_operations
from move2gnucash.file_operations import fetch_csv_data
# from .move2gnucash.file_operations import fetch_csv_data

@patch("pandas.read_csv")
def test_fetch_csv_data_works(mock_read: Mock):
    """
    GIVEN fetch_csv_data with an existing properly formatted csv file
    WHEN executed
    THEN a Pandas DataFrame is returned with the data
    """

    df = pd.DataFrame({"foo_id": [1, 2, 3, 4, 5]})

    results = fetch_csv_data("file")

    mock_read.assert_called_once_with("file")
    # pd.testing.assert_frame_equal(results, df)
