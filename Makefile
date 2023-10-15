.PHONY: all test
all: ## run tests with poetry
	poetry run isort .
	poetry run black .
	poetry run pflake8 .
	poetry run mypy .
	poetry run pytest
test:
	poetry run pytest
