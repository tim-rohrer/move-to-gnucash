import pandas as pd

def fetch_csv_data(file_to_open):
    """Read all csv contents of file and return DataFrame"""
    return pd.read_csv(file_to_open)