.PHONY: lint test infra app ideps

lint:
	flake8 app/

test:
	pytest app/

test-cov:
	pytest app/ --cov=app --cov-report=xml

infra:
	docker-compose -f local/docker-compose.infra.yaml up --remove-orphans

app:
	docker build . -t hex:latest
	docker-compose -f local/docker-compose.app.yaml up --remove-orphans

web:
	poetry run python -m app web

install-deps:
	pip3 install --upgrade pip
	pip3 install poetry
	poetry install