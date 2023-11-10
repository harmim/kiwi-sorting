#!/usr/bin/env bash

# Author: Dominik Harmim <harmim6@gmail.com>

export FLASK_APP=./src/index.py
pipenv run flask run -h 0.0.0.0
