"""
do_example.py
"""

from move2gnucash.file_operations import (
    add_transactions,
    create_accounts,
    create_gnucash_book,
    fetch_csv_data,
)
from move2gnucash.data_maps import accounts_and_balances

df = fetch_csv_data("examples/sample_balances_user.csv")

data = accounts_and_balances(df)

book = create_gnucash_book("example.gnucash", overwrite=True)
create_accounts(book, data["accounts"])
add_transactions(book, data["transactions"])
book.close()
