SHELL := /bin/bash

.PHONY: backend
backend:
	pip install -r backend/requirements.txt
	python3 backend/web_server.py

.PHONY: frontend
frontend:
	yarn --cwd frontend install
	yarn --cwd frontend run serve

.PHONY: db
db:
	mongod --config /usr/local/etc/mongod.conf

.PHONY: db_setup
db_setup:
	sh insert_doc.sh

.PHONY: db_show
db_show:
	mongo --eval "db.document.find().pretty()" documentation

.PHONY: db_clean
db_clean:
	mongo --eval "db.document.deleteMany({})" documentation