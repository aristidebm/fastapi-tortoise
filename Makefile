ENVIRONMENT ?= "development"

install:
	poetry install --no-dev

install-dev:
	poetry install

lint:
	poetry run task lint

format:
	poetry run task format

init-db:
	ENVIRONMENT=${ENVIRONMENT} aerich --app models init-db

show-migration:
	aerich history

migrate:
	aerich upgrade

dbshell:
	ENVIRONMENT=${ENVIRONMENT} tortoise-cli shell

run:
	ENVIRONMENT=${ENVIRONMENT} uvicorn src.main:app --reload
