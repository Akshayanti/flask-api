#!/bin/sh

export FLASK_APP=./flask_api/index.py

flask --debug run -h 0.0.0.0