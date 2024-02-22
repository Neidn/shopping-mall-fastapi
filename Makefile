#!make
include .env

VENV_DIR=.venv
VENV_BIN = $(VENV_DIR)/bin
VENV_PYTHON = $(VENV_BIN)/python
NOSETESTS   = $(VENV_BIN)/nosetests

run_back:
	@echo "Running the backend server"
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && $(VENV_PYTHON) -m uvicorn src.asgi:app --port $(BACKEND_SERVER_PORT) --reload \
	 --ssl-keyfile $(BACKEND_SSL_KEY) --ssl-certfile $(BACKEND_SSL_CERT)

run_front:
	@echo "Running the frontend server"
	cd $(FRONTEND_DIR) && npm start PORT=$(FRONTEND_SERVER_PORT)

test:
	@echo "Running the tests"
	$(NOSETESTS)

.PHONY: test run_back run_front
