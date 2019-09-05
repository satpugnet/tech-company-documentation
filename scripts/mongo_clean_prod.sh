#!/usr/bin/env bash

# This will drop the documentation database on prod DB
mongo "mongodb+srv://prod_user:TgSS0ftcTNu4pP3W@prod-ixx3d.gcp.mongodb.net/documentation" --eval "db.dropDatabase()"