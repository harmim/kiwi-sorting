# Author: Dominik Harmim <harmim6@gmail.com>

"""The index of the REST API."""

from http import HTTPMethod, HTTPStatus

from flask import Flask, Response
from flask import request as http_request

from .db import database
from .parsing import ParsingError, Request
from .sorting import sort_request

app = Flask(__name__)
"""instance of the Flask application"""


@app.route("/sort_itineraries", methods=[HTTPMethod.POST])
def sort_itineraries() -> Response:
    """
    Process a sorting itineraries POST request.

    A sorting itineraries end-point.

    :return Response: HTTP response
    """
    try:
        request = Request(http_request.get_json())

        with database() as cursor:
            request = sort_request(request, cursor)

        return Response(
            request.to_json(),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )

    except ParsingError as e:
        return Response(e.message, status=HTTPStatus.BAD_REQUEST)

    except:
        return Response(
            "Internal error.", status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
