SHELL := /bin/bash

.PHONY: backend
backend:
	pip install -r backend/requirements.txt
	python3 backend/server.py

.PHONY: frontend
frontend:
	yarn --cwd frontend install
	yarn --cwd frontend run serve

.PHONY: webhook
webhook:
	smee --url https://smee.io/UUkxjK9NwrD3pnTH --path /webhook_handler --port 5000

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