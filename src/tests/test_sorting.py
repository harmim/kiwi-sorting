# Author: Dominik Harmim <harmim6@gmail.com>

"""Testing the itineraries sorting."""

from ..db import database
from ..parsing import Request
from ..sorting import sort_request


def test_sort_cheapest() -> None:
    """Test sorting itineraries by cheapest ones."""

    # same currency
    request1 = sort_request(Request({
        "sorting_type": "cheapest",
        "itineraries": [
            {
                "id": "foo",
                "duration_minutes": 10,
                "price": {
                    "amount": 200,
                    "currency": "CZK",
                },
            },
            {
                "id": "bar",
                "duration_minutes": 20,
                "price": {
                    "amount": 100,
                    "currency": "CZK",
                },
            },
        ],
    }))
    request2 = Request({
        "sorting_type": "cheapest",
         "itineraries": [
             {
                "id": "bar",
                "duration_minutes": 20,
                "price": {
                    "amount": 100,
                    "currency": "CZK",
                },
            },
             {
                "id": "foo",
                "duration_minutes": 10,
                "price": {
                    "amount": 200,
                    "currency": "CZK",
                },
            },
         ],
    })
    assert request1.to_json() == request2.to_json()

    # different currencies
    request1 = sort_request(Request({
        "sorting_type": "cheapest",
        "itineraries": [
            {
                "id": "foo",
                "duration_minutes": 10,
                "price": {
                    "amount": 10,
                    "currency": "USD",
                },
            },
            {
                "id": "bar",
                "duration_minutes": 20,
                "price": {
                    "amount": 100,
                    "currency": "CZK",
                },
            },
        ],
    }))
    request2 = Request({
        "sorting_type": "cheapest",
         "itineraries": [
             {
                "id": "bar",
                "duration_minutes": 20,
                "price": {
                    "amount": 100,
                    "currency": "CZK",
                },
            },
             {
                "id": "foo",
                "duration_minutes": 10,
                "price": {
                    "amount": 10,
                    "currency": "USD",
                },
            },
         ],
    })
    assert request1.to_json() == request2.to_json()


def test_sort_fastest() -> None:
    """Test sorting itineraries by fastest ones."""

    request1 = sort_request(Request({
        "sorting_type": "fastest",
        "itineraries": [
            {
                "id": "foo",
                "duration_minutes": 300,
                "price": {
                    "amount": 100,
                    "currency": "EUR",
                },
            },
            {
                "id": "bar",
                "duration_minutes": 150,
                "price": {
                    "amount": 200,
                    "currency": "EUR",
                },
            },
        ],
    }))
    request2 = Request({
        "sorting_type": "fastest",
         "itineraries": [
             {
                "id": "bar",
                "duration_minutes": 150,
                "price": {
                    "amount": 200,
                    "currency": "EUR",
                },
            },
             {
                "id": "foo",
                "duration_minutes": 300,
                "price": {
                    "amount": 100,
                    "currency": "EUR",
                },
            },
         ],
    })
    assert request1.to_json() == request2.to_json()


def test_sort_best() -> None:
    """Test sorting itineraries by best ones."""

    request1 = sort_request(Request({
        "sorting_type": "best",
        "itineraries": [
            {
                "id": "foo",
                "duration_minutes": 300,
                "price": {
                    "amount": 102,
                    "currency": "EUR",
                },
            },
            {
                "id": "bar",
                "duration_minutes": 320,
                "price": {
                    "amount": 100,
                    "currency": "EUR",
                },
            },
        ],
    }))
    request2 = Request({
        "sorting_type": "best",
         "itineraries": [
             {
                "id": "foo",
                "duration_minutes": 300,
                "price": {
                    "amount": 102,
                    "currency": "EUR",
                },
            },
             {
                "id": "bar",
                "duration_minutes": 320,
                "price": {
                    "amount": 100,
                    "currency": "EUR",
                },
            },
         ],
    })
    assert request1.to_json() == request2.to_json()

    request1 = sort_request(Request({
        "sorting_type": "best",
        "itineraries": [
            {
                "id": "foo",
                "duration_minutes": 312,
                "price": {
                    "amount": 102,
                    "currency": "EUR",
                },
            },
            {
                "id": "bar",
                "duration_minutes": 320,
                "price": {
                    "amount": 100,
                    "currency": "EUR",
                },
            },
        ],
    }))
    request2 = Request({
        "sorting_type": "best",
         "itineraries": [
             {
                "id": "bar",
                "duration_minutes": 320,
                "price": {
                    "amount": 100,
                    "currency": "EUR",
                },
            },
             {
                "id": "foo",
                "duration_minutes": 312,
                "price": {
                    "amount": 102,
                    "currency": "EUR",
                },
            },
         ],
    })
    assert request1.to_json() == request2.to_json()


def test_caching() -> None:
    """Test caching of sorting requests."""

    # same request again
    with database() as cursor:
        sort_request(Request({
            "sorting_type": "fastest",
            "itineraries": [
                {
                    "id": "foo",
                    "duration_minutes": 300,
                    "price": {
                        "amount": 100,
                        "currency": "EUR",
                    },
                },
                {
                    "id": "bar",
                    "duration_minutes": 150,
                    "price": {
                        "amount": 200,
                        "currency": "EUR",
                    },
                },
            ],
        }), cursor)
        old_sorted_count = getattr(sort_request, "sorted_count", 0)
        sort_request(Request({
            "sorting_type": "fastest",
            "itineraries": [
                {
                    "id": "foo",
                    "duration_minutes": 300,
                    "price": {
                        "amount": 100,
                        "currency": "EUR",
                    },
                },
                {
                    "id": "bar",
                    "duration_minutes": 150,
                    "price": {
                        "amount": 200,
                        "currency": "EUR",
                    },
                },
            ],
        }), cursor)
        assert old_sorted_count == getattr(sort_request, "sorted_count", 0)

    # different requests
    with database() as cursor:
        sort_request(Request({
            "sorting_type": "fastest",
            "itineraries": [
                {
                    "id": "foo12345",
                    "duration_minutes": 300,
                    "price": {
                        "amount": 100,
                        "currency": "EUR",
                    },
                },
                {
                    "id": "bar",
                    "duration_minutes": 150,
                    "price": {
                        "amount": 200,
                        "currency": "EUR",
                    },
                },
            ],
        }), cursor)
        old_sorted_count = getattr(sort_request, "sorted_count", 0)
        sort_request(Request({
            "sorting_type": "fastest",
            "itineraries": [
                {
                    "id": "foo6789",
                    "duration_minutes": 300,
                    "price": {
                        "amount": 100,
                        "currency": "EUR",
                    },
                },
                {
                    "id": "bar",
                    "duration_minutes": 150,
                    "price": {
                        "amount": 200,
                        "currency": "EUR",
                    },
                },
            ],
        }), cursor)
        assert old_sorted_count + 1 == getattr(sort_request, "sorted_count", 0)
