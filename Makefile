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
	hypercorn "app.api.factory:app()" -b 127.0.0.1:5000 --reload

ideps:
	pip3 install --upgrade pip
	pip3 install poetry
	poetry config virtualenvs.create false --local
	poetry install