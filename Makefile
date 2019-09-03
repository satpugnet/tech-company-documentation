SHELL := /bin/bash

.PHONY: backend
backend:
	pip3 install -r backend/requirements.txt
	pip3 freeze > backend/requirements.txt
	FLASK_DEBUG=1 python3 backend/server.py

.PHONY: frontend
frontend:
	yarn --cwd frontend install
	yarn --cwd frontend run serve

.PHONY: webhook
webhook:
	smee --url https://smee.io/UUkxjK9NwrD3pnTH --path /api/webhook_handler --port 5000

.PHONY: db
db:
	mongod --config /usr/local/etc/mongod.conf

.PHONY: db_update
db_update:
	python backend/manually_update_db.py $(organisation_login) $(repo_full_name)

.PHONY: db_setup
db_setup:
	sh insert_doc.sh

.PHONY: db_show
db_show:
	mongo --eval "db.document.find().pretty()" documentation

.PHONY: db_clean
db_clean:
	mongo --eval "db.dropDatabase()" documentation

.PHONY: db_clean
db_clean_prod:
	mongo "mongodb+srv://prod_user:TgSS0ftcTNu4pP3W@prod-ixx3d.gcp.mongodb.net/documentation" --eval "db.dropDatabase()"