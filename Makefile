SHELL := /bin/bash

.PHONY: backend
backend:
	pip install -r backend/requirements.txt
	pip freeze > backend/requirements.txt
	FLASK_DEBUG=1 python3 backend/server.py

.PHONY: frontend
frontend:
	yarn --cwd frontend install
	yarn --cwd frontend run serve