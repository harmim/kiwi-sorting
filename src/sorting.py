# Author: Dominik Harmim <harmim6@gmail.com>

"""Module that handles sorting of itineraries."""

import pickle
from sqlite3 import Cursor

from .parsing import Itineraries, Request, SortingType


def __sort_cheapest(itineraries: Itineraries) -> None:
    """
    Sort itineraries based on price, with the most affordable ones coming first.

    :param Itineraries itineraries: itineraries to be sorted
    """
    itineraries.sort(key=lambda i: i.price.amount_eur)


def __sort_fastest(itineraries: Itineraries) -> None:
    """
    Sort itineraries by duration, with the shortest ones coming first.

    :param Itineraries itineraries: itineraries to be sorted
    """
    itineraries.sort(key=lambda i: i.duration)


def __sort_best(itineraries: Itineraries) -> None:
    """
    Sort itineraries with the best ones coming first.

    For the best ones, both duration as well as price are considered, each of
    them with a different weight.

    :param Itineraries itineraries: itineraries to be sorted
    """
    DURATION_WEIGHT = 1
    PRICE_WEIGHT = 5
    itineraries.sort(
        key=lambda i:
            DURATION_WEIGHT * i.duration + PRICE_WEIGHT * i.price.amount_eur,
    )


def sort_request(request: Request, cursor: Cursor | None = None) -> Request:
    """
    Sort itineraries using various sorting criteria.

    Sorting requests are cached to the SQLite3 database. So, the same requests
    are not sorted again.

    :param Request request: sorting request with itineraries to be sorted
    :param Cursor | None cursor: database cursor, defaults to None
    :return Request: request with sorted itineraries
    """
    request_hash = hash(request)

    # load from the cache
    if cursor is not None:
        row = cursor.execute(
            "SELECT request FROM request WHERE hash = ?",
            (request_hash,),
        ).fetchone()
        if row is not None:
            return pickle.loads(row[0])

    # for testing purposes only
    sort_request.sorted_count = getattr(sort_request, "sorted_count", 0) + 1

    if request.sorting_type == SortingType.CHEAPEST:
        __sort_cheapest(request.itineraries)
    elif request.sorting_type == SortingType.FASTEST:
        __sort_fastest(request.itineraries)
    else:
        __sort_best(request.itineraries)

    # store to the cache
    if cursor is not None:
        cursor.execute(
            "INSERT INTO request (hash, request) VALUES (?, ?)",
            (request_hash, pickle.dumps(request)),
        )
        cursor.connection.commit()

    return request
