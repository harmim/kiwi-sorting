# Kiwi.com - Itineraries Sorting

A REST API for sorting a given list of travel itineraries using various sorting
criteria. See the [task](https://github.com/mcyprian/itineraries_sorting_task).

It is implemented in [Python 3](https://www.python.org) using the
[Flask framework](https://flask.palletsprojects.com).

_The application runs in a Docker container. Thus,
[Docker](https://www.docker.com) needs to be installed._

## Usage

The application can be started using `make` (or `make run`). A web-server runs
inside a Docker container. The sorting end-point is accessible through
`/sort_itineraries`. The port `5000` is mapped from the container to a local
host. Therefore, the application may be accessed via
http://localhost:5000/sort_itineraries.

Below is an example how to make a `POST` sorting request, e.g., using `curl`:
```bash
curl --location 'http://localhost:5000/sort_itineraries' \
  --header 'Content-Type: application/json' \
  --data '{
    "sorting_type": "cheapest",
    "itineraries": [
      {
        "id": "sunny_beach_bliss",
        "duration_minutes": 330,
        "price": {
          "amount": 90,
          "currency": "EUR"
        }
      },
      {
        "id": "rocky_mountain_adventure",
        "duration_minutes": 140,
        "price": {
          "amount": 830,
          "currency": "EUR"
        }
      },
      {
        "id": "urban_heritage_odyssey",
        "duration_minutes": 275,
        "price": {
          "amount": 620,
          "currency": "CZK"
        }
      }
    ]
  }'
```

## Tests

[Pytest](https://docs.pytest.org) is used for testing the application. Tests
are located in [src/tests/](src/tests/). They can be executed using
`make tests`.

All tests are run automatically via GitHub Actions, see
[`tests.yml`](.github/workflows/tests.yml).

## Documentation

The documentation is generated using [Sphinx](https://www.sphinx-doc.org). It
can be generated using `make doc`. This will generate the documentation into
the `docs/_build/` directory in the HTML format. Open
`docs/_build/html/index.html`.

Testing of the generation of the documentation is done via GitHub Actions,
see [`doc.yml`](.github/workflows/doc.yml).

## Author: Dominik Harmim <harmim6@gmail.com>
