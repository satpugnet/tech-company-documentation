#!/usr/bin/env bash

# This will drop the documentation database on localhost:27017
mongo --eval "db.dropDatabase()" documentation