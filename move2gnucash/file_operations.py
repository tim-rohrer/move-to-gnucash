import pandas as pd

def fetch_csv_data(file_to_open):
    """Read all csv contents of file and return DataFrame"""
    try:
        return pd.read_csv(file_to_open)
    except FileNotFoundError as exc:
        raise FileNotFoundError("File not found") from exc
    except Exception:
        print("Some weird error occurred")

