# Author: Dominik Harmim <harmim6@gmail.com>

"""Module that handles SQLite3 database stuff related to sorting requests."""

from contextlib import closing, contextmanager
from sqlite3 import Cursor, connect
from typing import Iterator

__DB_FILE = "requests.db"  # database file name


@contextmanager
def database() -> Iterator[Cursor]:
    """
    Open, prepare, and return a database (cursor) for working with sorting
    requests.

    The database and cursor are closed afterwards.

    :yield Iterator[Cursor]: open database cursor
    """
    with (
        closing(connect(__DB_FILE)) as connection,
        closing(connection.cursor()) as cursor,
    ):
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS request " +
            "(hash TEXT PRIMARY KEY, request TEXT)",
        )
        connection.commit()

        yield cursor
