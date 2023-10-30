"""Move2GnuCash"""
import argparse
from unicodedata import category

from piecash import Book, create_book, GnucashException, open_book

from move2gnucash.migrations import *


class CapitalizedHelpFormatter(argparse.HelpFormatter):
    """Class needed to write command line help using proper English."""

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = "Usage: "
        return super(CapitalizedHelpFormatter, self).add_usage(usage, actions, groups, prefix)


parser = argparse.ArgumentParser(add_help=False, formatter_class=CapitalizedHelpFormatter)
parser._positionals.title = "Positional arguments"
parser._optionals.title = "Optional arguments"

parser.add_argument(
    "-v",
    "--version",
    action="version",
    version="%(prog)s 1.0",
    help="Show program's version number and exit.",
)

parser.add_argument(
    "input_file", help="The csv file containing the input data. Typical extension: '.csv'."
)
parser.add_argument(
    "output_file",
    help="The name of the GnuCash file to create/write. Typical extension: '.gnucash'.",
)
parser.add_argument(
    "action",
    choices=["ACCTS", "CATS", "IE"],
    help="Specify migration action. ACCTS for accounts/balances; CATS for categories; IE for income and expense transactions.",
)
parser.add_argument(
    "-d", "--dry-run", help="Executes without writing a GnuCash file.", action="store_true"
)
parser.add_argument(
    "-h",
    "--help",
    action="help",
    default=argparse.SUPPRESS,
    help="Show this help message and exit.",
)

args = parser.parse_args()


def create_memory_book() -> Book:
    return create_book(currency="USD")


def get_book(book_name: str, dry_run: bool) -> Book:
    try:
        book_instance = open_book(book_name, readonly=False)
        print(
            "Existing book opened, and data will be added to it (unless dry-run is True). If you meant to create a new book, re-run using a different book name."
        )
        if dry_run:
            book_instance = create_memory_book()
            print("Since dry-run is True, an empty in-memory book was created.")

    except GnucashException:
        print(
            "Book doesn't exists...creating. If dry-run is True, the returned book instance will be in-memory vice a file."
        )
        if dry_run:
            book_instance = create_memory_book()
        else:
            book_instance: Book = create_book(args.output_file, currency="USD")
    return book_instance


book = get_book(args.output_file, args.dry_run)

match args.action:
    case "ACCTS":
        opening_balances(args.input_file, book)
        print("Accounts and opening balances imported.")
    case "CATS":
        category_accounts(args.input_file, book)
        print("Categories imported as accounts.")
    case "IE":
        transactions(args.input_file, book)
    case _:
        print("Something weird occurred.")

book.close()
