# Author: Dominik Harmim <harmim6@gmail.com>

"""Testing the itineraries sorting requests parsing."""

import json

import pytest

from ..parsing import ParsingError, Request, SortingType


def test_invalid_requests() -> None:
    """Test parsing invalid requests."""

    # empty request
    with pytest.raises(ParsingError):
        Request({})

    # invalid types
    with pytest.raises(ParsingError):
        Request({
            "sorting_type": "cheapest",
            "itineraries": [{
                "id": "sunny_beach_bliss",
                "duration_minutes": "275",
                "price": {
                    "amount": True,
                    "currency": ["CZK"],
                },
            }],
        })

    # invalid fields
    with pytest.raises(ParsingError):
        Request({
            "sorting_type": "xxx",
            "itineraries": [{
                "id": "sunny_beach_bliss",
                "duration_minutes": 275,
                "price": {
                    "value": 620,
                    "currency": "CZK",
                },
            }],
        })

    # missing fields
    with pytest.raises(ParsingError):
        Request({
            "sorting_type": "cheapest",
            "itineraries": [{
                "duration_minutes": 275,
                "price": {
                    "currency": "CZK",
                },
            }],
        })

    # unknown currency
    with pytest.raises(ParsingError):
        Request({
            "sorting_type": "cheapest",
            "itineraries": [{
                "id": "sunny_beach_bliss",
                "duration_minutes": 275,
                "price": {
                    "amount": 620,
                    "currency": "FOO",
                },
            }],
        })


def test_valid_requests() -> None:
    """Test parsing valid requests."""

    request = Request({
        "sorting_type": "cheapest",
        "itineraries": [{
            "id": "sunny_beach_bliss",
            "duration_minutes": 275,
            "price": {
                "amount": 620,
                "currency": "CZK",
            },
        }],
    })

    assert request.sorting_type.value == SortingType.CHEAPEST.value
    assert len(request.itineraries) == 1

    itinerary = request.itineraries[0]
    assert itinerary.id == "sunny_beach_bliss"
    assert itinerary.duration == 275
    assert itinerary.price.amount == 620
    assert itinerary.price.currency == "CZK"
    assert itinerary.price.amount_eur < itinerary.price.amount


def test_request_to_json() -> None:
    """Test converting a request to JSON."""

    request = Request({
        "sorting_type": "cheapest",
        "itineraries": [{
            "id": "sunny_beach_bliss",
            "duration_minutes": 275,
            "price": {
                "amount": 620,
                "currency": "CZK",
            },
        }],
    })

    json1 = json.dumps({
        "sorting_type": "cheapest",
        "sorted_itineraries": [{
            "id": "sunny_beach_bliss",
            "duration_minutes": 275,
            "price": {
                "amount": 620,
                "currency": "CZK",
            },
        }],
    }, sort_keys=True)
    json2 = json.dumps(json.loads(request.to_json()), sort_keys=True)
    assert json1 == json2
