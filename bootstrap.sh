#!/bin/sh

protoc -I=./src/protobuffs --python_out=./src/protobuffs ./src/protobuffs/transactions.proto

export FLASK_APP=./src/index.py

flask --debug run -h 0.0.0.0