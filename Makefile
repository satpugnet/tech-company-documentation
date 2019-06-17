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
