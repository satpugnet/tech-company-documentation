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