# Author: Dominik Harmim <harmim6@gmail.com>

"""Module handling the itineraries sorting requests parsing."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from currency_converter import CurrencyConverter

_currency_converter = None


class SortingType(Enum):
    """Itineraries sorting criteria."""

    CHEAPEST = "cheapest"  # sort based on price
    FASTEST = "fastest"  # sort by duration
    BEST = "best"  # sort with the best ones coming first


class ParsingError(Exception):
    """Exception class for sorting requests parsing errors."""

    def __init__(self: ParsingError) -> None:
        """Construct the exception with a message."""
        self.message = "Format of the given sorting request is not valid."
        super().__init__(self.message)


PriceType = int | str
"""type of an itinerary's price"""


@dataclass(init=False, frozen=True)
class Price:
    """Encapsulates an itinerary's price."""

    amount: int
    """price amount in a given currency"""

    currency: str
    """currency of the price"""

    amount_eur: float
    """price amount in EUR"""

    def __init__(self: Price, amount: int, currency: str) -> None:
        """
        Construct a representation of an itinerary's price.

        :param int amount: price amount in a given currency
        :param str currency: currency of the price
        :raises ParsingError: if unknown currency is given
        """
        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "currency", currency)

        try:
            global _currency_converter
            if _currency_converter is None:
                _currency_converter = CurrencyConverter()

            object.__setattr__(
                self,
                "amount_eur",
                _currency_converter.convert(amount, currency, "EUR"),
            )
        except ValueError:
            raise ParsingError

    def _serialise(self: Price) -> Dict[str, PriceType]:
        """
        Serialise the price into a dictionary.

        :return Dict[str, PriceType]:
            dictionary: [property name, property's value]
        """
        return {"amount": self.amount, "currency": self.currency}

    def __hash__(self: Price) -> int:
        """
        Generate a unique hash from the current object.

        :return int: generated hash
        """
        return hash((self.amount, self.currency))


ItineraryType = str | int | PriceType
"""type of an itinerary"""


@dataclass(init=False, frozen=True)
class Itinerary:
    """Encapsulates an itinerary."""

    id: str
    """identifier of the travel itinerary"""

    duration: int
    """total travel duration including all flights and layovers in minutes"""

    price: Price
    """total price of the itinerary"""

    def __init__(self: Itinerary, itinerary_json: Dict[str, Any]) -> None:
        """
        Construct a representation of an itinerary.

        :param Dict[str, Any] itinerary_json: itinerary in the JSON format
        :raises ParsingError: if parsing of the itinerary failed
        """
        if (
            "id" not in itinerary_json
            or not isinstance(itinerary_json["id"], str)
            or "duration_minutes" not in itinerary_json
            or not isinstance(itinerary_json["duration_minutes"], int)
            or "price" not in itinerary_json
            or not isinstance(itinerary_json["price"], Dict)
            or "amount" not in itinerary_json["price"]
            or not isinstance(itinerary_json["price"]["amount"], int)
            or "currency" not in itinerary_json["price"]
            or not isinstance(itinerary_json["price"]["currency"], str)
        ):
            raise ParsingError

        object.__setattr__(self, "id", itinerary_json["id"])
        object.__setattr__(self, "duration", itinerary_json["duration_minutes"])
        object.__setattr__(
            self,
            "price",
            Price(
                itinerary_json["price"]["amount"],
                itinerary_json["price"]["currency"],
            ),
        )

    def _serialise(self: Itinerary) -> Dict[str, ItineraryType]:
        """
        Serialise the itinerary into a dictionary.

        :return Dict[str, ItineraryType]:
            dictionary: [property name, property's value]
        """
        return {
            "id": self.id,
            "duration_minutes": self.duration,
            "price": self.price._serialise(),
        }


    def __hash__(self: Itinerary) -> int:
        """
        Generate a unique hash from the current object.

        :return int: generated hash
        """
        return hash((self.id, self.duration, self.price))


Itineraries = List[Itinerary]
"""list of itineraries"""


@dataclass(init=False)
class Request:
    """Encapsulates a sorting request."""

    sorting_type: SortingType
    """sorting criteria"""

    itineraries: Itineraries
    """itineraries to be sorted"""

    def __init__(self: Request, request_json: Dict[str, Any]) -> None:
        """
        Construct a representation of a sorting request.

        :param Dict[str, Any] request_json: sorting request in the JSON format
        :raises ParsingError: if parsing of the sorting request failed
        """
        if (
            "sorting_type" not in request_json
            or request_json["sorting_type"] not in
                [t.value for t in SortingType]
            or "itineraries" not in request_json
            or not isinstance(request_json["itineraries"], List)
        ):
            raise ParsingError

        self.sorting_type = SortingType(request_json["sorting_type"])
        self.itineraries = [Itinerary(i) for i in request_json["itineraries"]]

    def to_json(self: Request) -> str:
        """
        Convert the current object to the JSON format.

        :return str: the current object in the JSON format
        """
        return json.dumps({
            "sorting_type": self.sorting_type.value,
            "sorted_itineraries": [i._serialise() for i in self.itineraries]
        }, indent=2)

    def __hash__(self: Request) -> int:
        """
        Generate a unique hash from the current object.

        :return int: generated hash
        """
        return hash((
            self.sorting_type,
            ''.join([str(hash(i)) for i in self.itineraries]),
        ))
